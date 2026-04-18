import { useState } from "react"

const API = "http://localhost:8000"

export default function App() {
  const [token, setToken] = useState("")
  const [repos, setRepos] = useState([])
  const [selectedRepo, setSelectedRepo] = useState(null)
  const [dockerfile, setDockerfile] = useState(null)
  const [loading, setLoading] = useState(false)
  const [step, setStep] = useState(1)

  function connectGithub() {
    window.open(API + "/api/auth/login", "_blank")
    setStep(2)
  }

  async function loadRepos() {
    if (!token) return
    setLoading(true)
    const res = await fetch(API + "/api/auth/repos?access_token=" + token)
    const data = await res.json()
    setRepos(data.repos)
    setLoading(false)
    setStep(3)
  }

async function generateDockerfile() {
    if (!selectedRepo || !token) return
    setLoading(true)
    setDockerfile(null)
    const res = await fetch(
      API + "/api/analyze-github?access_token=" + encodeURIComponent(token) +
      "&repo_full_name=" + encodeURIComponent(selectedRepo),
      { method: "POST" }
    )
    const data = await res.json()
    
    if (data.error) {
      alert(data.error)
      setLoading(false)
      return
    }
    
    setDockerfile(data)
    setLoading(false)
  }

  function copyDockerfile() {
    navigator.clipboard.writeText(dockerfile.dockerfile)
  }

  return (
    <div style={styles.app}>
      <div style={styles.logo}>dockerfile <span style={styles.logoAccent}>generator</span></div>
      <h1 style={styles.heading}>Generate your Dockerfile</h1>
      <p style={styles.subtitle}>Connect GitHub, pick a repo, get a production-ready Dockerfile.</p>

      <div style={styles.step}>
        <div style={styles.stepLabel}>01 — connect github</div>
        <button style={styles.btn} onClick={connectGithub}>Connect with GitHub</button>
      </div>

      {step >= 2 && (
        <div style={styles.step}>
          <div style={styles.stepLabel}>02 — paste your token</div>
          <div style={styles.row}>
            <input
              style={styles.input}
              type="password"
              placeholder="gho_xxxxxxxxxxxx"
              value={token}
              onChange={e => setToken(e.target.value)}
            />
            <button style={styles.btn} onClick={loadRepos}>Load repos</button>
          </div>
        </div>
      )}

      {step >= 3 && (
        <div style={styles.step}>
          <div style={styles.stepLabel}>03 — pick a repo</div>
          <div style={styles.repoGrid}>
            {repos.map(repo => (
              <div
                key={repo.full_name}
                style={{
                  ...styles.repoCard,
                  ...(selectedRepo === repo.full_name ? styles.repoCardSelected : {})
                }}
                onClick={() => setSelectedRepo(repo.full_name)}
              >
                <div style={styles.repoName}>{repo.name}</div>
                <div style={styles.repoLang}>{repo.language || "unknown"}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {selectedRepo && (
        <div style={styles.step}>
          <button style={styles.btn} onClick={generateDockerfile} disabled={loading}>
            {loading ? "Generating..." : "Generate Dockerfile"}
          </button>
        </div>
      )}

      {dockerfile && (
        <div style={styles.resultBox}>
          <div style={styles.resultHeader}>
            <div style={styles.resultMeta}>
              {dockerfile.language && <span style={styles.badge}>{dockerfile.language}</span>}
              {dockerfile.framework && <span style={styles.badge}>{dockerfile.framework}</span>}
            </div>
            <button style={styles.copyBtn} onClick={copyDockerfile}>copy</button>
          </div>
          <pre style={styles.pre}>{dockerfile.dockerfile}</pre>
        </div>
      )}
    </div>
  )
}

const styles = {
  app: { maxWidth: 720, margin: "0 auto", padding: "2rem 1.5rem", fontFamily: "monospace" },
  logo: { fontSize: 13, fontWeight: 500, color: "#888", letterSpacing: "0.08em", textTransform: "uppercase", marginBottom: "2.5rem" },
  logoAccent: { color: "#111" },
  heading: { fontSize: 22, fontWeight: 500, marginBottom: "0.5rem", color: "#111" },
  subtitle: { fontSize: 14, color: "#888", marginBottom: "2rem", lineHeight: 1.6 },
  step: { marginBottom: "1.5rem" },
  stepLabel: { fontSize: 11, fontWeight: 500, color: "#aaa", letterSpacing: "0.1em", textTransform: "uppercase", marginBottom: "0.5rem" },
  btn: { padding: "10px 20px", border: "0.5px solid #ddd", borderRadius: 8, background: "#fff", color: "#111", fontSize: 13, cursor: "pointer", fontFamily: "monospace" },
  row: { display: "flex", gap: 8 },
  input: { flex: 1, padding: "10px 12px", border: "0.5px solid #ddd", borderRadius: 8, background: "#fff", color: "#111", fontSize: 13, fontFamily: "monospace" },
  repoGrid: { display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(180px, 1fr))", gap: 8 },
  repoCard: { padding: "10px 14px", border: "0.5px solid #ddd", borderRadius: 8, cursor: "pointer" },
  repoCardSelected: { border: "0.5px solid #111", background: "#f9f9f9" },
  repoName: { fontSize: 13, fontWeight: 500, color: "#111", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" },
  repoLang: { fontSize: 11, color: "#aaa", marginTop: 3 },
  resultBox: { border: "0.5px solid #ddd", borderRadius: 8, overflow: "hidden", marginTop: "1.5rem" },
  resultHeader: { display: "flex", justifyContent: "space-between", alignItems: "center", padding: "10px 14px", borderBottom: "0.5px solid #ddd", background: "#f9f9f9" },
  resultMeta: { display: "flex", gap: 6 },
  badge: { fontSize: 11, padding: "2px 8px", border: "0.5px solid #ddd", borderRadius: 6, color: "#666" },
  copyBtn: { fontSize: 12, padding: "5px 12px", border: "0.5px solid #ddd", borderRadius: 6, background: "#fff", color: "#666", cursor: "pointer", fontFamily: "monospace" },
  pre: { padding: "1rem", fontSize: 12, lineHeight: 1.7, color: "#111", overflowX: "auto", background: "#fff", whiteSpace: "pre", fontFamily: "monospace" },
}