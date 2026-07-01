import React, { useState } from "react";

const NoteViewerPage = ({ selectedSubject }) => {
  const [selectedUnit, setSelectedUnit] = useState("");
  const [noteType, setNoteType] = useState("Detailed");
  const [loading, setLoading] = useState(false);
  const [generatedNote, setGeneratedNote] = useState(null);
  const [error, setError] = useState("");
  const [warning, setWarning] = useState("");

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
      setError("Please select a unit before generating notes.");
      return;
    }

    setLoading(true);
    setError("");
    setGeneratedNote(null);
    setWarning("");

    try {
      console.log("selectedSubject =", selectedSubject);
      console.log("file_id =", selectedSubject.file_id);

      const response = await fetch("http://localhost:8000/generate-notes", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          file_id: selectedSubject.file_id,
          subject: selectedSubject.name,
          module_name: selectedUnit,
          note_type: noteType.toLowerCase() === "quick"
            ? "revision"
            : noteType.toLowerCase()
        })
      });

      const data = await response.json();

      if (!response.ok) {
        setError("Failed to generate notes: " + (data.detail || "Unknown error"));
        setLoading(false);
        return;
      }

      setGeneratedNote({
        title: `${selectedSubject.name} - ${selectedUnit}`,
        content: data.content
      });

      if (data.warning) {
        setWarning(data.warning);
      }

    } catch (err) {
      setError("Unable to generate notes. Please try again later.");
    }

    setLoading(false);
  };

  const downloadNotes = () => {
    if (!generatedNote) return;
    const blob = new Blob([`${generatedNote.title}\n\n${generatedNote.content}`], { type: "text/plain" });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement("a");
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

      <div className="form-group">
        <label>Selected Subject</label>
        <input type="text" value={selectedSubject.name} disabled />
      </div>

      <div className="form-group">
        <label>Select Unit</label>
        <select value={selectedUnit} onChange={(e) => setSelectedUnit(e.target.value)}>
          <option value="">Choose Unit</option>
          {selectedSubject.units.map((unit, index) => (
            <option key={index} value={unit}>{unit}</option>
          ))}
        </select>
      </div>

      <div className="note-type-buttons">
        {["Detailed", "Exam", "Revision"].map((type) => (
          <button
            key={type}
            className={noteType === type ? "active" : ""}
            onClick={() => setNoteType(type)}
          >
            {type}
          </button>
        ))}
      </div>

      <button
        className="generate-btn"
        disabled={loading || !selectedUnit}
        onClick={handleGenerateNotes}
      >
        {loading ? "Generating your notes..." : "Generate Notes"}
      </button>

      {error && <div className="error-box">{error}</div>}
      {warning && <div className="warning-box">{warning}</div>}

      {generatedNote && (
        <div className="generated-note">
          <div className="notes-toolbar">
            <h2>{generatedNote.title}</h2>
            <button className="download-btn" onClick={downloadNotes}>
              Download Notes
            </button>
          </div>
          <pre>{generatedNote.content}</pre>
        </div>
      )}
    </div>
  );
};

export default NoteViewerPage;