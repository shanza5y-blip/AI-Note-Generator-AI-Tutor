# Study Assistant

## Overview
Study Assistant is a web application that helps students organize and access their study materials efficiently.

It allows users to upload notes, browse subjects, view study content, and interact with an AI-powered tutor.

---

## API Base URL

http://localhost:8000

---

## API Documentation

The complete API contract is available in:

api_contract.md

Refer to this document for:

- Endpoint details
- Request formats
- Response formats
- Status codes
- Validation requirements

---

## Features

- Upload study materials
- Browse subjects
- View notes
- AI Tutor Chat
- Simple UI

---

## Tech Stack

Frontend:
- React
- React Router

Backend:
- To be added

Database:
- To be added

---

## Project Structure

study-assistant/
├── frontend/
├── backend/
└── docs/

---

## Setup

Frontend:

```bash
cd frontend
npm install
npm start
---

# AI Tutor

## Overview

The AI Tutor is an AI-powered chat assistant that helps students understand topics from their uploaded syllabus. After a syllabus PDF is uploaded and processed, students can ask questions in natural language and receive answers based on the uploaded study material.

The AI Tutor supports multi-turn conversations by maintaining chat history, allowing students to ask follow-up questions without repeating previous context.

---

## Teaching Modes

The AI Tutor is designed to support two teaching styles.

### Beginner Mode

* Explains concepts using simple language.
* Provides step-by-step explanations.
* Uses examples to improve understanding.
* Suitable for first-time learners.

### Exam-Oriented Mode

* Focuses on important concepts for examinations.
* Gives concise and structured answers.
* Highlights key points for revision.
* Suitable for quick exam preparation.

> **Note:** The current implementation uses the default tutoring behavior. Dedicated teaching mode selection can be added in future versions.

---

## Grounding

The AI Tutor uses a Retrieval-Augmented Generation (RAG) pipeline to ensure responses are based on the uploaded syllabus rather than general knowledge.

Grounding works as follows:

1. The uploaded syllabus PDF is parsed.
2. The extracted content is divided into searchable chunks.
3. Chunks are converted into vector embeddings and stored in ChromaDB.
4. When a student asks a question, the most relevant syllabus sections are retrieved.
5. These retrieved sections are supplied to the language model as context.
6. The model generates a grounded answer using the retrieved information.
7. The answer and its supporting sources are returned to the frontend.

This approach helps reduce hallucinations and keeps responses relevant to the uploaded academic material.

---

## AI Tutor Features

* Chat with uploaded syllabus content.
* Context-aware conversations using chat history.
* Grounded responses using RAG.
* Source references displayed below each AI response.
* Chat logging for future reference.
* Integration with the Study Assistant frontend.
