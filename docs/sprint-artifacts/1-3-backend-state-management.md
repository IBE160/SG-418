# Story 1.3: Backend State Management

Status: drafted

## Story

As a **Developer**,
I want **a centralized in-memory store for the simulation state**,
so that **all components (and the frontend) access the same source of truth.**

## Acceptance Criteria

1. **Given** the application has started, **When** the state is accessed via the internal module, **Then** I should receive the singleton `WorldState` object.
2. **Given** the state is modified (e.g., tick incremented), **When** it is accessed again from a different request context, **Then** the modifications should be visible (persistence across requests).
3. **Given** the server is restarted, **When** the state is accessed, **Then** it should be reset to initial values (verifying in-memory only nature).
4. The `WorldState` model must include fields for `current_tick`, `current_day`, `is_running`, and `last_updated`.

## Tasks / Subtasks

- [ ] Define Domain Models
  - [ ] Create `backend/models/domain.py` (or check if exists)
  - [ ] Implement `WorldState` Pydantic model with fields: `current_tick` (int), `current_day` (int), `is_running` (bool), `last_updated` (float)
- [ ] Implement State Singleton
  - [ ] Create `backend/core/state.py`
  - [ ] Instantiate a global `world_state` instance of `WorldState`
  - [ ] Create a dependency function `get_world_state()` for FastAPI injection (if needed) or direct import pattern
- [ ] Testing
  - [ ] Create `tests/test_state.py`
  - [ ] Verify state updates persist between function calls
  - [ ] Verify default values on initialization

## Dev Notes

- **Architecture Pattern**: In-Memory Singleton (Decision #3). We are explicitly NOT using a database.
- **Concurrency**: Since we are using FastAPI (async), be mindful of race conditions if multiple requests modify state. For MVP, Python's GIL and single-worker `uvicorn` make simple assignment relatively safe, but consider using a lock if concurrent writes are expected (unlikely for simple tick loop).
- **Files**:
    - `backend/models/domain.py`: Use Pydantic `BaseModel`.
    - `backend/core/state.py`: The module that holds the global variable.

### Project Structure Notes

- Ensure `backend/` follows the `src` layout or flat layout as initialized in Story 1.1.
- Models should be in `backend/models/` to avoid circular imports.

### References

- [Source: docs/epics.md#Story-1.3-Backend-State-Management]
- [Source: docs/sprint-artifacts/tech-spec-epic-1.md#Data-Models-and-Contracts]

## Dev Agent Record

### Context Reference

<!-- Path(s) to story context XML will be added here by context workflow -->

### Agent Model Used

Gemini-2.5-Flash

### Debug Log References

### Completion Notes List

### File List
