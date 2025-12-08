# Story 3.2: Agent Decision: Trade Partner Selection

Status: drafted

## Story

As a **Researcher**,
I want **agents to intelligently select who to trade with**,
so that **market networks emerge organically.**

## Acceptance Criteria

1. **Valid Agent Selection:** Agent outputs a valid `agent_id` from the provided list of available agents.
2. **Rational Selection Logic:** Selection logic shows basic rationality (e.g., a hungry agent selects a Farmer, or an agent needing wood selects a Woodcutter).
3. **Structured Output:** The output conforms strictly to the `TargetSelection` Pydantic model.

## Tasks / Subtasks

- [ ] Define Data Models (AC: 1, 3)
  - [ ] Create `TargetSelection` model in `backend/models/decisions.py` with `agent_id` and `reasoning`.
- [ ] Implement Decision Logic (AC: 1, 2)
  - [ ] Create `decide_partner` function in `backend/agents/decisions.py`.
  - [ ] Implement prompt template in `backend/agents/prompts.py` that injects:
    - Agent's internal state (Needs, Inventory).
    - Public market state (List of other agents, their jobs, and visible inventory).
- [ ] Integrate with Agent Class (AC: 2)
  - [ ] Update `backend/agents/implementation.py` to include the `decide_partner` step in the agent's turn logic.
- [ ] Testing (AC: 1, 2, 3)
  - [ ] Unit Test: Verify `TargetSelection` model validation rejects invalid agent IDs or missing fields.
  - [ ] Unit Test: Mock LLM response to return a specific `agent_id` and verify `decide_partner` parses it correctly.
  - [ ] Integration Test (Mocked): Run a "synthetic" turn where an agent with specific needs (e.g., 0 Food) is presented with a Farmer and a Stonemason, and assert the prompt contains the correct context (though actual selection depends on LLM, the prompt construction can be verified).

## Dev Notes

- **Architecture:** This story implements part of the "Cognitive Engine" using `pydantic-ai` and Google Gemini.
- **Dependencies:** This story depends on **Story 3.1 (LLM Integration Infrastructure)** for the `pydantic-ai` client setup. Ensure 3.1 is implemented or stubbed before fully integrating.
- **State Management:** Agents are stateless between turns regarding the LLM context. We must pass the *full* relevant state (internal + public market) in the prompt for every decision.
- **Penalty Box:** While full error handling is Story 3.5, this implementation should allow exceptions to propagate (or simple try/catch) so the Engine can handle them later. Focus on the happy path and validation errors here.

### Project Structure Notes

- `backend/models/decisions.py`: New file for decision-related Pydantic models.
- `backend/agents/decisions.py`: New file for decision logic functions.
- `backend/agents/prompts.py`: New file for prompt templates.

### References

- [Source: docs/sprint-artifacts/tech-spec-epic-3.md#Detailed-Design] (Data Models and Workflows)
- [Source: docs/epics.md#Epic-3-Autonomous-Agent-Intelligence] (Story 3.2 definition)
- [Source: docs/architecture.md#9-Data-Architecture] (Agent and WorldState models)

## Dev Agent Record

### Context Reference

<!-- Path(s) to story context XML will be added here by context workflow -->

### Agent Model Used

Gemini 2.5 Flash

### Debug Log References

### Completion Notes List

### File List
