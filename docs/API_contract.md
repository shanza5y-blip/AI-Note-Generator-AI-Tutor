# API Contract

## Project
AI Note Generator + AI Tutor

## Base URL

http://localhost:8000

---

# 1. Upload Syllabus

## Method

POST

## URL

/upload-syllabus

## Description

Upload a syllabus PDF file and store it in the system.

## Request

Content-Type: multipart/form-data

### Request Fields

| Field | Type | Required |
|---------|---------|---------|
| file | PDF File | Yes |

## Response

Status Code: 201 Created

```json
{
    "file_id": 1,
    "filename": "dbms_syllabus.pdf",
    "status": "uploaded"
}
```

### Response Fields

| Field | Type |
|---------|---------|
| file_id | integer |
| filename | string |
| status | string |

### Status Codes

| Code | Description |
|---------|---------|
| 201 | File uploaded successfully |
| 400 | Invalid file |
| 500 | Internal server error |

---

# 2. Get Subjects

## Method

GET

## URL

/subjects/{file_id}

## Description

Retrieve all subjects extracted from the uploaded syllabus.

## Path Parameters

| Field | Type |
|---------|---------|
| file_id | integer |

## Response

Status Code: 200 OK

```json
{
    "file_id": 1,
    "subjects": [
        {
            "id": 1,
            "subject_name": "Database Management System"
        },
        {
            "id": 2,
            "subject_name": "Operating Systems"
        }
    ]
}
```

### Response Fields

| Field | Type |
|---------|---------|
| file_id | integer |
| subjects | array |
| id | integer |
| subject_name | string |

### Status Codes

| Code | Description |
|---------|---------|
| 200 | Success |
| 404 | File not found |
| 500 | Internal server error |

---

# 3. Generate Notes

## Method

POST

## URL

/generate-notes

## Description

Generate Detailed, Exam, or Revision notes for a selected subject and unit.

## Request

```json
{
    "subject_id": 1,
    "unit_id": 2,
    "note_type": "Detailed"
}
```

### Request Fields

| Field | Type | Required |
|---------|---------|---------|
| subject_id | integer | Yes |
| unit_id | integer | Yes |
| note_type | string | Yes |

### Allowed Values

- Detailed
- Exam
- Revision

## Response

```json
{
    "subject_id": 1,
    "unit_id": 2,
    "note_type": "Detailed",
    "notes": "Generated notes content..."
}
```

### Response Fields

| Field | Type |
|---------|---------|
| subject_id | integer |
| unit_id | integer |
| note_type | string |
| notes | string |

### Status Codes

| Code | Description |
|---------|---------|
| 200 | Success |
| 400 | Invalid request |
| 500 | Internal server error |

---

# 4. AI Tutor Chat

## Method

POST

## URL

/chat

## Description

Answer questions using uploaded syllabus and generated notes.

## Request

```json
{
    "subject_id": 1,
    "question": "Explain normalization",
    "teaching_mode": "Beginner"
}
```

### Request Fields

| Field | Type | Required |
|---------|---------|---------|
| subject_id | integer | Yes |
| question | string | Yes |
| teaching_mode | string | Yes |

### Allowed Values

- Beginner
- Exam-Oriented

## Response

```json
{
    "answer": "Normalization is a database design technique used to reduce redundancy and improve data integrity."
}
```

### Response Fields

| Field | Type |
|---------|---------|
| answer | string |

### Status Codes

| Code | Description |
|---------|---------|
| 200 | Success |
| 400 | Invalid request |
| 500 | Internal server error |