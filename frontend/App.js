import React, { useState } from "react";

import LoginPage from "./pages/LoginPage";
import UploadPage from "./pages/UploadPage";
import SubjectBrowserPage from "./pages/SubjectBrowserPage";
import NoteViewerPage from "./pages/NoteViewerPage";
import TutorChatPage from "./pages/TutorChatPage";

import "./App.css";

function App() {
  const [page, setPage] = useState("login");

  const [uploadedFile, setUploadedFile] =
    useState(null);

  const [selectedSubject, setSelectedSubject] =
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
    setPage("notes");
  };

  const goToNotes = () => {
    setPage("notes");
  };

  const logout = () => {
    setUploadedFile(null);
    setSelectedSubject(null);
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

      {/* Login Page */}
      {page === "login" && (
        <LoginPage onLogin={handleLogin} />
      )}

      {/* Upload Page */}
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

      {/* Note Viewer */}
      {page === "notes" && (
        <NoteViewerPage
          selectedSubject={selectedSubject}
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