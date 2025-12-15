# Story 4.3: Live Event Log Feed

Status: drafted

## Story

As a **Researcher**,
I want **a scrolling log of all major events (trades, conversations)**,
so that **I can follow the narrative of the simulation**.

## Acceptance Criteria

1. **Given** agents are interacting, **When** a trade or error occurs, **Then** a new text line should appear in the log panel.
2. **And** it should show the Day/Time and a description of the event.
3. **And** the log should automatically scroll to the newest event (or allow manual scrolling).

## Tasks / Subtasks

- [ ] Backend: Event Model & Storage (AC: 1, 2)
  - [ ] Define `Event` Pydantic model (timestamp, description, agent_id, type) in `backend/models/domain.py`
  - [ ] Add `events: List[Event]` to `WorldState` in `backend/core/state.py`
  - [ ] Implement helper function `log_event(event: Event)` in `backend/core/engine.py`

- [ ] Backend: Event API (AC: 1)
  - [ ] Ensure `GET /api/state` includes the recent events OR create `GET /api/events` endpoint (check Architecture preference, default to state inclusion for MVP simplicity)

- [ ] Frontend: Log Component (AC: 1, 2, 3)
  - [ ] Create `components/simulation/EventLog.tsx`
  - [ ] Implement `shadcn/ui` `ScrollArea` component
  - [ ] Connect to data source (Zustand store / API polling)
  - [ ] Render list of events with timestamp and description
  - [ ] Add auto-scroll behavior for new events

## Dev Notes

### Architecture & Tech Stack
- **Frontend**: Next.js 14, `shadcn/ui` ScrollArea.
- **Backend**: Python FastAPI, In-Memory State.
- **Data Pattern**: Polling (per Epic 4.2 pattern).

### Project Structure Alignment
- Backend models: `backend/models/`
- Backend core logic: `backend/core/`
- Frontend components: `frontend/components/simulation/`

### Learnings from Previous Story
- Previous story (4.2) not yet implemented (Status: backlog).
- Ensure consistent data fetching pattern (polling hook) used in 4.2 is reused/extended here.

### References
- [Epic 4: Real-Time Monitoring Dashboard](../epics.md#epic-4-real-time-monitoring-dashboard)
- [Architecture Decision: In-Memory State](../decisions/implementation_patterns.md)

## Dev Agent Record

### Context Reference
<!-- Path(s) to story context XML will be added here by context workflow -->

### Agent Model Used
Gemini-2.5-Flash

### Completion Notes List
