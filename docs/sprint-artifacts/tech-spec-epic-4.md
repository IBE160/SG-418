# Epic Technical Specification: Real-Time Monitoring Dashboard

Date: Monday, December 8, 2025
Author: BIP
Epic ID: 4
Status: Draft

---

## Overview

Develop a real-time web-based dashboard using Next.js to visualize the simulation state. This includes a responsive layout with a sidebar, a live economic value graph, a scrolling event log, and an agent interaction diagram. This component fulfills the monitoring requirements (FR3.1, FR3.3, FR3.4) enabling researchers to observe emergent behaviors.

## Objectives and Scope

### In-Scope
*   **Dashboard Shell:** A responsive layout with a sidebar navigation and main content area ("Command Center" style).
*   **Real-Time Polling:** Mechanism to fetch `WorldState` from the backend API (HTTP GET `/api/state`) at regular intervals.
*   **Economic Graph:** A time-series line chart displaying the "Total Economic Value" or similar global metric.
*   **Event Log:** A scrollable, auto-updating list of simulation events (trades, errors, system messages).
*   **Interaction Diagram:** A visualization (node-link or scatter plot) showing agent positions and active interactions.

### Out-of-Scope
*   **Detailed Agent Inspection:** Clicking agents to view deep state is part of Epic 5.
*   **Historical Playback:** "Rewind" or replay functionality is not included in MVP.
*   **Advanced Filtering:** Complex filtering of the event log (e.g., by agent ID) is post-MVP.
*   **WebSocket:** Real-time push is explicitly decided against in favor of HTTP Polling for MVP simplicity.

## System Architecture Alignment

This epic aligns with the **Split-Stack Architecture** defined in the Architecture Document:
*   **Frontend:** Next.js 14 (App Router) serves the UI.
*   **Backend:** FastAPI provides the data via REST endpoints.
*   **Communication:** Adheres to the "HTTP Short Polling" decision (Decision Summary Table) for near real-time updates (1-5s tick rates).
*   **State:** The dashboard consumes the `WorldState` In-Memory Singleton from the backend.
*   **UI Library:** Utilizes `shadcn/ui` (built on Radix UI and Tailwind CSS) for layout and `Recharts` for data visualization.

## Detailed Design

### Services and Modules

| Module / Component | Responsibility | Inputs | Outputs | Owner |
| :--- | :--- | :--- | :--- | :--- |
| **`DashboardPage`** (`app/dashboard/page.tsx`) | Main container; manages the polling hook and global state distribution. | URL Route | Rendered Page | Frontend |
| **`DashboardLayout`** | Provides the shell structure (Sidebar, Header, Main Content). | Children Components | UI Layout | Frontend |
| **`SimulationStateHook`** (`useSimulationState`) | Custom React hook to poll `GET /api/state` and manage loading/error states. | Polling Interval | `WorldState`, `isLoading`, `error` | Frontend |
| **`EconomyChart`** | Renders the time-series graph of global value using `Recharts`. | `market_history` (from State) | Line Chart | Frontend |
| **`EventLogFeed`** | Displays a scrollable list of events. | `event_log` (from State) | List UI | Frontend |
| **`InteractionGraph`** | Visualizes agents and their connections. | `agents` (from State) | Scatter/Node Graph | Frontend |

### Data Models and Contracts

**Frontend State (TypeScript Interfaces)**
Must match the Backend Pydantic Models.

```typescript
// Mirrored from backend/models/domain.py
interface WorldState {
  current_day: number;
  tick_count: number;
  agents: Agent[];
  market_history: MarketMetric[]; // { tick: number, total_value: number }
  event_log: SimulationEvent[];
}

interface SimulationEvent {
  id: string;
  timestamp: string; // ISO format
  type: 'TRADE' | 'ERROR' | 'SYSTEM' | 'NEGOTIATION';
  description: string;
  agent_id?: string;
}

interface Agent {
  id: string;
  job: string;
  // ... other fields needed for interaction graph (e.g. status)
}
```

### APIs and Interfaces

**Endpoint:** `GET /api/state`

*   **Description:** Returns the current snapshot of the simulation.
*   **Response (200 OK):** JSON matching `WorldState` structure.
*   **Error (500):** If backend is unreachable or internal error.

### Workflows and Sequencing

**Real-Time Polling Loop**

1.  **Dashboard Mount:** User navigates to `/dashboard`. Component mounts.
2.  **Hook Initialization:** `useSimulationState` starts a `setInterval`.
3.  **Poll:** Every X seconds (e.g., 2s), `fetch('/api/state')` is called.
4.  **Update:**
    *   **Success:** New JSON data replaces the current state in React context/store. Components re-render.
    *   **Error:** Error state is set. "Connection Lost" toast may appear.
5.  **Unmount:** `clearInterval` is called when user leaves page.

## Non-Functional Requirements

### Performance
*   **Render Latency:** Dashboard components must render updates within **100ms** of receiving new state.
*   **Polling Efficiency:** Polling interval should be configurable (default 2s) to balance freshness vs. load.
*   **Chart Performance:** `Recharts` should handle up to 1000 data points without significant UI lag.

### Security
*   **Read-Only:** The dashboard view is strictly read-only. No state mutation actions (POST) are triggered from the monitoring components.
*   **CORS:** API must be configured to allow requests only from the frontend origin (e.g., `http://localhost:3000`).

### Reliability/Availability
*   **Graceful Degradation:** If the backend is down, the dashboard should not crash (White Screen of Death). It should display a "Reconnecting..." status indicator.
*   **Data Integrity:** Charts must handle missing or partial data points gracefully (e.g., gaps in the line chart).

### Observability
*   **Client Logging:** Console errors should be logged when polling fails.
*   **Loading States:** Visual indicators (spinners/skeletons) must be shown while initial data is fetching.

## Dependencies and Integrations

*   **Libraries (npm):**
    *   `recharts`: For LineChart and ScatterChart.
    *   `lucide-react`: For icons in the sidebar and log.
    *   `clsx`, `tailwind-merge`: For dynamic class styling.
    *   `swr` or `react-query` (Optional, but recommended over raw `useEffect` for better polling management).
*   **UI Components (`shadcn/ui`):**
    *   `Card`: Containers for widgets.
    *   `ScrollArea`: For the Event Log.
    *   `Sheet`: (Prepared for Epic 5, used for sidebar on mobile if needed).
    *   `Button`: Navigation controls.

## Acceptance Criteria (Authoritative)

1.  **Dashboard Layout:** The `/dashboard` route renders a layout with a persistent sidebar and a main content area.
2.  **Live Updates:** The "Total Economic Value" chart updates automatically (without page refresh) as the simulation progresses.
3.  **Event Stream:** New events appear at the top (or bottom, auto-scrolling) of the Event Log widget.
4.  **Interaction Viz:** The Interaction Diagram displays nodes corresponding to the active agents.
5.  **Resilience:** Stopping the backend server results in a visible "Offline" indicator on the dashboard, and restarting it resumes updates automatically.

## Traceability Mapping

| Acceptance Criteria | Spec Section | Component(s) | Test Idea |
| :--- | :--- | :--- | :--- |
| **AC1: Layout** | Detailed Design / Services | `DashboardLayout` | Visual check of sidebar existence. |
| **AC2: Live Updates** | Workflows / Polling | `EconomyChart`, `useSimulationState` | Mock API with changing values, verify chart re-render. |
| **AC3: Event Stream** | Detailed Design / Services | `EventLogFeed` | Add event to mock state, verify list item appears. |
| **AC4: Interaction Viz** | Detailed Design / Services | `InteractionGraph` | Verify number of nodes matches `agent_count`. |
| **AC5: Resilience** | NFR / Reliability | `useSimulationState` | Simulate 500 API response, check for error UI. |

## Risks, Assumptions, Open Questions

*   **Risk:** Polling the *entire* state every 2 seconds might become heavy if the `market_history` or `event_log` grows very large over a long simulation.
    *   *Mitigation (Post-MVP):* Implement pagination for logs or "delta" updates (only fetch data since `last_tick`). For MVP, we assume lists < 10k items.
*   **Assumption:** The backend calculates "Total Economic Value". If not, the frontend must compute it from raw agent data (which is heavier).
*   **Open Question:** What specific layout/algorithm should the "Interaction Diagram" use? (Assumption: Simple random or circular layout for MVP).

## Test Strategy Summary

*   **Unit Tests:**
    *   Test `useSimulationState` hook handles success/error states correctly.
    *   Test `EventLogFeed` renders list items correctly.
*   **Integration Tests:**
    *   Mount `DashboardPage` with a mocked API client.
    *   Simulate a sequence of state updates.
    *   Assert that the Chart and Log components receive the new props.
*   **Manual Validation:**
    *   Run the full simulation (backend + frontend).
    *   Visually verify the "heartbeat" of the graphs matching the console output of the backend.
