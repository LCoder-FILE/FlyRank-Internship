const API_BASE = "http://localhost:8000";

export async function triggerRun(graph, startNodeId) {
  const res = await fetch(`${API_BASE}/api/workflows/run`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ graph, startNodeId }),
  });
  if (!res.ok) throw new Error("Failed to start run");
  return res.json(); // { runId }
}

export async function getRun(runId) {
  const res = await fetch(`${API_BASE}/api/workflows/run/${runId}`);
  if (!res.ok) throw new Error("Failed to fetch run status");
  return res.json(); // { status, history, error? }
}