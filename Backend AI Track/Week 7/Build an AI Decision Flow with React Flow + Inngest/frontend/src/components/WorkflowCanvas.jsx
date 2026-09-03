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

  return (
    <div className="w-full h-screen relative">
      <div className="absolute top-4 left-4 z-10 flex gap-2">
        <Button onClick={addNode}>+ Add Node</Button>
      </div>
      <ReactFlow
        nodes={nodesWithHandlers}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
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