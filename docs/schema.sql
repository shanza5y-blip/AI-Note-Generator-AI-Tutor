-- =====================================================
-- AI Note Generator + AI Tutor
-- Database Schema
-- Version 1.0
-- =====================================================

PRAGMA foreign_keys = ON;

-- =====================================================
-- FILES
-- Stores uploaded syllabus PDFs
-- =====================================================

CREATE TABLE IF NOT EXISTS files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL,
    upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT NOT NULL
);

-- =====================================================
-- SUBJECTS
-- Extracted subjects from syllabus
-- =====================================================

CREATE TABLE IF NOT EXISTS subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_id INTEGER NOT NULL,
    subject_name TEXT NOT NULL,

    FOREIGN KEY (file_id)
        REFERENCES files(id)
        ON DELETE CASCADE
);

-- =====================================================
-- UNITS
-- Units belonging to a subject
-- =====================================================

CREATE TABLE IF NOT EXISTS units (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_id INTEGER NOT NULL,
    unit_name TEXT NOT NULL,

    FOREIGN KEY (subject_id)
        REFERENCES subjects(id)
        ON DELETE CASCADE
);

-- =====================================================
-- CHUNKS (Metadata Mirror)
--
-- Actual chunk content and embeddings live in ChromaDB.
-- This table stores references for backend tracking.
-- =====================================================

CREATE TABLE IF NOT EXISTS chunks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    file_id INTEGER NOT NULL,
    subject_id INTEGER NOT NULL,
    unit_id INTEGER NOT NULL,

    chunk_id TEXT NOT NULL,
    source_file TEXT NOT NULL,
    page_number INTEGER,

    FOREIGN KEY (file_id)
        REFERENCES files(id)
        ON DELETE CASCADE,

    FOREIGN KEY (subject_id)
        REFERENCES subjects(id)
        ON DELETE CASCADE,

    FOREIGN KEY (unit_id)
        REFERENCES units(id)
        ON DELETE CASCADE
);

-- =====================================================
-- ChromaDB Design Reference
-- =====================================================

-- Collection Name:
-- notes_chunks

-- Embedding Model:
-- sentence-transformers/all-MiniLM-L6-v2

-- Metadata Stored:
-- user_id
-- file_id
-- subject
-- chunk_id
-- source_file
-- unit
-- page_number

-- Retrieval Example:
--
-- query = "Explain paging"
--
-- filter = {
--   "user_id": "u001"
-- }

-- Strategy:
-- Single Global Collection

-- Status:
-- LOCKED
