# Day 6 Test Checklist

## TC-01: Backend Starts
Action:
- Run the backend server.

Expected Result:
- Server starts successfully.
- Swagger opens without errors.

Status:
[ ] Pass


---

## TC-02: Health API

Action:
- Open /health endpoint.

Expected Result:
- Returns:
{
  "status": "ok"
}

Status:
[ ] Pass


---

## TC-03: Upload Valid PDF

Action:
- Upload a syllabus PDF.

Expected Result:
- Upload succeeds.
- Returns file_id.
- Returns subject.
- Returns module list.

Status:
[ ] Pass


---

## TC-04: Reject Invalid File

Action:
- Upload a JPG or TXT file.

Expected Result:
- Error:
Only PDF files are allowed.

Status:
[ ] Pass


---

## TC-05: Parse Syllabus

Action:
- Check uploaded syllabus response.

Expected Result:
- Subject extracted correctly.
- All modules extracted.

Status:
[ ] Pass


---

## TC-06: Generate Detailed Notes

Action:
- Generate detailed notes for Module 1.

Expected Result:
- Notes are generated.

Status:
[ ] Pass


---

## TC-07: Generate Exam Notes

Action:
- Generate exam notes.

Expected Result:
- Exam notes generated successfully.

Status:
[ ] Pass


---

## TC-08: Generate Revision Notes

Action:
- Generate revision notes.

Expected Result:
- Revision notes generated successfully.

Status:
[ ] Pass


---

## TC-09: AI Tutor

Action:
- Ask a question about Module 1.

Expected Result:
- AI returns an answer.
- Sources are included.

Status:
[ ] Pass


---

## TC-10: Invalid File ID

Action:
- Generate notes using an invalid file_id.

Expected Result:
- Returns:
File not found.

Status:
[ ] Pass
