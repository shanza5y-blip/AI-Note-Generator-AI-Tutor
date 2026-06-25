import React, { useState } from "react";

const NoteViewerPage = ({ selectedSubject }) => {
  const [selectedUnit, setSelectedUnit] =
    useState("");

  const [noteType, setNoteType] =
    useState("Detailed");

  const [loading, setLoading] =
    useState(false);

  const [generatedNote, setGeneratedNote] =
    useState(null);

  const [error, setError] =
    useState("");

  const [warning, setWarning] =
    useState("");

  if (!selectedSubject) {
    return (
      <div className="note-viewer-page">
        <div className="empty-note-state">
          <h2>No Subject Selected</h2>
          <p>Please select a subject first.</p>
        </div>
      </div>
    );
  }

  const handleGenerateNotes = async () => {
    if (!selectedUnit) {
      setError(
        "Please select a unit before generating notes."
      );
      return;
    }

    setLoading(true);
    setError("");
    setGeneratedNote(null);
    setWarning("");

    try {
      await new Promise((resolve) =>
        setTimeout(resolve, 2000)
      );

      const mockResponse = {
        title: `${selectedSubject.name} - ${selectedUnit}`,
        content: `
Subject: ${selectedSubject.name}

Unit: ${selectedUnit}

Note Type: ${noteType}

----------------------------------------

Introduction

These are mock notes generated for UI testing.

Important Concepts

• Concept 1
• Concept 2
• Concept 3
• Concept 4

Summary

This content is currently hardcoded until the backend API becomes available.

Generated Successfully.
        `,
        warning: true,
      };

      setGeneratedNote(mockResponse);

      if (mockResponse.warning) {
        setWarning(
          "Note: limited syllabus content found for this unit. Results may be incomplete."
        );
      }
    } catch (err) {
      setError(
        "Unable to generate notes. Please try again later."
      );
    }

    setLoading(false);
  };

  const downloadNotes = () => {
    if (!generatedNote) return;

    const content = `
${generatedNote.title}

${generatedNote.content}
`;

    const blob = new Blob(
      [content],
      {
        type: "text/plain",
      }
    );

    const url =
      window.URL.createObjectURL(blob);

    const link =
      document.createElement("a");

    link.href = url;

    link.download = `${selectedSubject.name}_${selectedUnit}_Notes.txt`;

    document.body.appendChild(link);

    link.click();

    document.body.removeChild(link);

    window.URL.revokeObjectURL(url);
  };

  return (
    <div className="note-viewer-page">

      <h1>Generate Notes</h1>

      {/* Subject */}
      <div className="form-group">
        <label>
          Selected Subject
        </label>

        <input
          type="text"
          value={selectedSubject.name}
          disabled
        />
      </div>

      {/* Unit */}
      <div className="form-group">
        <label>
          Select Unit
        </label>

        <select
          value={selectedUnit}
          onChange={(e) =>
            setSelectedUnit(
              e.target.value
            )
          }
        >
          <option value="">
            Choose Unit
          </option>

          {selectedSubject.units.map(
            (unit, index) => (
              <option
                key={index}
                value={unit}
              >
                {unit}
              </option>
            )
          )}
        </select>
      </div>

      {/* Note Type */}
      <div className="note-type-buttons">

        <button
          className={
            noteType === "Detailed"
              ? "active"
              : ""
          }
          onClick={() =>
            setNoteType(
              "Detailed"
            )
          }
        >
          Detailed
        </button>

        <button
          className={
            noteType === "Exam"
              ? "active"
              : ""
          }
          onClick={() =>
            setNoteType(
              "Exam"
            )
          }
        >
          Exam
        </button>

        <button
          className={
            noteType === "Revision"
              ? "active"
              : ""
          }
          onClick={() =>
            setNoteType(
              "Revision"
            )
          }
        >
          Revision
        </button>

      </div>

      {/* Generate */}
      <button
        className="generate-btn"
        disabled={
          loading ||
          !selectedUnit
        }
        onClick={
          handleGenerateNotes
        }
      >
        {loading
          ? "Generating your notes..."
          : "Generate Notes"}
      </button>

      {/* Error */}
      {error && (
        <div className="error-box">
          {error}
        </div>
      )}

      {/* Warning */}
      {warning && (
        <div className="warning-box">
          {warning}
        </div>
      )}

      {/* Generated Notes */}
      {generatedNote && (
        <div className="generated-note">

          <div
            className="notes-toolbar"
          >
            <h2>
              {
                generatedNote.title
              }
            </h2>

            <button
              className="download-btn"
              onClick={
                downloadNotes
              }
            >
              Download Notes
            </button>
          </div>

          <pre>
            {
              generatedNote.content
            }
          </pre>

        </div>
      )}

    </div>
  );
};

export default NoteViewerPage;