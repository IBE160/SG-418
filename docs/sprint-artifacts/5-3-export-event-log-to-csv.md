# Story 5.3: Export Event Log to CSV

Status: drafted

## Story

As a **Researcher**,
I want **to download the full simulation history as a CSV file**,
so that **I can perform statistical analysis in Excel or Python**.

## Acceptance Criteria

1.  **Trigger Download**: Clicking "Export Data" in the dashboard initiates a file download.
2.  **File Format**: The downloaded file is in `.csv` format.
3.  **Data Completeness**: The file includes all events from the simulation start (`tick=0`) to the current moment.
4.  **Schema Compliance**: The CSV contains at minimum the columns: `Tick`, `AgentID`, `Action`, `Details` (or Result).
5.  **Consistency**: The exported data matches the events shown in the Live Event Log.

## Tasks / Subtasks

- [ ] **Backend: Implement Export Logic** (AC 3, 4)
  - [ ] Create a utility function/service to convert `WorldState.event_log` to CSV format.
  - [ ] Ensure correct column headers: `Tick`, `Day`, `AgentID`, `Action`, `Target`, `Resource`, `Amount`, `Result`.
  - [ ] Use Python's `csv` module (standard library) for proper escaping.

- [ ] **Backend: Create Export Endpoint** (AC 1, 2)
  - [ ] Add `GET /api/export` route in `backend/app/main.py` (or dedicated router).
  - [ ] Implement `StreamingResponse` to stream CSV lines (memory efficiency).
  - [ ] Set `Content-Type: text/csv`.
  - [ ] Set `Content-Disposition` header with a timestamped filename (e.g., `simulation_log_20251215.csv`).

- [ ] **Frontend: Add Export Control** (AC 1)
  - [ ] Add an "Export CSV" button to the Dashboard Sidebar (or global controls area).
  - [ ] Implement the click handler to trigger the download (e.g., `window.open` or hidden anchor tag pointing to `/api/export`).

- [ ] **Verification & Testing** (AC 5)
  - [ ] Verify that the downloaded file opens correctly in Excel/Sheets.
  - [ ] Verify that special characters in log messages are escaped correctly.
  - [ ] Ensure endpoint handles empty event logs gracefully.

## Dev Notes

### Implementation Details
-   **Memory Management**: For long simulations, the event log could be large. Avoid creating the entire CSV string in memory. Use a generator function with `StreamingResponse`.
-   **Concurrency**: Since `WorldState` is a singleton accessed by the simulation loop, consider if a read-lock is needed, though for MVP and Python's GIL/FastAPI async model, iterating over the list is likely safe enough if append-only.
-   **Frontend**: No complex API client method needed; a simple browser navigation/download trigger is sufficient for a GET request returning a file.

### Architecture Alignment
-   **State Source**: Read directly from the in-memory `WorldState.event_log`.
-   **Location**: Logic belongs in `backend` (likely `backend/app/api/` or `backend/app/services/` if strict separation desired, but `main.py` or `api/routes.py` is fine for MVP).

### References
-   [Source: docs/sprint-artifacts/tech-spec-epic-5.md#Detailed-Design]
-   [Source: docs/epics.md#Story-5.3:-Export-Event-Log-to-CSV]

## Dev Agent Record

### Context Reference

<!-- Path(s) to story context XML will be added here by context workflow -->

### Agent Model Used

Gemini 2.5 Flash

### Debug Log References

### Completion Notes List

### File List
