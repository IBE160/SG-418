# Project Structure

```
/home/eirik/ibe160/SG-418/
├── backend/                  # The Brain (FastAPI + Python)
│   ├── app/
│   │   ├── agents/           # Agent Logic (The Personalities)
│   │   │   ├── base.py       # The "Blind" Interface
│   │   │   └── profiles/     # Different Agent Types
│   │   ├── core/             # Core Engine
│   │   │   ├── engine.py     # The Simulation Loop
│   │   │   └── state.py      # The World State (Singleton)
│   │   ├── models/           # Data Shapes (Pydantic)
│   │   │   ├── api.py        # API Req/Res models
│   │   │   └── domain.py     # Internal Simulation models
│   │   ├── api/              # The Nervous System (Endpoints)
│   │   │   └── routes.py     # Connects Frontend to Engine
│   │   └── main.py           # Application Entry Point
│   ├── pyproject.toml        # Python Dependencies (uv)
│   └── README.md
├── frontend/                 # The Face (Next.js)
│   ├── src/
│   │   ├── components/       # UI Building Blocks (shadcn)
│   │   │   ├── ui/           # Buttons, Cards, Inputs
│   │   │   └── features/     # Dashboard, AgentGraph
│   │   ├── lib/              # Utilities
│   │   │   └── api.ts        # API Client (The Fetcher)
│   │   ├── app/              # Pages/Routes
│   │   │   ├── page.tsx      # Dashboard
│   │   │   └── layout.tsx    # Global Layout
│   │   └── types/            # TypeScript Definitions
│   ├── package.json          # JS Dependencies
│   ├── tailwind.config.ts    # Styling Config
│   └── README.md
└── README.md                 # Project Root Documentation
```

**Mapping Epics to Boundaries:**
*   **Simulation Engine:** Lives in `backend/app/core`
*   **Agent Logic:** Lives in `backend/app/agents`
*   **Dashboard:** Lives in `frontend/src/app/page.tsx` + `frontend/src/components/features`
