import "./loading.css"
function Loading() {
  return (
    <div className="loading-overlay">
      <div className="loading-card">

        <div className="loader">
          <div className="loader-ring"></div>
          <div className="loader-dot"></div>
        </div>

        <h2>Analyzing Resume</h2>

        <p>
          AI is comparing your resume with the job description...
        </p>

        <div className="loading-bar">
          <div className="loading-progress"></div>
        </div>

      </div>
    </div>
  );
}

export default Loading;