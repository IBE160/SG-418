# Story 3.5: Agent Error Handling (The "Penalty Box")

Status: drafted

## Story

As a **System**,
I want **to handle cases where the LLM produces invalid output or crashes**,
so that **the entire simulation doesn't stop due to one agent's failure**.

## Acceptance Criteria

1.  **Graceful Failure Handling**: If the LLM returns an error, invalid JSON, or times out, the system must catch the exception.
2.  **Turn Forfeiture**: The failing agent's turn ends immediately with a default "WAIT" action.
3.  **Error Logging**: The specific error (e.g., `ValidationError`, `Timeout`) is logged to the simulation event stream with the Agent ID.
4.  **Simulation Continuity**: The simulation engine proceeds to the next agent's turn without crashing or halting.

## Tasks / Subtasks

- [ ] Implement Exception Handling in Agent Execution Loop
    - [ ] Wrap agent decision calls (Partner Selection, Offer, Evaluation) in a `try/except` block in `backend/core/engine.py` (or relevant execution controller).
    - [ ] Catch `pydantic_ai.ValidationError`, `json.JSONDecodeError`, and general `Exception`.
- [ ] Implement "Penalty Box" Logic
    - [ ] Define a fallback `Action.WAIT` or null-operation state.
    - [ ] Ensure the agent's state remains consistent (no partial updates if half-failed).
- [ ] Update Event Logging
    - [ ] Add support for error events in the `WorldState` event log.
    - [ ] Format: `[ERROR] Agent {id} failed: {error_message}`.
- [ ] Verify Simulation Continuity
    - [ ] Unit Test: Mock an agent that always raises an exception; verify simulation advances to next tick/agent.

## Dev Notes

### Architecture & Patterns
- **Pattern**: "Penalty Box" / Circuit Breaker for Agents.
- **Location**: `backend/core/engine.py` (Main Loop) and `backend/agents/implementation.py` (Safety wrappers).
- **Libraries**: `pydantic-ai` (for validation exceptions).

### Source Components
- `backend/core/engine.py`: The primary location for the try/except block.
- `backend/models/domain.py`: Ensure `Event` model can accommodate error types.

### Testing Standards
- **Integration Test**: Inject a "poison pill" mock agent into the engine and assert the engine survives.

### Project Structure Notes
- Adhere to established Python exception handling practices.
- Ensure error logs are exposed to the frontend event feed (Epic 4 dependency, but foundational work here).

## Dev Agent Record

### Context Reference
<!-- Path(s) to story context XML will be added here by context workflow -->

### Agent Model Used
Gemini 2.5 Flash

### Debug Log References

### Completion Notes List

### File List
