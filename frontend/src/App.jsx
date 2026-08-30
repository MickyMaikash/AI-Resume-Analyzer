import { useRef, useState } from 'react'
import './App.css'
import Loading from './loading'
function App() {
  let [file, setfiles] = useState(null)
  let [jobDescription, setJobDescription] = useState("")
  let [result, setResult] = useState(null)
  const url = "http://127.0.0.1:8000/analyze"
  let [loading, setResultloading] = useState(false)

  let resultRef = useRef(null)
  function callApi() {
    if (!file) {
      alert("Please Enter valid pdf")
      return
    }

    if (jobDescription == "") {
      alert("job description should not empty")
      return
    }
    setResultloading(true)
    let formdata = new FormData()
    formdata.append("resume", file)
    formdata.append("job_des", jobDescription)
    fetch(url, {
      method: "POST",
      body: formdata
    })
      .then(async res => {
        return await res.json()
      })
      .then(res => {
        console.log(res)
        setResult(res)
        setResultloading(false)
        setTimeout(() => {
          resultRef.current?.scrollIntoView({
            behavior: "smooth",
            block: "start"
          });
        }, 100);
      })
      .catch(e => {
        console.log(e)
        setResultloading(false)
      })
  }


  return (
    <>
      <nav className="navbar">
        <div className="logo">
          Resume<span>AI</span>
        </div>
        <p>AI Resume Analyzer</p>
      </nav>
      {!result && !loading && (
        <section className="hero">
          <div className="hero-content">
            <div className="badge">
              ✨ AI-Powered Resume Analysis
            </div>
            <h1>
              Build a resume that
              <br />
              <span>gets noticed.</span>
            </h1>
            <p>
              Compare your resume with any job description,
              discover missing skills, and get AI-powered
              recommendations to improve your chances.
            </p>
          </div>

        </section>
      )}
      {loading && <Loading />}
      {!loading && (
        <section className="analyzer">
          <div className="analyzer-header">
            <h2>
              Analyze Your Resume
            </h2>
            <p>
              Upload your resume and paste the job description
              to get your personalized analysis.
            </p>
          </div>

          <div className="Main">
            <div
              id="PdfInput"
              onClick={() => document.getElementById("pdf").click()}>
              <div className="inputFG">
                <input
                  onChange={(e) => setfiles(e.target.files[0])}
                  id="pdf"
                  type="file"
                  accept=".pdf"
                />
                <div className="uploadIcon">↑</div>
                <h3>
                  {file ? file.name : "Upload your resume"}
                </h3>
                <p>
                  {file
                    ? "PDF selected successfully"
                    : "Click anywhere here to choose a PDF file"}
                </p>
              </div>
            </div>

            <div className="job">
              <div className="job-header">
                <h3>
                  Job Description
                </h3>
                <span>
                  Required
                </span>
              </div>

              <textarea
                onChange={(e) =>
                  setJobDescription(p => e.target.value)
                }
                id="jobDes"
                placeholder="Paste the job description here..."
              />
              <button onClick={callApi}>
                Analyze Resume →
              </button>
            </div>
          </div>
          <div className="features">
            <div className="feature">
              <div className="feature-icon">
                📊
              </div>
              <div>
                <h3>Match Score</h3>
                <p>
                  See how closely your resume matches the role.
                </p>
              </div>
            </div>

            <div className="feature">
              <div className="feature-icon">
                🎯
              </div>
              <div>
                <h3>Missing Skills</h3>
                <p>
                  Discover skills that could improve your match.
                </p>
              </div>
            </div>

            <div className="feature">
              <div className="feature-icon">
                💡
              </div>
              <div>
                <h3>AI Suggestions</h3>
                <p>
                  Get actionable recommendations for your resume.
                </p>
              </div>
            </div>
          </div>

        </section>
      )}

      {result && (
        <section ref={resultRef} className="result">
          <div className="result-header">
            <div>
              <span className="result-label">
                ANALYSIS COMPLETE
              </span>
              <h2>
                Resume Analysis
              </h2>
              <p>
                Here's how your resume matches the job description.
              </p>
            </div>
            <button
              className="analyze-again"
              onClick={() => window.location.reload()}
            >
              Analyze Another
            </button>
          </div>

          <div className="match">
            <div>
              <h3>
                Overall Match
              </h3>
              <p>
                Resume compatibility with this job
              </p>
            </div>
            <div className="percentage">
              {result.overall_match_percentage}%
            </div>
          </div>

          <div className="section">
            <h3>
              <span>✓</span>
              Matched Skills
            </h3>
            <div className="tags">
              {result.matched_skills_and_requirements.map(
                (skill, index) => (

                  <span
                    className="tag matched"
                    key={index}
                  >
                    {skill}
                  </span>

                )
              )}
            </div>
          </div>

          <div className="section">
            <h3>
              <span>!</span>
              Missing Skills
            </h3>
            <div className="tags">
              {result.missing_skills_and_requirements.map(
                (skill, index) => (
                  <span
                    className="tag missing"
                    key={index}
                  >
                    {skill}
                  </span>
                )
              )}
            </div>
          </div>

          <div className="section">
            <h3>
              <span>✦</span>
              Recommended Keywords
            </h3>
            <div className="tags">
              {result.recommended_keywords.map(
                (keyword, index) => (
                  <span
                    className="tag recommended"
                    key={index}
                  >
                    {keyword}
                  </span>
                )
              )}
            </div>
          </div>


          <div className="section">
            <h3>
              <span>◆</span>
              Relevant Experience & Projects
            </h3>
            <ul>
              {result.relevant_experience_and_projects.map(
                (project, index) => (
                  <li key={index}>
                    {project}
                  </li>
                )
              )}
            </ul>
          </div>


          <div className="section">
            <h3>
              <span>↗</span>
              Skills to Learn
            </h3>
            <div className="tags">
              {result.skills_to_learn.map(
                (skill, index) => (
                  <span
                    className="tag learn"
                    key={index}
                  >
                    {skill}
                  </span>
                )
              )}
            </div>
          </div>

          <div className="section suggestions">
            <h3>
              <span>💡</span>
              Suggestions
            </h3>

            <ul>
              {result.specific_suggestions.map(
                (suggestion, index) => (

                  <li key={index}>
                    {suggestion}
                  </li>

                )
              )}
            </ul>
          </div>
        </section>

      )}

    </>
  );

}

export default App
