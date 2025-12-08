# Story 3.4: Agent Decision: Evaluate Offer

Status: drafted

## Story

As a Researcher,
I want agents to accept, reject, or counter incoming offers,
so that negotiations are two-sided.

## Acceptance Criteria

1. Given an agent receives a `TradeOffer`
2. When it evaluates the offer
3. Then it should output a decision: `ACCEPT`, `REJECT`, or `COUNTER`
4. And the decision should increase the agent's utility (subjective value)
5. And the response follows the `OfferResponse` Pydantic model

## Tasks / Subtasks

- [ ] Define Response Models (AC: 1, 3, 5)
  - [ ] Add `DecisionEnum` (ACCEPT, REJECT, COUNTER) to `backend/models/decisions.py`
  - [ ] Add `OfferResponse` model (decision, counter_offer, reasoning) to `backend/models/decisions.py`
- [ ] Implement Evaluation Logic (AC: 2, 4)
  - [ ] Create prompt template for offer evaluation in `backend/agents/prompts.py`
  - [ ] Implement `decide_offer_response` in `backend/agents/decisions.py` using `pydantic-ai`
  - [ ] Expose `evaluate_offer` method in `backend/agents/implementation.py`
- [ ] Unit Testing (AC: 1, 3, 5)
  - [ ] Test Pydantic model validation for valid/invalid responses
  - [ ] Mock LLM to verify `evaluate_offer` returns correct structure

## Dev Notes

- **Architecture:** Follows "Cognitive Engine" pattern. `evaluate_offer` is a synchronous call from the Engine's perspective (though implementation may vary).
- **Models:**
    ```python
    class DecisionEnum(str, Enum):
        ACCEPT = "ACCEPT"
        REJECT = "REJECT"
        COUNTER = "COUNTER"

    class OfferResponse(BaseModel):
        decision: DecisionEnum
        counter_offer: Optional[TradeOffer] = None
        reasoning: str
    ```
- **Prompt Strategy:** The prompt must include:
    - The incoming offer details (who, what offered, what asked).
    - The agent's current state (inventory, needs).
    - A goal instruction: "Maximize your utility. If the offer helps you meet needs, accept. If it hurts, reject. If close, counter."
- **Dependencies:** Relies on `pydantic-ai` setup from Story 3.1.

### Project Structure Notes

- `backend/models/decisions.py`: Central location for all agent decision schemas.
- `backend/agents/decisions.py`: Pure functions for LLM interaction.
- `backend/agents/implementation.py`: Class-based interface called by Engine.

### References

- [Epics: Story 3.4](../epics.md#story-34-agent-decision-evaluate-offer)
- [Tech Spec: Data Models](../sprint-artifacts/tech-spec-epic-3.md#data-models-and-contracts)

## Dev Agent Record

### Context Reference

<!-- Path(s) to story context XML will be added here by context workflow -->

### Agent Model Used

Gemini 2.5 Flash

### Debug Log References

### Completion Notes List

### File List
