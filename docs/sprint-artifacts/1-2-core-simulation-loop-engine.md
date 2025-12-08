# Story 1.2: Core Simulation Loop (Engine)

Status: drafted

## Story

As a **Researcher**,
I want **the simulation to advance in discrete "turns" or "ticks"**,
so that **agents have a structured opportunity to act.**

## Acceptance Criteria

1.  **Engine Module**: `backend/core/engine.py` exists and contains a `SimulationEngine` class.
2.  **Tick Logic**: A `tick()` method increments the `current_tick` counter in the global state.
3.  **Day Cycle**: When `current_tick` reaches the configured `ticks_per_day`, the `current_day` increments.
4.  **Daily Reset**: On a new day, a method/hook is called to reset agent budgets (placeholder/stub allowed if agents undefined).
5.  **State Updates**: All changes are reflected in the `WorldState` object.
6.  **Testing**: Unit tests verify tick increments and day transitions.

## Tasks / Subtasks

- [ ] Scaffold Engine Module
  - [ ] Create `backend/core/engine.py`
  - [ ] Define `SimulationEngine` class
- [ ] Implement Time Logic
  - [ ] Implement `tick()` method
  - [ ] Add logic to check `ticks_per_day` threshold
  - [ ] Implement `_advance_day()` private method
- [ ] Integrate with State (Stub/Basic)
  - [ ] Ensure `tick()` updates a `WorldState` instance (even if mocked/local for now)
- [ ] Implement Testing
  - [ ] Create `backend/tests/test_engine.py`
  - [ ] Test: `test_tick_increments_counter`
  - [ ] Test: `test_day_transition`
  - [ ] Test: `test_daily_reset_trigger`

## Dev Notes

- **Architecture**: This module (`backend/core/engine.py`) is the heartbeat of the application.
- **State Dependency**: This story closely relates to Story 1.3 (State Management). Since 1.3 is not yet done, you may need to define a minimal `WorldState` Pydantic model in `backend/models/domain.py` or `backend/core/state.py` to make the engine functional.
- **Configuration**: `ticks_per_day` should ideally come from a config object. For this story, a constant or simple class attribute is acceptable until Epic 2.
- **Concurrency**: The `tick()` method itself should be synchronous logic, but designed to be called from an asyncio loop (e.g., via `fastapi` lifespan or background task).
- **Project Structure**:
    - `backend/core/` for the engine logic.
    - `backend/models/` for the state/config definitions.
    - `backend/tests/` for `pytest`.

### References

- **Tech Spec**: [Source: docs/sprint-artifacts/tech-spec-epic-1.md#Detailed-Design]
- **Architecture**: In-Memory Singleton Pattern.

## Dev Agent Record

### Context Reference

### Agent Model Used

Gemini 2.0 Flash

### Debug Log References

### Completion Notes List

### File List
