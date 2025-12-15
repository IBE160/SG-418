# Story 3.3: Agent Decision: Generate Offer

Status: drafted

## Story

As a **Researcher**,
I want **agents to formulate specific trade proposals**,
So that **economic exchange can occur.**

## Acceptance Criteria

1. **Offer Structure:** Agent generates a `TradeOffer` containing:
    - `offered_resource` (string)
    - `offered_amount` (int)
    - `requested_resource` (string)
    - `requested_amount` (int)
    - `reasoning` (string)
2. **Rationality:** The offer reflects the agent's internal state (e.g., an agent with high "Hunger" requests "Food").
3. **Validity:** The agent does not offer resources it does not possess (inventory check).
4. **Target Context:** The offer is formulated with awareness of the selected target (from Story 3.2 output).

## Tasks / Subtasks

- [ ] **Define Data Models**
  - [ ] Update `backend/models/decisions.py` to include `TradeOffer` Pydantic model.
  - [ ] Ensure fields match `pydantic-ai` requirements.

- [ ] **Create Prompt Template**
  - [ ] Add `OFFER_GENERATION_PROMPT` to `backend/agents/prompts.py`.
  - [ ] Template should include: Agent's Inventory, Agent's Needs, Target Agent's Public Info (Job).

- [ ] **Implement Decision Logic**
  - [ ] Create `make_offer` function in `backend/agents/decisions.py`.
  - [ ] Wire up `pydantic-ai` client with the prompt and model.
  - [ ] Add pre-computation logic: Check inventory before sending prompt? OR Check inventory after LLM response? (Architecture preference: LLM should know inventory, but code should validate).
  - [ ] Implement validation logic: If `offered_amount` > `current_inventory`, adjust or fail.

- [ ] **Update Agent Class**
  - [ ] Add `make_offer(self, target: AgentPublicState)` method to `Agent` class in `backend/agents/implementation.py`.
  - [ ] Ensure it delegates to `decisions.py`.

- [ ] **Testing**
  - [ ] **Unit Test:** `tests/agents/test_decisions.py` - Mock LLM to return a fixed `TradeOffer`. Verify parsing.
  - [ ] **Logic Test:** Verify inventory validation prevents offering phantom resources.
  - [ ] **Integration Test:** `tests/agents/test_flow.py` - Setup an agent with 0 Food, 10 Wood. Verify it asks for Food and offers Wood (using mocked or real LLM).

## Dev Notes

- **Architecture Alignment:**
  - Logic resides in `backend/agents/decisions.py` to keep `Agent` class clean.
  - Models in `backend/models/decisions.py` shared with Pydantic-AI.
- **Dependencies:**
  - Requires `pydantic-ai` setup from Story 3.1.
  - Input relies on `TargetSelection` from Story 3.2 (or mock for dev).
- **Error Handling:**
  - If LLM returns invalid JSON, `pydantic-ai` raises exception.
  - For this story, let the exception propagate (caught by Engine in Story 3.5).
- **Rationality:**
  - We are not hard-coding rules. We rely on the LLM's "reasoning" field to explain why it made the trade.

### References

- [Tech Spec Epic 3](../sprint-artifacts/tech-spec-epic-3.md)
- [Architecture Decision: "Blind" Interface](../architecture.md#3-decision-summary-table)
