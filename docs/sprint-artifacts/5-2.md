# Story 5.2: Agent Detail Data Fetching

Status: drafted

## Story

As a User,
I want to see the "Needs" and "Recent Thoughts" of the inspected agent,
so that I can debug their behavior.

## Acceptance Criteria

1.  **Live Updates:** Given the Inspector is open, when the polling cycle triggers, the displayed values (Inventory, Satisfaction, Needs, Last Action) update automatically. [Source: tech-spec-epic-5.md]
2.  **Data Completeness:** The data available to the frontend includes: ID, Job, Culture, Inventory, Needs, Satisfaction, and Last Action. [Source: tech-spec-epic-5.md]

## Tasks / Subtasks

- [ ] **Backend Model Update** (AC 2)
  - [ ] Verify `Agent` model in `backend/app/models/domain.py` includes `inventory`, `needs`, `satisfaction`, and `last_action` fields.
  - [ ] Ensure `WorldState` model correctly propagates this full agent list in the `GET /api/state` response.
  - [ ] Testing: Unit test `Agent` model serialization to ensure all fields are present in JSON output.
- [ ] **Frontend Type Definition** (AC 1, AC 2)
  - [ ] Define `AgentDetail` interface (or update existing `Agent` type) in `frontend/src/types/` to match the backend model.
  - [ ] Ensure the type includes `needs` (Record<string, number>) and `inventory` (Record<string, number>).
- [ ] **Integration Verification** (AC 1)
  - [ ] Verify that the existing polling hook in `frontend/src/lib/api.ts` (or equivalent) fetches the updated `WorldState`.
  - [ ] (Manual) Verify `GET /api/state` payload contains the new fields.

## Dev Notes

- **Architecture Pattern:** This story relies on the "In-Memory State" and "HTTP Short Polling" patterns. We are NOT creating a specific `GET /api/agent/{id}` endpoint at this stage, as the global `WorldState` payload is expected to be small enough for MVP (< 50 agents). [Source: docs/architecture.md]
- **Data Source:** The `WorldState.agents` list is the single source of truth.
- **Frontend State:** The frontend will filter the `WorldState` client-side to find the selected agent.

### Project Structure Notes

- Backend models: `backend/app/models/domain.py`
- Frontend types: `frontend/src/types/` (or `types.ts` depending on setup)

### References

- [Source: docs/sprint-artifacts/tech-spec-epic-5.md#Detailed-Design] (Data Models)
- [Source: docs/architecture.md#9-data-architecture] (WorldState definition)

## Dev Agent Record

### Context Reference

<!-- Path(s) to story context XML will be added here by context workflow -->

### Agent Model Used

Gemini 2.5 Flash

### Debug Log References

### Completion Notes List

### Learnings from Previous Story

*   **Previous Story Status:** Backlog (5.1)
*   **Note:** Story 5.1 (UI shell) is not yet implemented. This story (5.2) focuses on ensuring the *data* is available and typed correctly. The actual UI implementation will depend on 5.1, but the data structures can be prepared now.
*   **Dependency:** Ensure coordination with 5.1 implementation to use the types defined here.

### File List
