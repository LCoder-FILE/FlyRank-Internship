# Progress — Visual AI Workflow System

Stack: **React (JavaScript) + React Flow + Shadcn** frontend · **FastAPI + Inngest (Python) + OpenAI SDK** backend
Repo: **[ link ]**

---

## Phase 1 — Setup (~1h)
**Goal:** Initialize the project and prepare the development environment.

- [x] Frontend: React app created (Vite + React, JavaScript)
- [x] Frontend deps installed: `reactflow`, `shadcn/ui` (+ Tailwind)
- [x] Backend: FastAPI app created
- [x] Backend deps installed: `inngest`, `openai`
- [x] Environment variables configured (`.env` — `OPENAI_API_KEY`, etc.)
- [x] Basic project structure in place (frontend/ + backend/ folders, or two repos)
- [x] Checkpoint — frontend running
- [x] Checkpoint — backend running
- [x] Checkpoint — Inngest Dev Server running, syncs with backend (no "Error" on Apps tab):
- [x] Repo initialized with README
- [x] Committed: `Phase 1: setup`

Notes:

- Access frontend : cd "Backend AI Track/Week 7/Build an AI Decision Flow with React Flow + Inngest/frontend"

- Access backend : cd "Backend AI Track/Week 7/Build an AI Decision Flow with React Flow + Inngest/backend"

to run : 

```cmd
cd "Backend AI Track/Week 7/Build an AI Decision Flow with React Flow + Inngest/frontend"
npm run dev 
```

---

## Phase 2 — Foundations (~2h)
**Goal:** Build the visual flow editor and graph structure.

- [x] React Flow canvas renders
- [x] Can add nodes (button / double-click / drag from palette)
- [x] Can connect nodes (drag edge between handles)
- [x] Can edit a node's prompt (inline text field or side panel)
- [x] Two edge types defined: **YES** path, **NO** path (visually distinguished — color/label)
- [x] Graph state stored locally (React state / localStorage / JSON in memory)
- [x] Checkpoint:
  - Added ≥3 nodes, connected with both YES/NO edges: **[yes]**
  - Edited a node's prompt and it persisted: **[yes]**
  - Screenshot of the flow editor:
    ![Phase 2 flow editor](./screenshot/Phase%202.png)

- [x] Committed: `Phase 2: flow editor + graph state`

Notes:

Frontend only phase

---

## Phase 3 — Build (core) (~2h)
**Goal:** Execute the workflow using Inngest and AI responses.

- [x] Each node maps to an Inngest step
- [x] Node prompt sent to an LLM (OpenAI)
- [x] Model constrained to return only `YES` or `NO`
- [x] Execution continues down the matching edge (YES → yes-node, NO → no-node)
- [x] Execution order tracked (list/log of visited nodes)
- [x] Checkpoint — example run:
  ```
  Prompt: "Is this a support request?"
  Input: [what you tested with]
  Result: YES / NO
  Path taken: [node -> node -> node]
  ```
  - Dashboard shows the run stepping through nodes: **[ yes/no ]**
- [x] Committed: `Phase 3: workflow execution via Inngest`

Notes:

TO RUN THE OLLAMA:

FlyRank-Internship>set CUDA_VISIBLE_DEVICES=-1

FlyRank-Internship>ollama list

NAME         ID              SIZE      MODIFIED    
gemma3:1b    8648f39daa8f    815 MB    2 weeks ago    

FlyRank-Internship>ollama serve

Error: listen tcp 127.0.0.1:11434: bind: Only one usage of each socket address (protocol/network address/port) is normally permitted.

FlyRank-Internship>tasklist | findstr ollama

ollama app.exe                6376 Console                    3     24,840 K
ollama.exe                   17676 Console                    3     33,896 K

FlyRank-Internship>taskkill /IM "ollama app.exe" /F

SUCCESS: The process "ollama app.exe" with PID 6376 has been terminated.


FlyRank-Internship>taskkill /IM ollama.exe /F

SUCCESS: The process "ollama.exe" with PID 17676 has been terminated.


FlyRank-Internship>ollama serve


TO RUN THE INNGEST:

npx inngest-cli@latest dev -u http://localhost:8000/api/inngest

---

## Phase 4 — Build (polish) (~2h)
**Goal:** Improve usability and developer experience. **Pick at least 3:**

- [ ] Visual execution state (highlight active/visited nodes)
- [ ] Execution logs panel
- [ ] Save/load workflows
- [ ] JSON export/import
- [ ] Better node styling
- [ ] Error handling
- [ ] Retry failed nodes
- [ ] Animated active edges
- [ ] Execution history

For each chosen item:
- **[ item ]** — what you built:
  > [notes]
- **[ item ]** — what you built:
  > [notes]
- **[ item ]** — what you built:
  > [notes]

- [ ] Checkpoint — screenshot/gif of polished UI during a run
- [ ] Committed: `Phase 4: polish`

Notes:

---

## Final checklist
- [ ] Frontend runs and renders the flow editor
- [ ] Nodes can be added, connected (YES/NO), and edited
- [ ] Workflow executes end-to-end through Inngest
- [ ] Each node's AI call is constrained to YES/NO only
- [ ] Execution correctly branches based on the AI's answer
- [ ] At least 3 polish features implemented
- [ ] README explains setup + how to run both frontend and backend
- [ ] Repo public with meaningful commits per phase