# Epic Technical Specification: Foundation & Simulation Engine

Date: Monday, December 8, 2025
Author: BIP
Epic ID: 1
Status: Draft

---

## Overview

This epic establishes the fundamental technical infrastructure for the AI Economy Simulator (AIES). It focuses on setting up the split-stack environment (Next.js Frontend + FastAPI Backend), implementing the core in-memory simulation loop, and ensuring basic connectivity between the client and server. Success in this epic provides the necessary "runtime" for all future agent behaviors and user interactions.

## Objectives and Scope

### In-Scope
*   **Project Initialization:** Scaffolding the Next.js 14 frontend and FastAPI backend using `uv`.
*   **Core Engine:** Implementing the simulation loop (ticks, daily cycles) and time management.
*   **State Management:** Creating the centralized in-memory `WorldState` singleton.
*   **Basic Connectivity:** Establishing the REST API pattern and a "Health Check" verification.
*   **Environment Configuration:** Setting up `.env` handling and CORS policies.

### Out-of-Scope
*   **Agent Intelligence:** LLM integration and decision logic (Epic 3).
*   **Complex UI:** Dashboards, charts, or configuration forms (Epics 2 & 4).
*   **Persistence:** Database integration or file-based saving (State is in-memory only).
*   **Deployment:** Production build pipelines.

## System Architecture Alignment

This epic directly implements the "Simplicity and Observability" architectural vision:
*   **Component Structure:** Adheres to the `backend/` vs. `frontend/` directory separation.
*   **State Pattern:** Implements the **In-Memory Singleton** decision (`backend/core/state.py`) to avoid database overhead.
*   **Communication:** Establishes the **HTTP Short Polling** foundation (though full polling comes in Epic 4, the API client structure is set here).
*   **Tech Stack:** Enforces the use of **FastAPI** (Python 3.12+) and **Next.js 14** (TypeScript).

## Detailed Design

### Services and Modules

| Module/Service | Path | Responsibility | Owner |
| :--- | :--- | :--- | :--- |
| **App Entry** | `backend/main.py` | FastAPI app initialization, middleware (CORS), and route inclusion. | Backend |
| **Sim Engine** | `backend/core/engine.py` | Manages the game loop, advances time (`tick`), and resets daily counters. | Backend |
| **Global State** | `backend/core/state.py` | Defines and holds the singleton `WorldState` instance. | Backend |
| **Domain Models** | `backend/models/domain.py` | Pydantic models for `WorldState`, `SimulationConfig` (stub). | Backend |
| **API Client** | `frontend/lib/api.ts` | Typed fetch wrapper for communicating with the backend. | Frontend |
| **System Status** | `frontend/app/page.tsx` | Simple UI to display backend connectivity status. | Frontend |

### Data Models and Contracts

**WorldState (Singleton)**
```python
class WorldState(BaseModel):
    current_tick: int = 0
    current_day: int = 1
    is_running: bool = False
    last_updated: float = Field(default_factory=time.time)
    # Agents and Events to be added in future epics
```

### APIs and Interfaces

**Health Check**
*   **GET** `/health`
*   **Response:** `200 OK`
    ```json
    {
      "status": "online",
      "version": "0.1.0",
      "timestamp": "2025-12-08T10:00:00Z"
    }
    ```

**Get State (Internal Debug)**
*   **GET** `/api/state`
*   **Response:** `200 OK` (Returns full `WorldState` JSON)

### Workflows and Sequencing

**Server Start & Tick Loop**
1.  `main.py` starts `uvicorn` server.
2.  `lifespan` event initializes `WorldState`.
3.  Background task (if implemented now, or simple function call) triggers `engine.tick()`.
4.  `engine.tick()` increments `current_tick`.
5.  If `current_tick` % `ticks_per_day` == 0, increment `current_day` and reset agent budgets.

## Non-Functional Requirements

### Performance
*   **Startup Time:** Both servers should start in < 5 seconds locally.
*   **Loop Overhead:** The empty tick loop should execute in < 1ms.

### Security
*   **CORS:** Backend must strictly allow specific frontend origins (e.g., `http://localhost:3000`).
*   **Environment:** Sensitive config (if any) loaded via `.env`.

### Reliability/Availability
*   **Crash Safety:** Uncaught exceptions in the engine loop should be logged and not crash the main server process (though loop may stop).

### Observability
*   **Logging:** Server must emit structured logs to stdout (using `uvicorn` default logging is acceptable for MVP).
*   **Status:** Frontend clearly indicates if backend is unreachable.

## Dependencies and Integrations

*   **Python (Backend):**
    *   `fastapi` (Web Framework)
    *   `uvicorn` (ASGI Server)
    *   `pydantic` (Data Validation)
    *   `python-dotenv` (Config)
*   **Node.js (Frontend):**
    *   `next` (Framework)
    *   `react`, `react-dom`
    *   `lucide-react` (Icons)
    *   `shadcn-ui` components (Button, Card)

## Acceptance Criteria (Authoritative)

1.  **Project Structure:**
    *   Directory `frontend/` contains a runnable Next.js app.
    *   Directory `backend/` contains a runnable FastAPI app managed by `uv`.
2.  **Connectivity:**
    *   Visiting `http://localhost:3000` displays "System Status: Online" when backend is running.
    *   Displays "System Status: Offline" when backend is stopped.
3.  **State Persistence:**
    *   Restarting the backend resets the `WorldState` (confirming in-memory behavior).
    *   `GET /api/state` returns valid JSON structure.
4.  **Engine Logic:**
    *   Manually triggering a tick (or auto-tick) increases `current_tick` count in the state.
    *   Passing the day threshold increments `current_day`.

## Traceability Mapping

| Acceptance Criteria | Story | Component | Test Idea |
| :--- | :--- | :--- | :--- |
| **AC1 (Structure)** | 1.1 | Repo Root | Run `npm run dev` and `uv run start` |
| **AC2 (Connectivity)** | 1.4 | `frontend/page.tsx` | Kill backend and observe UI change |
| **AC3 (State)** | 1.3 | `backend/core/state.py` | Query API, restart server, query again |
| **AC4 (Engine)** | 1.2 | `backend/core/engine.py` | Call tick function and assert state change |

## Risks, Assumptions, Open Questions

*   **Assumption:** Developer has Python 3.12+ and Node.js 18+ installed.
*   **Risk:** Port conflicts (3000 or 8000 in use). *Mitigation:* Make ports configurable via env vars.
*   **Question:** Should the loop run in a separate thread or use `asyncio.sleep`? *Decision:* Use `asyncio.create_task` for the background loop in `main.py` lifespan.

## Test Strategy Summary

*   **Manual Verification:** Since this is setup-heavy, manual verification of the "Hello World" connectivity is the primary gate.
*   **Unit Tests:** Basic `pytest` for the `Engine` class to ensure time math is correct.
*   **Smoke Test:** "Green Lights" test—start both servers, verify no console errors, verify health endpoint.
