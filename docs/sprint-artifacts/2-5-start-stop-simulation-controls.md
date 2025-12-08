# Story 2.5: Start/Stop Simulation Controls

**Epic:** 2 - Simulation Configuration Interface
**Status:** Draft
**Sprint:** 1
**Feature:** Simulation Execution Control

## User Story

As a **Researcher**,
I want **buttons to Start, Pause, and Stop the simulation**,
So that **I can control the execution flow and observe specific behaviors.**

## Acceptance Criteria

### Scenario 1: Start Simulation
**Given** a valid configuration has been submitted (System is initialized)
**And** the simulation is currently stopped or paused
**When** I click the "Start Simulation" button
**Then** the backend engine should begin processing ticks
**And** the frontend should switch to the "Monitor" view
**And** the system status indicator should change to "Running"

### Scenario 2: Stop/Pause Simulation
**Given** the simulation is currently running
**When** I click the "Stop" or "Pause" button
**Then** the backend engine should stop processing ticks
**And** the system status indicator should change to "Stopped" or "Paused"
**And** the current state (tick count, agent states) should be preserved

### Scenario 3: Reset Simulation
**Given** the simulation is running or stopped
**When** I click the "Reset" button
**Then** the backend should clear the current simulation state
**And** the frontend should return to the Configuration view
**And** the tick count should be 0

## Technical Implementation Plan

### 1. Backend Implementation (`fastapi`)

**Objective:** Create control endpoints to manage the engine loop.

-   **File:** `backend/api/control.py` (New Router)
    -   `POST /api/control/start`: Triggers `engine.start()`.
    -   `POST /api/control/stop`: Triggers `engine.stop()`.
    -   `POST /api/control/reset`: Triggers `state.reset()` and `engine.reset()`.

-   **File:** `backend/core/engine.py` (Update)
    -   Implement `start()`: Should likely set a flag `is_running = True` and ensuring the tick loop is active (if using `asyncio.create_task` for background ticks or similar mechanism).
    -   Implement `stop()`: Set `is_running = False`.
    -   Implement `reset()`: Stop engine and reset ticks.

-   **File:** `backend/main.py`
    -   Include the new `control` router.

### 2. Frontend Implementation (`next.js`)

**Objective:** Add UI controls and connect to backend.

-   **File:** `frontend/lib/api.ts` (Update)
    -   Add function `controlSimulation(action: 'start' | 'stop' | 'reset'): Promise<void>`.

-   **File:** `frontend/lib/store.ts` (Update Zustand Store)
    -   Add `simulationStatus`: `'idle' | 'running' | 'paused'`.
    -   Add actions to update this status based on API responses.

-   **File:** `frontend/components/simulation-controls.tsx` (New Component)
    -   Buttons: Play (Start), Pause/Stop, Reset.
    -   Logic: Call API on click, update local/global state.

-   **File:** `frontend/app/page.tsx` (or Main Layout)
    -   Integrate `SimulationControls` component.
    -   Implement conditional rendering: Show "Monitor" view if status is `running` or `paused`.

## Validation Steps

1.  **Manual Test:** Configure a simple simulation (1 agent).
2.  **Manual Test:** Click "Start". Verify logs show ticks incrementing.
3.  **Manual Test:** Click "Stop". Verify logs show ticks stopping.
4.  **Manual Test:** Click "Reset". Verify frontend goes back to Config screen and backend state is cleared.
5.  **API Test:** `curl -X POST http://localhost:8000/api/control/start` returns 200 OK.
