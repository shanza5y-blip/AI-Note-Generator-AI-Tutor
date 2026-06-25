from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from PyPDF2 import PdfReader
from parser import extract_pdf_text, parse_syllabus
from datetime import datetime
from ingest import ingest_file
from note_generator import generate_notes
import asyncio
import sqlite3
import os
import json
import re

app = FastAPI()


@app.get("/")
def root():
    return RedirectResponse(url="/docs")


# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_NAME = "database.db"


from typing import Literal

class GenerateNotesRequest(BaseModel):
    file_id: int
    subject: str
    unit_name: str
    note_type: Literal["detailed", "exam", "revision"]


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.post("/upload-syllabus")
async def upload_notes(file: UploadFile = File(...)):

    # Validate file type
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    os.makedirs("uploads", exist_ok=True)

    file_path = os.path.join(
        "uploads",
        file.filename
    )

    try:

        # Save PDF
        content = await file.read()

        if not content:
            raise HTTPException(
                status_code=400,
                detail="Uploaded file is empty"
            )

        with open(file_path, "wb") as f:
            f.write(content)

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO files
            (filename, status)
            VALUES (?, ?)
            """,
            (
                file.filename,
                "processing"
            )
        )

        conn.commit()

        file_id = cursor.lastrowid
        # Extract text
        pdf_data = extract_pdf_text(file_path)

        extracted_text = pdf_data["text"]

        page_count = pdf_data["page_count"]
        print("\n" + "=" * 60)
        print("EXTRACTED TEXT PREVIEW")
        print("=" * 60)
        print(extracted_text[:5000])
        print("=" * 60)
        if not extracted_text.strip():
            raise HTTPException(
                status_code=400,
                detail="PDF contains no readable text"
            )

        # Debug Preview

        with open("debug.txt", "w", encoding="utf-8") as f:
            f.write(extracted_text[:10000])
        # Parse syllabus
        parsed_data = parse_syllabus(
            extracted_text
        )

        print("PARSED DATA:")
        print(json.dumps(parsed_data, indent=2))

        # Database
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE files
            SET status = ?,
                parsed_json = ?
            WHERE id = ?
            """,
            (
                "completed",
                json.dumps(parsed_data),
                file_id
            )
        )
        conn.commit()
        asyncio.create_task(
            asyncio.to_thread(
                ingest_file,
                file_id,
                parsed_data
            )
        )
        conn.close()

        return {
            "file_id": file_id,
            "filename": file.filename,
            "page_count": page_count,
            "status": "completed",
            "subject_url": f"/subjects/{file_id}"
        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=f"PDF processing failed: {str(e)}"
        )


@app.get("/subjects/{file_id}")
def get_subjects(file_id: int):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            status,
            parsed_json
        FROM files
        WHERE id = ?
        """,
        (file_id,)
    )

    row = cursor.fetchone()

    conn.close()

    if not row:
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )
    if row[0] == "processing":

        return {
            "file_id": file_id,
            "status": "processing"
        }
    return {
        "file_id": file_id,
        "status": row[0],
        "data": json.loads(row[1])
        if row[1]
        else None
    }


@app.post("/generate-notes")
async def generate_notes_endpoint(request: GenerateNotesRequest):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Check file exists
    cursor.execute(
        "SELECT id FROM files WHERE id=?",
        (request.file_id,)
    )

    file = cursor.fetchone()

    if not file:
        conn.close()
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )

    # Call Intern 2's function
    result = await asyncio.to_thread(
        generate_notes,
        request.file_id,
        request.unit_name,
        request.note_type
    )

    generated_at = datetime.utcnow().isoformat()

    # Log generation
    cursor.execute(
        """
        INSERT INTO generation_log
        (
            file_id,
            unit_name,
            note_type,
            generated_at,
            token_count
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            request.file_id,
            request.unit_name,
            request.note_type,
            generated_at,
            None
        )
    )

    conn.commit()
    conn.close()

    return {
        "note_type": request.note_type,
        "unit_name": request.unit_name,
        "content": result["content"],
        "warning": result["warning"],
        "generated_at": generated_at
    }