-- =====================================================
-- AI Note Generator + AI Tutor
-- Database Schema
-- Version 1.0
-- =====================================================

-- Files Table

CREATE TABLE files (
id INTEGER PRIMARY KEY AUTOINCREMENT,
filename TEXT NOT NULL,
upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
status TEXT NOT NULL
);

-- Subjects Table

CREATE TABLE subjects (
id INTEGER PRIMARY KEY AUTOINCREMENT,
file_id INTEGER NOT NULL,
subject_name TEXT NOT NULL,
FOREIGN KEY (file_id) REFERENCES files(id)
);

-- Units Table

CREATE TABLE units (
id INTEGER PRIMARY KEY AUTOINCREMENT,
subject_id INTEGER NOT NULL,
unit_name TEXT NOT NULL,
FOREIGN KEY (subject_id) REFERENCES subjects(id)
);

-- =====================================================
-- ChromaDB Metadata Mapping
-- =====================================================
--------------------------------------------------------

-- Collection Name:
-- notes_chunks
---------------

## -- Metadata Stored:

-- user_id
-- file_id
-- subject
-- chunk_id
-- source_file
-- unit
-- page_number
--------------

## -- Example:

-- {
--   "user_id":"u001",
--   "file_id":"f001",
--   "subject":"Operating Systems",
--   "chunk_id":"chunk_102",
--   "source_file":"os_notes.pdf",
--   "unit":"Unit 3",
--   "page_number":14
-- }
----

-- Embedding Model:
-- sentence-transformers/all-MiniLM-L6-v2
-----------------------------------------

-- Collection Strategy:
-- Single Global Collection
-- Collection Name: notes_chunks
--------------------------------

-- Filtering:
-- user_id
-- file_id
-- subject
-- unit
-------

-- Design Status: LOCKED
