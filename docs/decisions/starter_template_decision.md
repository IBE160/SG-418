# Starter Template Decision

*   **Selected Template:** None (Custom Setup)
*   **Rationale:** The project requires a specialized, long-running simulation engine without the overhead of a full database or authentication system (which most templates force). A custom setup allows for a lightweight, fit-for-purpose architecture.
*   **Initialization Strategy:**
    *   **Frontend:** `npx create-next-app@latest` (Standard Next.js 14+ setup)
    *   **Backend:** `uv init` (Modern Python project management)
    *   **Integration:** REST API over HTTP
