import React, { useState } from "react";
import axios from "axios";

function UploadForm() {
  const [file, setFile] = useState(null);
  const [summary, setSummary] = useState("");
  const [quiz, setQuiz] = useState("");
  const [pdfPath, setPdfPath] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return;

    setLoading(true);
    setSummary("");
    setQuiz("");
    setPdfPath("");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post("http://localhost:5000/upload", formData);
      setSummary(response.data.summary);
      setQuiz(response.data.quiz);
      setPdfPath(response.data.pdf);
    } catch (error) {
      alert("Error uploading file or generating summary.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input
          type="file"
          accept=".pdf"
          onChange={(e) => setFile(e.target.files[0])}
        />
        <button type="submit" disabled={!file || loading}>
          {loading ? "Processing..." : "Generate Summary"}
        </button>
      </form>

      {summary && (
        <div style={{ marginTop: "20px" }}>
          <h3>📝 Summary:</h3>
          <pre>{summary}</pre>
        </div>
      )}

      {quiz && (
        <div style={{ marginTop: "20px" }}>
          <h3>🧠 Quiz:</h3>
          <pre>{quiz}</pre>
        </div>
      )}

      {pdfPath && (
        <div style={{ marginTop: "20px" }}>
          <a
            href={`http://localhost:5000/download?path=${encodeURIComponent(pdfPath)}`}
            download
          >
            📥 Download PDF
          </a>
        </div>
      )}
    </div>
  );
}
export default UploadForm;