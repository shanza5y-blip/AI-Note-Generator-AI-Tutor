import React, { useRef, useState } from "react";

const NOTE_TYPES = [
  {
    key: "detailed",
    icon: "📖",
    title: "Detailed Notes",
    desc: "Full explanations and examples"
  },
  {
    key: "exam",
    icon: "🎯",
    title: "Exam Oriented",
    desc: "Important questions and answers"
  },
  {
    key: "quick",
    icon: "⚡",
    title: "Quick Revision",
    desc: "Short revision notes"
  }
];

const UploadPage = ({ onViewNotes }) => {
  const fileRef = useRef();

  const [file, setFile] = useState(null);

  const [unit, setUnit] = useState("");
  const [chapter, setChapter] = useState("");
  const [module, setModule] = useState("");

  const [noteType, setNoteType] =
    useState("detailed");

  const [loading, setLoading] =
    useState(false);

  const [generatedNotes, setGeneratedNotes] =
    useState("");

  const handleFile = (selectedFile) => {
    if (!selectedFile) return;

    setFile(selectedFile);
  };

  const generateNotes = async () => {
    if (!file) return;

    setLoading(true);

    try {
      const formData = new FormData();

      formData.append("file", file);
      formData.append("unit", unit);
      formData.append("chapter", chapter);
      formData.append("module", module);
      formData.append("noteType", noteType);

      const response = await fetch(
        "http://localhost:8000/generate-notes",
        {
          method: "POST",
          body: formData
        }
      );

      const data = await response.json();

      setGeneratedNotes(data.notes);

      if (onViewNotes) {
        onViewNotes(data.notes);
      }
    } catch (error) {
      console.error(error);

      alert("Failed to generate notes");
    }

    setLoading(false);
  };

  return (
    <div className="upload-page">
      <div className="upload-container">

        <div className="upload-title">
          <h1>Generate Study Notes</h1>

          <p>
            Upload your syllabus and choose
            your preferred note style
          </p>
        </div>

        {/* STEP 1 */}

        <div className="upload-card">
          <div className="card-header">
            <span>1</span>
            Upload your syllabus
          </div>

          {!file ? (
            <div
              className="upload-dropzone"
              onClick={() =>
                fileRef.current.click()
              }
            >
              <input
                type="file"
                ref={fileRef}
                hidden
                accept=".pdf,.doc,.docx,.ppt,.pptx"
                onChange={(e) =>
                  handleFile(
                    e.target.files[0]
                  )
                }
              />

              <div className="upload-icon">
                📄
              </div>

              <h3>
                Click to Upload
              </h3>

              <p>
                PDF, DOCX, PPTX Supported
              </p>
            </div>
          ) : (
            <div className="file-success">
              <div>
                <h3>{file.name}</h3>

                <p>
                  {Math.round(
                    file.size / 1024
                  )}{" "}
                  KB
                </p>
              </div>

              <button
                onClick={() =>
                  setFile(null)
                }
              >
                Remove
              </button>
            </div>
          )}
        </div>

        {/* STEP 2 */}

        <div className="upload-card">
          <div className="card-header">
            <span>2</span>
            Select Scope
          </div>

          <div className="scope-grid">
            <input
              placeholder="Unit"
              value={unit}
              onChange={(e) =>
                setUnit(e.target.value)
              }
            />

            <input
              placeholder="Chapter"
              value={chapter}
              onChange={(e) =>
                setChapter(e.target.value)
              }
            />

            <input
              placeholder="Module"
              value={module}
              onChange={(e) =>
                setModule(e.target.value)
              }
            />
          </div>
        </div>

        {/* STEP 3 */}

        <div className="upload-card">
          <div className="card-header">
            <span>3</span>
            Choose Note Type
          </div>

          <div className="note-type-grid">

            {NOTE_TYPES.map((type) => (

              <div
                key={type.key}
                className={`note-card ${
                  noteType === type.key
                    ? "active"
                    : ""
                }`}
                onClick={() =>
                  setNoteType(type.key)
                }
              >
                <div className="note-icon">
                  {type.icon}
                </div>

                <h3>{type.title}</h3>

                <p>{type.desc}</p>
              </div>

            ))}
          </div>
        </div>

        <button
          className="generate-btn"
          disabled={!file || loading}
          onClick={generateNotes}
        >
          {loading
            ? "Generating..."
            : "Generate Notes"}
        </button>

        {generatedNotes && (
          <div className="notes-preview">
            <h2>Generated Notes</h2>

            <pre>
              {generatedNotes}
            </pre>
          </div>
        )}
      </div>
    </div>
  );
};

export default UploadPage;