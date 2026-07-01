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
    status TEXT NOT NULL,
    parsed_json TEXT
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
CREATE TABLE IF NOT EXISTS modules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_id INTEGER NOT NULL,
    module_name TEXT NOT NULL,

    FOREIGN KEY (subject_id)
        REFERENCES subjects(id)
        ON DELETE CASCADE
);


-- =====================================================
-- GENERATION LOG
-- =====================================================

CREATE TABLE IF NOT EXISTS generation_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_id INTEGER NOT NULL,
    module_name TEXT NOT NULL,
    note_type TEXT NOT NULL,
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    token_count INTEGER,

    FOREIGN KEY (file_id)
        REFERENCES files(id)
        ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS chat_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_id INTEGER NOT NULL,
    subject TEXT NOT NULL,
    message TEXT NOT NULL,
    answer TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(file_id) REFERENCES files(id)
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
