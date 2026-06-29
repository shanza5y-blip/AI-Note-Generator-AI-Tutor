
import React, { useMemo, useState, useEffect } from "react";

const SubjectBrowserPage = ({ fileId, onSelect }) => {
  const [search, setSearch] = useState("");
  const [selectedSemester, setSelectedSemester] = useState("All");
  const [subjects, setSubjects] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!fileId) return;

    const fetchSubjects = async () => {
      try {
        const response = await fetch(
          `http://localhost:8000/subjects/${fileId}`
        );

        const data = await response.json();

        console.log(data);

        if (data.data) {
          setSubjects([
            {
              id: fileId,
              name: data.data.subject,
              code: "",
              semester: "",
              credits: "",
              units: data.data.units.map(
                unit => unit.unit_name
              )
            }
          ]);
        }

      } catch (error) {
        console.error(error);
      } finally {
        setLoading(false);
      }
    };

    fetchSubjects();

  }, [fileId]);
  const semesters = [
    "All",
    ...new Set(
      subjects.map((subject) => subject.semester)
    ),
  ];

  const filteredSubjects = useMemo(() => {
    return subjects.filter((subject) => {
      const matchesSearch =
        (subject.name || "")
          .toLowerCase()
          .includes(search.toLowerCase()) ||
        (subject.code || "")
          .toLowerCase()
          .includes(search.toLowerCase());

      const matchesSemester =
        selectedSemester === "All"
          ? true
          : subject.semester === selectedSemester;

      return (
        matchesSearch &&
        matchesSemester
      );
    });
  }, [subjects, search, selectedSemester]);
  if (loading) {
    return <h2>Loading subjects...</h2>;
  }
  return (
    <div className="subject-browser-page">

      {/* Header */}
      <div className="page-header">
        <h1>Browse Subjects</h1>

        <p>
          Select a subject to generate
          notes and start learning.
        </p>
      </div>

      {/* Search */}
      <div className="browser-toolbar">

        <input
          type="text"
          className="search-box"
          placeholder="Search subject..."
          value={search}
          onChange={(e) =>
            setSearch(e.target.value)
          }
        />

        <select
          className="semester-filter"
          value={selectedSemester}
          onChange={(e) =>
            setSelectedSemester(
              e.target.value
            )
          }
        >
          {semesters.map((semester) => (
            <option
              key={semester}
              value={semester}
            >
              {semester}
            </option>
          ))}
        </select>

      </div>

      {/* Stats */}
      <div className="subject-stats">

        <div className="stat-card">
          <h3>
            {subjects.length}
          </h3>

          <p>Total Subjects</p>
        </div>

        <div className="stat-card">
          <h3>
            {filteredSubjects.length}
          </h3>

          <p>Results Found</p>
        </div>

      </div>

      {/* Subject Grid */}
      <div className="subject-grid">

        {filteredSubjects.length === 0 ? (
          <div className="empty-state">
            <h3>
              No Subjects Found
            </h3>

            <p>
              Try another search term.
            </p>
          </div>
        ) : (
          filteredSubjects.map(
            (subject) => (
              <div
                key={subject.id}
                className="subject-card"
              >
                <div className="subject-top">

                  <div className="subject-icon">
                    📚
                  </div>

                  <div>

                    <h3>
                      {subject.name}
                    </h3>

                    <p>
                      {subject.code}
                    </p>

                  </div>

                </div>

                <div className="subject-info">

                  <div className="info-row">
                    <span>
                      Semester
                    </span>

                    <span>
                      {
                        subject.semester
                      }
                    </span>
                  </div>

                  <div className="info-row">
                    <span>
                      Credits
                    </span>

                    <span>
                      {
                        subject.credits
                      }
                    </span>
                  </div>

                </div>

                <div className="unit-list">

                  <h4>
                    Units Covered
                  </h4>

                  {subject.units.map(
                    (unit, index) => (
                      <span
                        key={index}
                        className="unit-chip"
                      >
                        {unit}
                      </span>
                    )
                  )}

                </div>

                <button
                  className="select-subject-btn"
                  onClick={() =>
                    onSelect(subject)
                  }
                >
                  Generate Notes
                </button>

              </div>
            )
          )
        )}

      </div>

    </div>
  );
};

export default SubjectBrowserPage;
