# Epic Technical Specification: Simulation Configuration Interface

Date: Monday, December 8, 2025
Author: BIP
Epic ID: 2
Status: Draft

---

## Overview

This epic focuses on enabling researchers to define the specific economic scenario they want to study. It involves building a user-friendly configuration interface in the frontend and the corresponding backend logic to initialize the simulation state. This is a critical prerequisite for running any meaningful experiments, as it moves the system from a hardcoded testbed to a configurable research platform.

## Objectives and Scope

### In-Scope
*   **Global Configuration UI:** Form inputs for simulation duration (days) and day length (seconds).
*   **Job & Resource UI:** Dynamic list interface to define available jobs (e.g., Woodcutter) and their output resources.
*   **Agent Configuration UI:** Interface to specify agent counts, assigned jobs, and behavioral traits (culture, needs).
*   **Backend Configuration Endpoint:** A unified API endpoint (`POST /api/config`) to validate and apply the full simulation setup.
*   **Simulation Controls:** Frontend controls and backend endpoints to Start, Stop, and Reset the simulation loop.
*   **Validation:** Strict validation of configuration consistency (e.g., agents must have valid job IDs).

### Out-of-Scope
*   **Saved Scenarios:** Persistence of configuration presets to disk/database (MVP is session-based).
*   **Hot-Swapping:** Changing configuration while a simulation is running (must stop/reset first).
*   **Advanced "Map" Generation:** Spatial or grid-based configuration (simulation is abstract/graph-based).

## System Architecture Alignment

This epic strictly adheres to the "Command Center" architecture defined in the Architecture Document.

*   **Frontend (Next.js + shadcn/ui):** Uses structured forms and client-side validation to build the `SimulationConfig` object. State is managed locally (or via Zustand) until submission.
*   **Backend (FastAPI + Pydantic):** Acts as the authority. The `WorldState` singleton is initialized *only* upon successful receipt of a valid `SimulationConfig` payload.
*   **Data Contract:** The `SimulationConfig` Pydantic model in the backend is the single source of truth for the configuration schema. The frontend must match this structure.

## Detailed Design

### Services and Modules

*   **Frontend Config Module (`frontend/app/config/`):**
    *   `ConfigForm`: Main container component managing the multi-step wizard or tabbed interface.
    *   `JobEditor`: Component for adding/removing jobs and resources.
    *   `AgentEditor`: Component for defining agent populations.
    *   `api.ts`: Updated to include `submitConfig` and `controlSimulation` methods.

*   **Backend Core (`backend/core/`):**
    *   `engine.py`: Needs methods `initialize(config: SimulationConfig)` and `start()`, `stop()`.
    *   `state.py`: The `WorldState` class must support a "reset" to a fresh state based on config.

*   **Backend API (`backend/main.py` & `backend/api/`):**
    *   New router `config.py` for configuration endpoints.
    *   New router `control.py` for simulation flow control.

### Data Models and Contracts

**Pydantic Models (`backend/models/domain.py`):**

```python
class JobConfig(BaseModel):
    job_id: str
    resource_produced: str

class AgentConfig(BaseModel):
    count: int
    job_id: str  # Must match a defined JobConfig
    culture: str
    needs: Dict[str, int]
    wants: Dict[str, int]
    income: int

class GlobalConfig(BaseModel):
    day_length_seconds: int = Field(..., gt=0)
    max_days: int = Field(..., gt=0)

class SimulationConfig(BaseModel):
    globals: GlobalConfig
    jobs: List[JobConfig]
    agents: List[AgentConfig]
```

### APIs and Interfaces

| Method | Endpoint | Request Body | Response | Description |
| :--- | :--- | :--- | :--- | :--- |
| `POST` | `/api/config` | `SimulationConfig` (JSON) | `200 OK` or `422 Error` | Validates config and initializes WorldState. |
| `POST` | `/api/control/start` | None | `200 OK` | Starts the simulation loop. |
| `POST` | `/api/control/stop` | None | `200 OK` | Stops/Pauses the simulation loop. |
| `POST` | `/api/control/reset` | None | `200 OK` | Clears current state (optional, or part of config). |

### Workflows and Sequencing

1.  **User Interaction:** User completes the Configuration Form on the frontend.
2.  **Client-Side Validation:** Frontend checks for basic errors (negative numbers, empty fields).
3.  **Submission:** Frontend sends `POST /api/config` with the JSON payload.
4.  **Backend Validation:** FastAPI/Pydantic validates types and logical constraints (e.g., distinct job IDs).
5.  **Initialization:**
    *   If valid: Backend replaces the `WorldState` singleton with a new instance populated with the specified agents and jobs. Returns 200.
    *   If invalid: Returns 422 with specific field errors.
6.  **Start:** User clicks "Start Simulation". Frontend sends `POST /api/control/start`. Backend Engine begins the tick loop.

## Non-Functional Requirements

### Performance
*   **Responsiveness:** The Configuration UI should handle up to 50 distinct agent groups without UI lag.
*   **Initialization Time:** Simulation initialization (backend) should take < 500ms for a standard config (100 agents).

### Security
*   **Input Sanitization:** All string inputs (Agent Name, Culture) must be sanitized to prevent injection (though low risk in MVP).
*   **Validation limits:** Enforce reasonable max limits (e.g., max 1000 agents) to prevent DoS via massive memory allocation.

### Reliability
*   **Atomic Config:** The simulation state is only updated if the *entire* configuration is valid. No partial application.
*   **Error Feedback:** Validation errors must be returned with clear messages mapped to the specific UI fields.

### Observability
*   **Logging:** Log every configuration change and simulation state transition (Initialized -> Running -> Stopped).

## Dependencies and Integrations

*   **Frontend:**
    *   `react-hook-form` or `zod`: For form state management and validation (standard with shadcn/ui forms).
    *   `shadcn/ui`: specific components: `Form`, `Input`, `Button`, `Card`, `Table` (for job lists).
*   **Backend:**
    *   `pydantic`: Core validation logic.

## Acceptance Criteria (Authoritative)

**From Epic 2 Stories:**

1.  **Global Parameters (Story 2.1):**
    *   Input fields for "Day Length" and "Max Days" exist.
    *   Values must be positive integers.
    *   UI validates these before submission.

2.  **Job Definition (Story 2.2):**
    *   User can add multiple Job/Resource pairs.
    *   User can remove a Job.
    *   Duplicate Job IDs are prevented.

3.  **Agent Definition (Story 2.3):**
    *   User can specify agent count for a job.
    *   User can define culture string, needs, and wants.
    *   System generates the full list of individual agents from these groups upon config generation.

4.  **Backend Config (Story 2.4):**
    *   `POST /api/config` accepts valid JSON and initializes state.
    *   Invalid JSON returns 422.
    *   Successful config resets `current_day` to 0.

5.  **Controls (Story 2.5):**
    *   Start/Stop buttons function correctly.
    *   Frontend switches to "Monitor" view upon successful Start.
    *   Simulation actually advances ticks when Started (verified via logs/state).

## Traceability Mapping

| Acceptance Criteria | Component | API / Module | Test Idea |
| :--- | :--- | :--- | :--- |
| Global Params Validation | Frontend | `ConfigForm` | Try entering "-1" for days; button should be disabled. |
| Job List Management | Frontend | `JobEditor` | Add 3 jobs, delete the middle one; verify list integrity. |
| Config Submission | Backend | `POST /api/config` | Send valid JSON; check `GET /api/state` reflects new agent count. |
| Invalid Config Handling | Backend | `POST /api/config` | Send config with agent referring to non-existent job; expect 422. |
| Start Simulation | Backend | `engine.py` | Call Start; wait 5s; check `tick_count` > 0. |

## Risks, Assumptions, Open Questions

*   **Risk:** Complex UI state management for nested lists (Jobs -> Agents) can be buggy.
    *   *Mitigation:* Use a robust form library (`react-hook-form`) and keep the data structure flat where possible.
*   **Assumption:** Researchers don't need to configure *individual* agents one-by-one, but rather "groups" of identical agents (e.g., "5 Cooperative Farmers"). The UI will support this "Agent Group" concept.
*   **Question:** Should we allow "Random" culture assignment?
    *   *Decision:* MVP will use explicit assignment. Randomization can be added later.

## Test Strategy Summary

*   **Unit Tests:**
    *   Backend: Test `SimulationConfig` Pydantic models with valid/invalid data.
    *   Backend: Test `Engine.initialize()` ensures state is reset cleanly.
*   **Component Tests:**
    *   Frontend: Test `JobEditor` adds and removes items correctly.
*   **Integration Tests:**
    *   Full flow: Config Payload -> API -> Init State -> Start -> 1 Tick.
