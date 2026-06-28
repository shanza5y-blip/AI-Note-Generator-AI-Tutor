from typing import List, Literal
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from PyPDF2 import PdfReader
from backend.parser import extract_pdf_text, parse_syllabus
from datetime import datetime
from rag.ingest import ingest_file
from rag.note_generator import generate_notes
from rag.tutor import tutor_chat
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
        "http://localhost:5173",  # Ayisha's Vite React app
        "http://localhost:3000",  # fallback just in case
        "http://localhost:3001",  # what Shanza had before
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_NAME = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "database.db")


def create_chat_table():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_id INTEGER NOT NULL,
            subject TEXT NOT NULL,
            message TEXT NOT NULL,
            answer TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(file_id) REFERENCES files(id)
        )
    """)

    conn.commit()
    conn.close()


create_chat_table()


class GenerateNotesRequest(BaseModel):
    file_id: int
    module_name: str
    note_type: Literal["detailed", "exam", "revision"]


class ChatHistory(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    file_id: int
    subject: str
    message: str
    history: List[ChatHistory] = []


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

        # Save subject
        cursor.execute(
            """
            INSERT INTO subjects(file_id, subject_name)
            VALUES (?, ?)
            """,
            (
                file_id,
                parsed_data["subject"]
            )
        )

        subject_id = cursor.lastrowid

        # Save modules
        for module in parsed_data["modules"]:
            cursor.execute(
                """
                INSERT INTO units(subject_id, unit_name)
                VALUES (?, ?)
                """,
                (
                    subject_id,
                    module["module_name"]
                )
            )

        # Update uploaded file
        cursor.execute(
            """
            UPDATE files
            SET
                status=?,
                parsed_json=?
            WHERE id=?
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
            "subject": parsed_data["subject"],
            "modules": [
                module["module_name"]
                for module in parsed_data["modules"]
            ]
        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=f"PDF processing failed: {str(e)}"
        )


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
        request.module_name,
        request.note_type
    )

    generated_at = datetime.utcnow().isoformat()

    # Log generation
    cursor.execute(
        """
    INSERT INTO generation_log
        (
            file_id,
            module_name,
            note_type,
            generated_at,
            token_count
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            request.file_id,
            request.module_name,
            request.note_type,
            generated_at,
            None
        )
    )

    conn.commit()
    conn.close()

    return {
        "note_type": request.note_type,
        "module_name": request.module_name,
        "content": result["content"],
        "warning": result["warning"],
        "generated_at": generated_at
    }


@app.post("/chat")
async def chat(request: ChatRequest):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Validate file_id
    cursor.execute(
        "SELECT id FROM files WHERE id=?",
        (request.file_id,)
    )

    if cursor.fetchone() is None:
        conn.close()
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )

    # Validate message
    if not request.message.strip():
        conn.close()
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty"
        )

    try:
        # Call Intern 2's tutor function
        result = await asyncio.to_thread(
            tutor_chat,
            request.file_id,
            request.subject,
            request.message,
            [h.model_dump() for h in request.history]
        )

        # Save chat to database
        cursor.execute(
            """
            INSERT INTO chat_log
            (
                file_id,
                subject,
                message,
                answer
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                request.file_id,
                request.subject,
                request.message,
                result["answer"]
            )
        )

        conn.commit()

        return {
            "answer": result["answer"],
            "sources": result["sources"]
        }

    except Exception as e:

        conn.rollback()

        raise HTTPException(
            status_code=400,
            detail=f"Chat failed: {str(e)}"
        )

    finally:
        conn.close()
