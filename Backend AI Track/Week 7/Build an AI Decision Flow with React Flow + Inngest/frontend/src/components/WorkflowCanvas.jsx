import { useCallback, useMemo, useState, useEffect } from "react";
import ReactFlow, {
  Background,
  Controls,
  MiniMap,
  addEdge,
  applyNodeChanges,
  applyEdgeChanges,
  MarkerType,
} from "reactflow";
import "reactflow/dist/style.css";
import DecisionNode from "@/nodes/DecisionNode";
import { Button } from "@/components/ui/button";
import { triggerRun, getRun } from "@/lib/api";

const STORAGE_KEY = "ai-workflow-graph";

const edgeStyle = (branch) => ({
  stroke: branch === "yes" ? "#10b981" : "#f43f5e",
  strokeWidth: 2,
});

let idCounter = 1;
const nextId = () => `node-${idCounter++}`;

export default function WorkflowCanvas() {
  const [nodes, setNodes] = useState([]);
  const [edges, setEdges] = useState([]);
  const [runStatus, setRunStatus] = useState(null); // { status, history, error? }
  const nodeTypes = useMemo(() => ({ decision: DecisionNode }), []);

  // Load saved graph on mount
  useEffect(() => {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) {
      const { nodes: n, edges: e } = JSON.parse(saved);
      setNodes(n);
      setEdges(e);
    } else {
      setNodes([
        {
          id: nextId(),
          type: "decision",
          position: { x: 250, y: 50 },
          data: { prompt: "Is this a support request?" },
        },
      ]);
    }
  }, []);

  // Persist on every change
  useEffect(() => {
    if (nodes.length === 0) return;
    localStorage.setItem(STORAGE_KEY, JSON.stringify({ nodes, edges }));
  }, [nodes, edges]);

  const onNodesChange = useCallback(
    (changes) => setNodes((nds) => applyNodeChanges(changes, nds)),
    []
  );
  const onEdgesChange = useCallback(
    (changes) => setEdges((eds) => applyEdgeChanges(changes, eds)),
    []
  );

  const onConnect = useCallback((connection) => {
    setEdges((eds) =>
      addEdge(
        {
          ...connection,
          style: edgeStyle(connection.sourceHandle),
          markerEnd: { type: MarkerType.ArrowClosed },
        },
        eds
      )
    );
  }, []);

  // Block a second edge coming out of the same yes/no handle
  const isValidConnection = useCallback(
    (connection) => {
      const alreadyUsed = edges.some(
        (e) =>
          e.source === connection.source &&
          e.sourceHandle === connection.sourceHandle
      );
      return !alreadyUsed;
    },
    [edges]
  );

  const onPromptChange = useCallback((id, prompt) => {
    setNodes((nds) =>
      nds.map((n) => (n.id === id ? { ...n, data: { ...n.data, prompt } } : n))
    );
  }, []);

  // Inject the callback into every node's data so DecisionNode can call it
  const nodesWithHandlers = nodes.map((n) => ({
    ...n,
    data: { ...n.data, onPromptChange },
  }));

  const addNode = () => {
    setNodes((nds) => [
      ...nds,
      {
        id: nextId(),
        type: "decision",
        position: { x: 250 + Math.random() * 200, y: 200 + nds.length * 120 },
        data: { prompt: "" },
      },
    ]);
  };

  // Start node = the one decision node with no incoming edge.
  // If multiple qualify, the first one found is used.
  const getStartNodeId = () => {
    const targets = new Set(edges.map((e) => e.target));
    const start = nodes.find((n) => !targets.has(n.id));
    return start?.id;
  };

  const runWorkflow = async () => {
    const startNodeId = getStartNodeId();
    if (!startNodeId) {
      alert("No start node found (every node has an incoming edge).");
      return;
    }

    const graph = {
      nodes: Object.fromEntries(nodes.map((n) => [n.id, n])),
      edges,
    };

    setRunStatus({ status: "running", history: [] });

    try {
      const { runId } = await triggerRun(graph, startNodeId);

      const poll = setInterval(async () => {
        const result = await getRun(runId);
        setRunStatus(result);
        if (result.status === "completed" || result.status === "failed") {
          clearInterval(poll);
        }
      }, 1000);
    } catch (err) {
      setRunStatus({ status: "failed", history: [], error: err.message });
    }
  };

  return (
    <div className="w-full h-screen relative">
      <div className="absolute top-4 left-4 z-10 flex gap-2">
        <Button onClick={addNode}>+ Add Node</Button>
        <Button
          onClick={runWorkflow}
          className="bg-emerald-600 hover:bg-emerald-700"
        >
          Run Workflow
        </Button>
      </div>

      {runStatus && (
        <div className="absolute top-4 right-4 z-10 w-72 bg-white border rounded-md shadow-md p-3 text-sm">
          <div className="font-medium mb-2">
            Status: <span className="capitalize">{runStatus.status}</span>
          </div>
          <ul className="space-y-1">
            {runStatus.history.map((h, i) => (
              <li key={i} className="flex justify-between gap-2">
                <span className="truncate">{h.nodeId}</span>
                <span
                  className={
                    h.decision === "YES" ? "text-emerald-600" : "text-rose-600"
                  }
                >
                  {h.decision}
                </span>
              </li>
            ))}
          </ul>
          {runStatus.error && (
            <p className="text-rose-600 mt-2 text-xs">{runStatus.error}</p>
          )}
        </div>
      )}

      <ReactFlow
        nodes={nodesWithHandlers}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        isValidConnection={isValidConnection}
        nodeTypes={nodeTypes}
        fitView
      >
        <Background gap={16} />
        <Controls />
        <MiniMap pannable zoomable />
      </ReactFlow>
    </div>
  );
}