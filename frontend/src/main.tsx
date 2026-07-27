import React from "react";
import ReactDOM from "react-dom/client";
import "./styles.css";

type Attribution = { token: string; contribution: number; label: string };
type Evidence = { id: string; title: string; content: string; source?: string; relevance: number };
type Assessment = {
  assessment_id?: string;
  hallucination: boolean;
  confidence: number;
  reason: string;
  hallucination_score: number;
  semantic_similarity: number;
  evidence: Evidence[];
  explanation: { summary: string; supported_claims: string[]; unsupported_claims: string[]; token_attributions: Attribution[]; method: string };
};

const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000/api/v1";

function App(): React.JSX.Element {
  const [question, setQuestion] = React.useState("What is the capital of France?");
  const [answer, setAnswer] = React.useState("Paris is the capital and most populous city of France.");
  const [context, setContext] = React.useState("Paris is the capital and most populous city of France.");
  const [assessment, setAssessment] = React.useState<Assessment | null>(null);
  const [error, setError] = React.useState("");
  const [loading, setLoading] = React.useState(false);

  async function assess(): Promise<void> {
    setLoading(true);
    setError("");
    try {
      const response = await fetch(`${API_URL}/check`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question, answer, context: context ? [context] : [] }),
      });
      if (!response.ok) throw new Error(`Assessment failed (${response.status}).`);
      setAssessment((await response.json()) as Assessment);
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Unexpected assessment error.");
    } finally {
      setLoading(false);
    }
  }

  const score = assessment ? Math.round(assessment.hallucination_score * 100) : 0;
  return (
    <main className="shell">
      <header className="hero">
        <p className="eyebrow">Evidence-grounded LLM evaluation</p>
        <h1>TRUTHLENS</h1>
        <p>Detect unsupported claims, inspect evidence, and compare answers under identical prompts.</p>
      </header>
      <section className="workspace" aria-label="Hallucination assessment workspace">
        <div className="card form-card">
          <label>Question<textarea value={question} onChange={(event) => setQuestion(event.target.value)} /></label>
          <label>LLM answer<textarea value={answer} onChange={(event) => setAnswer(event.target.value)} /></label>
          <label>Trusted context <span>(optional)</span><textarea value={context} onChange={(event) => setContext(event.target.value)} /></label>
          <button onClick={() => void assess()} disabled={loading || !question.trim() || !answer.trim()}>
            {loading ? "Assessing…" : "Analyze answer"}
          </button>
          {error && <p className="error" role="alert">{error}</p>}
        </div>
        <div className="card results-card">
          {!assessment ? <p className="empty">Submit an answer to generate an evidence-grounded assessment.</p> : <>
            <div className="score-row">
              <div className={`score ${assessment.hallucination ? "risk" : "clear"}`} style={{ "--score": `${score}%` } as React.CSSProperties}>
                <strong>{score}</strong><span>risk score</span>
              </div>
              <div><p className="eyebrow">{assessment.hallucination ? "Potential hallucination" : "Evidence supported"}</p><h2>{assessment.confidence}% confidence</h2><p>{assessment.reason}</p></div>
            </div>
            <dl className="metrics"><div><dt>Semantic similarity</dt><dd>{Math.round(assessment.semantic_similarity * 100)}%</dd></div><div><dt>Evidence passages</dt><dd>{assessment.evidence.length}</dd></div></dl>
            <h3>Explanation</h3><p>{assessment.explanation.summary}</p>
            <div className="token-groups"><p><b>Supported:</b> {assessment.explanation.supported_claims.join(", ") || "None"}</p><p><b>Needs evidence:</b> {assessment.explanation.unsupported_claims.join(", ") || "None"}</p></div>
            <h3>Evidence</h3>
            {assessment.evidence.map((item) => <article className="evidence" key={item.id}><b>{item.title}</b><p>{item.content}</p>{item.source && <a href={item.source} target="_blank" rel="noreferrer">Source ↗</a>}</article>)}
          </>}
        </div>
      </section>
      <footer>Baseline detector · Evidence-grounded token attribution · Do not use as the sole source for high-stakes decisions.</footer>
    </main>
  );
}

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode><App /></React.StrictMode>,
);
