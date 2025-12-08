# Epic Technical Specification: Deep Inspection & Analysis

Date: Monday, December 8, 2025
Author: BIP
Epic ID: 5
Status: Draft

---

## Overview

Epic 5 focuses on providing researchers with deep visibility into the simulation's micro-level dynamics and the ability to extract data for post-hoc analysis. While the dashboard (Epic 4) provides a high-level overview, this epic implements the "Agent Inspector" to view individual agent states (inventory, needs, recent thoughts) and the "Data Export" functionality to download the full simulation event log as a CSV file. These features are critical for verifying emergent behavior and conducting quantitative research.

## Objectives and Scope

**In Scope:**
*   **Agent Inspector UI:** A side panel (using shadcn `Sheet`) that displays detailed information about a selected agent.
*   **Real-Time Detail Updates:** The inspector panel must update dynamically as the simulation progresses (via polling).
*   **Event Log Export:** A backend endpoint to convert the in-memory event log into a downloadable CSV file.
*   **CSV Formatting:** Ensuring the exported data is structured correctly for analysis (Tick, AgentID, Action, Details, Result).

**Out of Scope:**
*   **Agent Editing:** Users cannot modify agent state (e.g., add inventory) while the simulation is running.
*   **Database Persistence:** Export is based on in-memory state; no persistent database is being added.
*   **Complex Filtering:** The export will dump the entire log; filtering will happen in external tools (Excel/Python).

## System Architecture Alignment

This epic aligns with the established **Split-Stack Architecture** and **In-Memory State** pattern:

*   **Frontend (Next.js):** Utilizes `shadcn/ui` components (specifically `Sheet`) for the Inspector Panel, maintaining the "Command Center" aesthetic.
*   **Backend (FastAPI):** Adds a `GET /api/export` endpoint. Since state is in-memory, this endpoint simply iterates over the `WorldState.event_log` list and streams a CSV response.
*   **Communication:** The Inspector Panel leverages the existing HTTP Short Polling mechanism (fetching `WorldState`) or potentially a targeted `GET /api/state` if optimization is needed, though the global state object likely contains enough detail for MVP.

## Detailed Design

### Services and Modules

| Module | Component | Responsibility | Inputs | Outputs | Owner |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Frontend** | `AgentInspector` | UI component to display detailed agent data. | `selectedAgentId`, `WorldState` | Rendered UI | Frontend Dev |
| **Frontend** | `ExportButton` | UI control to trigger CSV download. | User Click | Browser Download | Frontend Dev |
| **Backend** | `ExportService` | Logic to convert event log to CSV format. | `WorldState.event_log` | CSV String | Backend Dev |
| **Backend** | `API Router` | Route handler for export request. | `GET /api/export` | `StreamingResponse` | Backend Dev |

### Data Models and Contracts

**Frontend Type Definition (`AgentDetail` - subset of `Agent`):**
```typescript
interface AgentDetail {
  id: string;
  name: string;
  job: string;
  culture: string;
  inventory: Record<string, number>;
  needs: Record<string, number>;
  satisfaction: number;
  lastAction: string;
}
```

**Export Schema (CSV Columns):**
`Tick, Day, AgentID, ActionType, TargetAgentID, Resource, Amount, Price, Result, Details`

### APIs and Interfaces

**1. Export Event Log**
*   **Endpoint:** `GET /api/export`
*   **Description:** Downloads the full simulation history.
*   **Response:** `200 OK` (Content-Type: `text/csv`)
*   **Header:** `Content-Disposition: attachment; filename="simulation_log_{timestamp}.csv"`

**(Note: Agent details are already available via the existing `GET /api/state` which returns the full `WorldState` including the list of agents. No new API is strictly required for the Inspector unless payload size becomes an issue, which is unlikely for MVP agent counts.)**

### Workflows and Sequencing

**1. Inspecting an Agent**
1.  **User** clicks on an agent node in the Interaction Graph or an ID in the Event Log.
2.  **Frontend** sets `selectedAgentId` in local state (or Zustand store).
3.  **Frontend** opens the `Sheet` component.
4.  **Frontend** (via existing polling hook) receives the latest `WorldState`.
5.  **Inspector Component** finds the agent matching `selectedAgentId` in the `WorldState.agents` list.
6.  **UI** updates to show the agent's current inventory and needs.

**2. Exporting Data**
1.  **User** clicks the "Export CSV" button in the dashboard sidebar.
2.  **Frontend** triggers a direct browser navigation or `window.open` to `API_URL/api/export`.
3.  **Backend** receives request.
4.  **Backend** locks the event log (if necessary for thread safety) or copies it.
5.  **Backend** generates CSV lines from the list of events.
6.  **Browser** handles the file download.

## Non-Functional Requirements

### Performance
*   **Export Latency:** CSV generation for a standard simulation (e.g., 5 days, 10 agents) should start streaming within < 500ms.
*   **UI Responsiveness:** The Inspector Panel open/close animation should be smooth (60fps).

### Security
*   **Sanitization:** Ensure CSV output does not contain executable formulas (CSV injection), though inputs are strictly controlled by the system.

### Reliability
*   **Empty State:** Export function must handle cases where the event log is empty without crashing.
*   **Concurrency:** Exporting should not block the main simulation loop (FastAPI async handling).

### Observability
*   **Logging:** The backend should log when an export is requested and completed, including the number of rows generated.

## Dependencies and Integrations

*   **shadcn/ui Sheet:** For the slide-out inspector panel.
*   **Python `csv` module:** Standard library for backend CSV generation.
*   **Frontend Polling Hook:** Relies on the hook established in Epic 4.

## Acceptance Criteria (Authoritative)

### 1. Agent Inspector Panel UI (Story 5.1, 5.2)
1.  Clicking an agent ID in the graph or log opens a side panel (`Sheet`).
2.  The panel displays the agent's Static Info: ID, Job, Culture.
3.  The panel displays Dynamic Info: Current Inventory (item counts), Needs (status), Current Satisfaction/Score.
4.  The data in the panel updates automatically with the next simulation tick (via polling).
5.  Closing the panel clears the selection.

### 2. Export Event Log to CSV (Story 5.3)
1.  Clicking "Export Data" initiates a file download.
2.  The file format is `.csv`.
3.  The file includes all events from `tick=0` to current.
4.  Columns include at minimum: `Tick`, `AgentID`, `Action`, `Details/Result`.
5.  The exported data matches the events shown in the Live Event Log.

## Traceability Mapping

| Acceptance Criteria | Spec Section | Component | Test Idea |
| :--- | :--- | :--- | :--- |
| AC 1.1 (Open Panel) | Workflows #1 | Frontend/AgentInspector | Simulate click, assert Sheet is visible. |
| AC 1.3 (Dynamic Info) | Data Models | Frontend/AgentInspector | Update mock state, assert UI numbers change. |
| AC 2.1 (Download) | APIs #1 | Backend/ExportService | Request endpoint, verify HTTP 200 & Content-Disposition. |
| AC 2.4 (Columns) | Data Models | Backend/ExportService | Parse downloaded CSV, verify headers match schema. |

## Risks, Assumptions, Open Questions

*   **Assumption:** The `WorldState` payload size is manageable for the frontend to filter agent details client-side.
    *   *Mitigation:* If payload > 1MB, implement `GET /api/agent/{id}`. For MVP (< 50 agents), client-side filtering is fine.
*   **Risk:** Large CSV exports might consume significant memory on the backend if the simulation runs for thousands of ticks.
    *   *Mitigation:* Use Python's `StreamingResponse` to stream lines instead of building the whole string in memory.

## Test Strategy Summary

*   **Unit Tests (Backend):** Test `ExportService` with a mock event log to verify CSV formatting and header generation.
*   **Integration Tests (API):** Test `GET /api/export` returns valid CSV content type.
*   **Component Tests (Frontend):** Test `AgentInspector` renders correctly with various `AgentDetail` props.
