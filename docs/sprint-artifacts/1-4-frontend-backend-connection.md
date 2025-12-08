# Story 1.4: Frontend-Backend Connection

**Epic:** 1 - Foundation & Simulation Engine
**Story Key:** 1-4-frontend-backend-connection
**Status:** Drafted
**Date:** 2025-12-08

## User Story

**As a** User,
**I want** the frontend to connect to the backend API,
**So that** I can verify the system is operational and the two components can communicate.

## Acceptance Criteria

### 1. Backend Health Endpoint
- [ ] The backend exposes a `GET /health` endpoint.
- [ ] The endpoint returns a JSON response with status "online" and the current timestamp.
- [ ] The endpoint is accessible from the frontend (CORS configured).

### 2. Frontend API Client
- [ ] A dedicated API client module (`lib/api.ts`) is implemented.
- [ ] The client handles base URL configuration (defaulting to localhost:8000).
- [ ] The client provides a typed function to fetch system status.

### 3. System Status Display
- [ ] The home page (`/`) displays a "System Status" indicator.
- [ ] When backend is running, the indicator shows "Online" (green).
- [ ] When backend is stopped/unreachable, the indicator shows "Offline" (red/gray).
- [ ] The status is checked on page load.

## Implementation Tasks

### Backend
- [ ] **Task 1:** Add `GET /health` route to `backend/main.py`.
    - Return model: `{"status": "online", "timestamp": "..."}`.
- [ ] **Task 2:** Configure CORS in `backend/main.py` to allow requests from `http://localhost:3000`.

### Frontend
- [ ] **Task 3:** Create `frontend/lib/config.ts` for environment variables (API URL).
- [ ] **Task 4:** Create `frontend/lib/api.ts` with `getHealthStatus()` function.
    - Use `fetch` API.
    - Handle network errors gracefully.
- [ ] **Task 5:** Update `frontend/app/page.tsx`.
    - Add state for `status` (loading, online, offline).
    - Use `useEffect` to call `getHealthStatus`.
    - Render status badge/text.

### Testing
- [ ] **Task 6:** Manual Verification.
    - Start backend, start frontend -> See "Online".
    - Stop backend -> Refresh frontend -> See "Offline".

## Development Notes

### Architectural Decisions
- **API Pattern:** Use a simple `fetch` wrapper for now. No complex query library (React Query) needed for this simple status check yet, but keep it in mind for Epic 2.
- **CORS:** strict allow-list for `localhost:3000` to align with security requirements.

### Dependencies
- Backend: `fastapi`, `uvicorn`.
- Frontend: `lucide-react` (for status icons if used).

### Learnings from Previous Story
*Previous story (1-3-backend-state-management) not yet implemented.*

## Change Log
- **2025-12-08**: Initial draft created by Scrum Master.
