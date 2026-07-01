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

const UploadPage = ({
  onUpload,
  onViewNotes,
}) => {
  const fileRef = useRef();

  const [file, setFile] = useState(null);

  const [module, setModule] = useState("");
  const [modules] = useState([]);

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
      // Step 1 — Upload PDF and get file_id
      const formData = new FormData();
      formData.append("file", file);

      const uploadResponse = await fetch(
        "http://localhost:8000/upload-syllabus",
        {
          method: "POST",
          body: formData
        }
      );

      const uploadData = await uploadResponse.json();
      console.log("Upload Response:", uploadData);
      if (!uploadResponse.ok) {
        alert("Upload failed: " + uploadData.detail);
        setLoading(false);
        return;
      }

      const file_id = uploadData.file_id;
      const subject = uploadData.subject;
      const modules = uploadData.modules;
      console.log("Upload API Response:", uploadData);
      console.log("file_id:", file_id);
      console.log("subject:", subject);
      console.log("modules:", modules);
      if (onUpload) {
        onUpload(file, file_id, subject, modules);
      }
      console.log("Calling onUpload with:", file_id);
      // Step 2 — Generate notes
      const notesResponse = await fetch(
        "http://localhost:8000/generate-notes",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            file_id: file_id,
            subject: subject,
            module_name: module || modules[0],
            note_type: noteType === "quick" ? "revision" : noteType
          })
        }
      );

      const notesData = await notesResponse.json();

      setGeneratedNotes(notesData.content);

      if (onViewNotes) {
        onViewNotes({
          file_id: file_id,
          name: subject,
          units: modules,
          notes: notesData.content
        });
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

            <select
              value={module}
              onChange={(e) => setModule(e.target.value)}
            >
              <option value="">
                Select Module
              </option>

              {modules.map((moduleName) => (
                <option
                  key={moduleName}
                  value={moduleName}
                >
                  {moduleName}
                </option>
              ))}
            </select>

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
                className={`note-card ${noteType === type.key
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