-- =====================================================
-- AI Note Generator + AI Tutor
-- Database Schema
-- Version 1.0
-- =====================================================

PRAGMA foreign_keys = ON;

-- =====================================================
-- FILES
-- =====================================================

CREATE TABLE IF NOT EXISTS files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL,
    upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT NOT NULL
);

-- =====================================================
-- SUBJECTS
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

-- Strategy:
-- Single Global Collection

-- Status:
-- LOCKED
