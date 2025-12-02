# Cross-Cutting Decisions

**Error Handling Strategy:**
*   **Backend:** Use global exception handlers in FastAPI to catch crashes and return standardized JSON errors `{ "error": "message", "code": 500 }`.
*   **Frontend:** Use React Error Boundaries to catch UI crashes and show a "Something went wrong" card instead of a white screen.

**Logging Approach:**
*   **Format:** Structured Logging (JSON).
*   **Convention:** All logs must include `{"timestamp": "...", "level": "INFO", "component": "Agent/Sim/API", "message": "..."}`.
*   **Why:** Makes the "Event Log" feature easy to implement—just filter the logs!

**Date/Time Handling:**
*   **Standard:** UTC everywhere on the backend.
*   **Format:** ISO 8601 Strings (`2024-11-21T10:00:00Z`).
*   **Display:** Convert to User's Local Time only at the very last moment (in the React Component).

**API Response Format:**
*   **Success:** Direct data return (e.g., `[Agent1, Agent2]`).
*   **Validation Error:** `422 Unprocessable Entity` (Standard FastAPI behavior).
*   **System Error:** `500 Internal Server Error` with safe message.
