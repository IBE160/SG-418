# Story 2.4: Backend Configuration Endpoint

Status: drafted

## Story

As a **Developer**,
I want **an API endpoint to receive the full simulation configuration**,
so that **the backend can initialize the simulation state.**

## Acceptance Criteria

1. **Endpoint Definition**: `POST /api/config` exists and accepts a JSON payload matching `SimulationConfig`.
2. **Schema Validation**: The backend must strictly validate the payload against Pydantic models (`SimulationConfig`, `GlobalConfig`, `JobConfig`, `AgentConfig`). Invalid requests return 422.
3. **State Initialization**: Upon successful validation, the backend `WorldState` singleton is initialized (or reset) with the specified agents, jobs, and global settings.
4. **State Reset**: Any existing simulation state (current day, history, active agents) is cleared before applying the new configuration.
5. **Response**: Returns 200 OK on success.

## Tasks / Subtasks

- [ ] Create Pydantic Models (AC: 2)
  - [ ] Create `backend/models/domain.py`
  - [ ] Define `GlobalConfig`, `JobConfig`, `AgentConfig`, `SimulationConfig` matching Tech Spec.
- [ ] Implement Initialization Logic (AC: 3, 4)
  - [ ] Update `backend/core/state.py` to add `initialize(config)` method.
  - [ ] Ensure `initialize` replaces the current singleton instance or resets its fields.
- [ ] Create API Endpoint (AC: 1, 5)
  - [ ] Create `backend/api/config.py` router.
  - [ ] Implement `POST /` handler calling `state.initialize`.
  - [ ] Register router in `backend/main.py`.
- [ ] Add Unit Tests
  - [ ] Test payload validation (valid/invalid cases).
  - [ ] Test state reset functionality (ensure old state is gone).

## Dev Notes

- **Architecture**:
  - `backend/models/domain.py` is the single source of truth for config schema.
  - `backend/core/state.py` holds the `WorldState` singleton.
  - `backend/api/config.py` handles the HTTP interface.
- **Data Models**:
  - Refer to Tech Spec for exact Pydantic definitions.
  - `JobConfig`: `job_id`, `resource_produced`
  - `AgentConfig`: `count`, `job_id`, `culture`, `needs`, `wants`, `income`
- **Error Handling**: FastAPI automatically handles Pydantic validation errors (422). Ensure business logic errors (e.g., agent referring to non-existent job ID) raise `HTTPException(400, ...)`.

### Project Structure Notes

- New file: `backend/models/domain.py`
- New file: `backend/api/config.py`
- Modified file: `backend/core/state.py`
- Modified file: `backend/main.py`

### References

- [Source: docs/epics.md#Story 2.4: Backend Configuration Endpoint]
- [Source: docs/sprint-artifacts/tech-spec-epic-2.md#Data Models and Contracts]

## Dev Agent Record

### Context Reference

<!-- Path(s) to story context XML will be added here by context workflow -->

### Agent Model Used

Gemini 2.5 Flash

### Debug Log References

### Completion Notes List

### File List

## Change Log

- **[2025-12-08]**: Initial draft created by SM Agent (YOLO mode).
