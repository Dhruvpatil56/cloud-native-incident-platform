import { useQuery } from "@tanstack/react-query";
import { useParams, useNavigate } from "react-router-dom";
import { fetchIncident, submitRca, transitionState } from "../api/client";
import { RcaForm } from "../components/RcaForm";
import { SeverityBadge } from "../components/SeverityBadge";
import { StateBadge } from "../components/StateBadge";

export function IncidentDetail() {
  const { id = "" } = useParams();
  const navigate = useNavigate();
  const { data, refetch } = useQuery({
    queryKey: ["incident", id],
    queryFn: () => fetchIncident(id),
  });

  if (!data) return (
    <main>
      <div className="loading">Loading incident...</div>
    </main>
  );

  return (
    <main>
      <button className="back-btn" onClick={() => navigate("/")}>← Back to Dashboard</button>

      <div className="incident-header">
        <div className="incident-title-row">
          <h1>{data.title}</h1>
          <SeverityBadge severity={data.severity} />
        </div>
        <div className="incident-meta">
          <StateBadge state={data.state} />
          <span className="meta-item">📦 {data.component}</span>
          <span className="meta-item">🕐 {new Date(data.created_at).toLocaleString()}</span>
          {data.mttr_seconds && (
            <span className="meta-item mttr">⚡ MTTR: {Math.round(data.mttr_seconds / 60)} min</span>
          )}
        </div>
        <p className="incident-description">{data.description}</p>
      </div>

      {(data as any).ai_analysis && (
        <div className="ai-analysis-card">
          <div className="ai-analysis-header">
            <span className="ai-icon">🤖</span>
            <h2>AI Analysis</h2>
            <span className="ai-badge">Powered by Groq</span>
          </div>
          <div className="ai-analysis-content">
            {(data as any).ai_analysis.split('\n').map((line: string, i: number) => {
              if (line.startsWith('### ')) return <h3 key={i} className="ai-section-title">{line.replace('### ', '')}</h3>;
              if (line.startsWith('- ')) return <li key={i} className="ai-list-item">{line.replace('- ', '')}</li>;
              if (line.trim() === '') return <br key={i} />;
              return <p key={i} className="ai-text">{line}</p>;
            })}
          </div>
        </div>
      )}

      {!(data as any).ai_analysis && (
        <div className="ai-analysis-card ai-pending">
          <div className="ai-analysis-header">
            <span className="ai-icon">🤖</span>
            <h2>AI Analysis</h2>
            <span className="ai-badge pending">Analyzing...</span>
          </div>
          <p className="ai-pending-text">AI analysis is being generated for this incident.</p>
        </div>
      )}

      <div className="incident-details-grid">
        <div className="detail-card">
          <h3>Root Cause</h3>
          <p>{data.root_cause}</p>
        </div>
        <div className="detail-card">
          <h3>RCA Description</h3>
          <p>{(data as any).rca_description}</p>
        </div>
      </div>

      <div className="rca-section">
        <h2>Submit RCA</h2>
        <RcaForm
          onSubmit={async (payload) => {
            await submitRca(id, payload);
            await refetch();
          }}
        />
      </div>
    </main>
  );
}
