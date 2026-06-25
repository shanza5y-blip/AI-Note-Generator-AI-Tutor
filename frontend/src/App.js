import React, { useState } from "react";

import LoginPage from "./pages/LoginPage";
import UploadPage from "./pages/UploadPage";
import SubjectBrowserPage from "./pages/SubjectBrowserPage";
import NoteViewerPage from "./pages/NoteViewerPage";
import TutorChatPage from "./pages/TutorChatPage";

import "./App.css";

function App() {
  const [page, setPage] = useState("login");

  const [uploadedFile, setUploadedFile] = useState(null);

  const [selectedSubject, setSelectedSubject] =
    useState(null);

  const [generatedNotes, setGeneratedNotes] =
    useState(null);

  const handleLogin = () => {
    setPage("upload");
  };

  const handleUpload = (fileData) => {
    setUploadedFile(fileData);
    setPage("subjects");
  };

  const handleSubjectSelect = (subject) => {
    setSelectedSubject(subject);

    const notes = {
      title: `${subject.name} Notes`,
      date: new Date().toLocaleDateString(),

      overview:
        "Based on the uploaded syllabus, these notes summarize the selected subject and key concepts.",

      keyPoints: [
        "Core concepts explained clearly",
        "Important exam-oriented topics",
        "Definitions and terminology",
        "Examples and practical applications",
        "Revision-friendly summary",
      ],
    };

    setGeneratedNotes(notes);

    setPage("notes");
  };

  const goToChat = () => {
    setPage("chat");
  };

  const goToNotes = () => {
    setPage("notes");
  };

  const logout = () => {
    setUploadedFile(null);
    setSelectedSubject(null);
    setGeneratedNotes(null);
    setPage("login");
  };

  return (
    <div className="app-container">
      {/* Floating Navigation */}
      {page !== "login" && (
        <div className="floating-nav">
          <button
            className={
              page === "upload"
                ? "nav-btn active"
                : "nav-btn"
            }
            onClick={() => setPage("upload")}
          >
            Upload
          </button>

          <button
            className={
              page === "subjects"
                ? "nav-btn active"
                : "nav-btn"
            }
            onClick={() => setPage("subjects")}
          >
            Subjects
          </button>

          <button
            className={
              page === "notes"
                ? "nav-btn active"
                : "nav-btn"
            }
            onClick={() => setPage("notes")}
          >
            Notes
          </button>

          <button
            className={
              page === "chat"
                ? "nav-btn active"
                : "nav-btn"
            }
            onClick={() => setPage("chat")}
          >
            Tutor Chat
          </button>

          <button
            className="nav-btn logout-btn"
            onClick={logout}
          >
            Logout
          </button>
        </div>
      )}

      {/* Login */}
      {page === "login" && (
        <LoginPage onLogin={handleLogin} />
      )}

      {/* Upload */}
      {page === "upload" && (
        <UploadPage
          uploadedFile={uploadedFile}
          onUpload={handleUpload}
        />
      )}

      {/* Subject Browser */}
      {page === "subjects" && (
        <SubjectBrowserPage
          onSelect={handleSubjectSelect}
        />
      )}

      {/* Notes Viewer */}
      {page === "notes" && (
        <NoteViewerPage
          notes={generatedNotes}
          uploadedFile={uploadedFile}
          selectedSubject={selectedSubject}
          onOpenChat={goToChat}
        />
      )}

      {/* Tutor Chat */}
      {page === "chat" && (
        <TutorChatPage
          onOpenNotes={goToNotes}
        />
      )}
    </div>
  );
}

export default App;