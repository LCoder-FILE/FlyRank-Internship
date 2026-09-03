import { useState } from "react";
import { Handle, Position } from "reactflow";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";

export default function DecisionNode({ id, data }) {
  const [prompt, setPrompt] = useState(data.prompt || "");

  const handleBlur = () => {
    data.onPromptChange?.(id, prompt);
  };

  return (
    <Card className="w-64 border-2 shadow-sm">
      <CardHeader className="py-2 px-3 flex flex-row items-center justify-between">
        <span className="text-xs font-medium text-muted-foreground">
          Decision Node
        </span>
        <Badge variant="outline" className="text-[10px]">{id}</Badge>
      </CardHeader>
      <CardContent className="p-3 pt-0">
        <Textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          onBlur={handleBlur}
          placeholder="Ask a yes/no question…"
          className="text-sm min-h-[60px] resize-none nodrag"
        />
      </CardContent>

      {/* Input */}
      <Handle type="target" position={Position.Top} className="!bg-slate-400" />

      {/* Two labeled outputs */}
      <div className="flex justify-between px-3 pb-2 text-xs font-medium">
        <span className="text-emerald-600">YES</span>
        <span className="text-rose-600">NO</span>
      </div>
      <Handle
        type="source"
        position={Position.Bottom}
        id="yes"
        style={{ left: "25%" }}
        className="!bg-emerald-500"
      />
      <Handle
        type="source"
        position={Position.Bottom}
        id="no"
        style={{ left: "75%" }}
        className="!bg-rose-500"
      />
    </Card>
  );
}