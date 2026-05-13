import { useState } from "react";
import ClauseCard from "./components/ClauseCard";

function App() {
  const [file, setFile] = useState(null);
  const [results, setResults] = useState({
    document_summary: null,
    clauses: []
  });

  const handleUpload = async () => {
    if (!file) return;
    const formData = new FormData();
    formData.append("file", file);
    try {
      const res = await fetch(
        "http://127.0.0.1:8000/upload/",
        {
          method: "POST",
          body: formData
        }
      );
      const data = await res.json();
      setResults(data.analysis);
    } catch (err) {
      console.error(err);
    }
  };

  const groupedClauses = {};
  (results?.clauses || []).forEach((clause) => {
    const label =
      clause.predictions?.[0]?.label ||
      "Other";
    if (!groupedClauses[label]) {
      groupedClauses[label] = [];
    }
    groupedClauses[label].push(clause);
  });

  return (
    <div
      style={{
        maxWidth: "950px",
        margin: "auto",
        padding: "20px",
        fontFamily: "Arial, sans-serif"
      }}
    >
      <h1
        style={{
          textAlign: "center",
          marginBottom: "25px"
        }}
      >
        Legal Document Analyzer
      </h1>

      <div
        style={{
          display: "flex",
          gap: "10px",
          marginBottom: "20px"
        }}
      >
        <input
          type="file"
          onChange={(e) =>
            setFile(e.target.files[0])
          }
        />

        <button
          onClick={handleUpload}
          style={{
            padding: "8px 16px",
            border: "none",
            borderRadius: "6px",
            background: "#1677ff",
            color: "#fff",
            cursor: "pointer"
          }}
        >
          Upload
        </button>
      </div>

      <hr />

      {results?.document_summary && (
        <div
          style={{
            background: "#fff",
            padding: "18px",
            borderRadius: "10px",
            marginTop: "20px",
            marginBottom: "25px",
            boxShadow:
              "0 2px 8px rgba(0,0,0,0.08)"
          }}
        >
          <h2 style={{ marginBottom: "10px" }}>
            Document Summary
          </h2>

          <p style={{ fontSize: "18px" }}>
            <strong>
              {
                results.document_summary
                  .document_type
              }
            </strong>

            {" "}

            (
            {Math.round(
              results.document_summary
                .confidence * 100
            )}
            %
            )
          </p>

          {results.document_summary
            ?.detected_labels && (
            <div style={{ marginTop: "15px" }}>
              <strong>
                Detected Categories:
              </strong>

              <div
                style={{
                  marginTop: "10px"
                }}
              >
                {Object.entries(
                  results.document_summary
                    .detected_labels
                ).map(
                  ([label, count]) => (
                    <span
                      key={label}
                      style={{
                        display: "inline-block",
                        background:
                          "#f5f5f5",
                        padding:
                          "6px 10px",
                        borderRadius: "6px",
                        marginRight: "8px",
                        marginBottom: "8px",
                        fontSize: "13px"
                      }}
                    >
                      <strong>
                        {label}
                      </strong>

                      {" "}

                      ({count})
                    </span>
                  )
                )}
              </div>
            </div>
          )}
        </div>
      )}

      {results?.clauses?.length > 0 && (
        <div style={{ marginTop: "20px" }}>
          <h2>Analysis Results</h2>

          {Object.entries(
            groupedClauses
          ).map(
            ([group, clauses]) => (
              <div
                key={group}
                style={{
                  marginTop: "30px"
                }}
              >
                <h3
                  style={{
                    marginBottom: "15px",
                    paddingBottom: "8px",
                    borderBottom:
                      "2px solid #f0f0f0"
                  }}
                >
                  {group}
                </h3>

                {clauses.map(
                  (item, index) => (
                    <ClauseCard
                      key={index}
                      data={item}
                    />
                  )
                )}
              </div>
            )
          )}
        </div>
      )}
    </div>
  );
}

export default App;