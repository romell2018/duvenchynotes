import React from "react";
import UploadForm from "./UploadForm";

function App() {
  return (
    <div style={{ padding: "2rem", fontFamily: "Arial" }}>
      <h1>📚 Edu-AI Notes Summarizer</h1>
      <p>Upload a class PDF and get summarized notes + download as PDF.</p>
      <UploadForm />
    </div>
  );
}

export default App;
