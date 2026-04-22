import { useState } from "react";
import ClauseCard from "./components/ClauseCard";

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState([]);

  const handleUpload = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://127.0.0.1:8000/upload", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      setResult(data.analysis);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div style={{
      maxWidth: "800px",
      margin: "auto",
      padding: "20px"
      }}>
      <h1 style={{ textAlign: "center" }}>
        Legal Document Analyzer
      </h1>

      <input
        type="file"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <button onClick={handleUpload}>Upload</button>

      <hr />

      {result.length > 0 && (
      <div style={{ marginTop: "20px" }}>
        <h2>Analysis Results</h2>

        {result.map((item, index) => (
          <ClauseCard key={index} data={item} />
        ))}
      </div>
      )}
    </div>
  );
}

export default App;