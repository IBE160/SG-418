# Architecture Decision Document: AIES - AI Economy Simulator

## 1. Executive Summary
The architecture for AIES is designed for **simplicity and observability**. It employs a split-stack approach with a **FastAPI** backend serving as the central simulation engine and a **Next.js** frontend as the command center. The system prioritizes research validity by isolating agent logic (preventing information leakage) and robust error handling (preventing LLM failures from crashing the simulation). By eschewing complex databases and real-time sockets in favor of in-memory state and HTTP polling, the architecture remains lightweight and easy to maintain for the MVP.

## 2. Project Initialization

### Frontend Setup
```bash
npx create-next-app@latest frontend --typescript --tailwind --eslint
# Select: App Router, No 'src' directory (optional, but structure implies it), Import alias '@/*'
cd frontend
npx shadcn-ui@latest init
# Select: Slate, CSS Variables, Default config
```

### Backend Setup
```bash
# Install uv if not present
curl -LsSf https://astral.sh/uv/install.sh | sh

mkdir backend && cd backend
uv init
uv add fastapi uvicorn pydantic pydantic-ai google-generativeai python-dotenv
```

## 3. Decision Summary Table

| Category | Decision | Version | Affects | Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **Communication** | HTTP Short Polling | HTTP/1.1 | Dashboard | Simple to implement, sufficient for 1-5s tick rates. |
| **State** | In-Memory Singleton | Python Global | Engine | Fast, no DB overhead, fits MVP "session-based" model. |
| **Isolation** | "Blind" Interface | Custom | Agents | Prevents cheating; ensures agents act only on perceived info. |
| **Error Handling** | "Penalty Box" | Custom | All | Agent skips turn on error; prevents simulation crash. |
| **Output** | Pydantic-AI | v0.0.1+ | LLM | Enforces strict JSON output from LLMs for reliability. |

## 4. Project Structure

```
/project-root/
├── backend/                  # The Brain (FastAPI + Python)
│   ├── app/
│   │   ├── agents/           # Agent Logic
│   │   │   ├── base.py       # Abstract Base Class
│   │   │   └── implementation.py # Gemini Agent
│   │   ├── core/             # Simulation Engine
│   │   │   ├── engine.py     # Main Loop
│   │   │   └── state.py      # Global State
│   │   ├── models/           # Data Models
│   │   │   ├── api.py        # DTOs
│   │   │   └── domain.py     # Simulation Objects
│   │   ├── main.py           # App Entry & Routes
│   ├── pyproject.toml        # Dependencies
│   └── .env                  # API Keys
├── frontend/                 # The Command Center (Next.js)
│   ├── src/
│   │   ├── components/
│   │   │   ├── ui/           # shadcn components
│   │   │   └── dashboard/    # Custom visualizations
│   │   ├── lib/              # API Client
│   │   ├── app/              # Pages
│   ├── package.json
│   └── tailwind.config.ts
```

## 5. Functional Requirement Mapping

| FR Category | Component | Description |
| :--- | :--- | :--- |
| **FR1: Config** | `backend/models/domain.py` | Pydantic models define the exact shape of valid configuration. |
| **FR2: Agents** | `backend/agents/` | `pydantic-ai` ensures LLMs return valid `TradeOffer` objects. |
| **FR3: Monitor** | `frontend/app/page.tsx` | Polling hook fetches `GET /state` every X seconds. |
| **FR4: Export** | `backend/api/export` | Endpoint dumps the in-memory Event Log list to CSV. |

## 6. Technology Stack Details

*   **Frontend:** Next.js 14 (App Router), TypeScript 5, TailwindCSS, Recharts, Lucide React.
*   **Backend:** Python 3.12, FastAPI, Uvicorn, Pydantic v2.
*   **AI:** Pydantic-AI (wrapping Google GenAI SDK).
*   **Dev Tools:** `uv` (Python package manager), `npm` (JS package manager).

## 7. Integration Points

*   **Frontend-Backend:** REST API over HTTP/1.1.
*   **Backend-LLM:** `pydantic-ai` calls to Google Gemini API.
*   **State-Persistence:** None (In-memory). Export to CSV for persistence.

## 8. Implementation Patterns & Consistency Rules

### Naming Conventions
*   **Python:** `snake_case` for variables/functions. Classes are `PascalCase`.
*   **TypeScript:** `camelCase` for variables/functions. Components/Interfaces are `PascalCase`.
*   **API:** JSON keys are `camelCase` (Backend automatically converts).

### Code Organization
*   **Feature Folding:** Keep related things close. The "Agent Card" component and its specific types live together.
*   **Type Sharing:** We DO NOT share code between languages. We manually keep the TS Interfaces and Python Models in sync (MVP trade-off for simplicity).

### Error Handling
*   **Backend:** Catch all unhandled exceptions in `main.py` middleware. Return 500.
*   **Agents:** Catch `ValidationError` from Pydantic-AI. Log it. Agent does `Action.WAIT`.
*   **Frontend:** If API fails, show a toast notification "Connection Lost" but keep the old data visible.

## 9. Data Architecture

*   **Models:**
    *   `Agent`: id, job, inventory (dict), needs (dict), last_action.
    *   `WorldState`: day, time, agents (list), market_history (list).
    *   `Transaction`: buyer_id, seller_id, resource, amount, price, tick.
*   **Relationships:**
    *   Agents belong to WorldState.
    *   Transactions belong to WorldState (global log).
*   **Persistence:** In-memory lists.

## 10. API Contracts

*   `GET /api/state` -> `200 OK` (Returns `WorldState`)
*   `POST /api/config` -> `200 OK` (Accepts `SimulationConfig`)
*   `POST /api/control/start` -> `200 OK`
*   `POST /api/control/stop` -> `200 OK`
*   `GET /api/export` -> `200 OK` (Returns `text/csv`)

## 11. Security Architecture

*   **Authentication:** None (Internal Research Tool).
*   **Input Validation:** Strict Pydantic validation on all `POST` bodies.
*   **CORS:** Configured to allow requests ONLY from the specific Frontend origin (e.g., `http://localhost:3000`).

## 12. Deployment Architecture

*   **Frontend:** Vercel (Zero config).
*   **Backend:** Containerized (Docker). Deploy to Render or Fly.io.
*   **Environment Variables:** `GEMINI_API_KEY` (Backend), `NEXT_PUBLIC_API_URL` (Frontend).

## 13. Development Environment

### Prerequisites
*   Node.js 18+
*   Python 3.12+
*   Google Gemini API Key

### Setup Commands
```bash
# Backend
cd backend
uv sync
echo "GEMINI_API_KEY=..." > .env
uv run uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

---
*Generated by BMAD Architecture Workflow*