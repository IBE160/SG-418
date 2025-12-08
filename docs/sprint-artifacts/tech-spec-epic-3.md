# Epic Technical Specification: Autonomous Agent Intelligence

Date: Monday, December 8, 2025
Author: BIP
Epic ID: 3
Status: Draft

---

## Overview

This epic introduces the core "intelligence" of the simulation: enabling agents to autonomously negotiate and trade using Large Language Models (LLMs). It transitions the agents from static state containers to active decision-makers that can analyze their needs, identify trade partners, formulate rational offers, and evaluate counter-offers. This epic also establishes the critical infrastructure for structured LLM communication using `pydantic-ai` and Google Gemini.

## Objectives and Scope

### In-Scope
*   **LLM Integration Infrastructure:** Setting up `pydantic-ai` with Google Gemini to ensure strictly structured JSON outputs.
*   **Trade Partner Selection:** Agents analyzing the global market state to choose a trading partner.
*   **Offer Generation:** Agents creating specific trade proposals (resource, amount, price/exchange) based on internal needs.
*   **Offer Evaluation:** Agents deciding to Accept, Reject, or Counter an incoming offer based on utility.
*   **Structured Communication:** All agent interactions must conform to strict Pydantic models (Input Prompts and Output Responses).
*   **Error Handling (The "Penalty Box"):** Robust handling of LLM hallucinations, timeouts, or invalid JSON, ensuring single-agent failures do not crash the simulation.

### Out-of-Scope
*   **Long-term Memory:** Agents do not yet need to remember *past* interactions (history), only current state (MVP).
*   **Complex Social Dynamics:** No alliances, gossip, or reputation systems yet.
*   **Multi-turn Negotiation:** Interaction is limited to Offer -> Response (Accept/Reject/Counter). Extended bargaining chains are for later.
*   **Chat/Natural Language Generation:** Agents communicate via structured data signals (offers), not free-text chat (for now).

## System Architecture Alignment

This epic implements the "Cognitive Engine" components defined in the Architecture Document.

*   **Backend (FastAPI + Pydantic-AI):** The core logic resides entirely in the backend.
*   **External Service (Google Gemini):** The system relies on the Gemini API for decision logic.
*   **Structured Data First:** We strictly avoid "chatty" LLM interactions. Inputs are rich context dumps; outputs are `pydantic` objects.
*   **Sync/Async Model:** The simulation engine (Epic 1) invokes agent decisions synchronously (from the engine's perspective) or asynchronously, but must wait for the decision before proceeding to the next agent (Turn-based).

## Detailed Design

### Services and Modules

*   **Agent Module (`backend/agents/`):**
    *   `implementation.py`: The `Agent` class implementation.
    *   `decisions.py`: Functions wrapping specific LLM calls (decide_partner, make_offer, etc.).
    *   `prompts.py`: Templates for constructing the context strings fed to the LLM.

*   **LLM Service (`backend/llm/`):**
    *   `service.py`: Wrapper around `pydantic-ai` client, handling API keys and retry logic.
    *   `safety.py`: Error handling and "Penalty Box" implementation.

### Data Models and Contracts

**Pydantic Models (`backend/models/decisions.py`):**

```python
class TargetSelection(BaseModel):
    agent_id: str = Field(..., description="The ID of the agent to approach.")
    reasoning: str = Field(..., description="Short explanation of why this target was chosen.")

class TradeOffer(BaseModel):
    offered_resource: str
    offered_amount: int
    requested_resource: str
    requested_amount: int
    reasoning: str

class DecisionEnum(str, Enum):
    ACCEPT = "ACCEPT"
    REJECT = "REJECT"
    COUNTER = "COUNTER"

class OfferResponse(BaseModel):
    decision: DecisionEnum
    counter_offer: Optional[TradeOffer] = None
    reasoning: str
```

### APIs and Interfaces

*   **Internal Python API:** The Engine calls the Agent.
    *   `agent.decide_partner(public_market_state: List[AgentPublicState]) -> TargetSelection`
    *   `agent.make_offer(target: AgentPublicState) -> TradeOffer`
    *   `agent.evaluate_offer(offer: TradeOffer, from_agent: AgentPublicState) -> OfferResponse`

*   **External API (Gemini):**
    *   Standard `POST` to Gemini API via `pydantic-ai`.

### Workflows and Sequencing

**The Agent Turn Cycle (Epic 3 Logic):**

1.  **Engine Trigger:** Engine calls `agent.take_turn()`.
2.  **Perception:** Agent gathers its internal state (Needs, Inventory) and visible market state (other agents' jobs/public inventory).
3.  **Partner Selection (Story 3.2):**
    *   LLM Input: "You are a [Job]. You need [Needs]. Market: [List]. Who do you trade with?"
    *   LLM Output: `TargetSelection`.
4.  **Offer Generation (Story 3.3):**
    *   LLM Input: "You chose [Target]. Formulate an offer."
    *   LLM Output: `TradeOffer`.
5.  **Interaction:** Engine routes offer to Target Agent.
6.  **Offer Evaluation (Story 3.4):**
    *   Target LLM Input: "Incoming offer [Offer]. Your state: [State]. Accept/Reject/Counter?"
    *   Target LLM Output: `OfferResponse`.
7.  **Resolution:** Engine executes the trade (swaps inventory) if Accepted.
8.  **Error Handling (Story 3.5):** If any step fails (API timeout, bad JSON), the agent "Waits" and the turn ends.

## Non-Functional Requirements

### Performance
*   **Latency:** Agent decisions should ideally resolve within 2-3 seconds. (Gemini Flash is recommended).
*   **Concurrency:** If the simulation scales, we may need to batch requests or run agents in parallel, but for MVP/Turn-based, serial execution is acceptable.

### Reliability
*   **Fault Tolerance:** A single agent's API failure must **never** crash the server. It must result in a `SKIP` turn.
*   **Validation:** `pydantic-ai` must guarantee that outputs match the schema. If not, it counts as a failure.

### Cost Management
*   **Token Usage:** Prompts should be concise. Avoid sending full chat history. Send only current state snapshot.
*   **Model Selection:** Use Gemini Flash (or equivalent efficient model) for high-frequency trading decisions.

## Acceptance Criteria (Authoritative)

**From Epic 3 Stories:**

1.  **Infrastructure (Story 3.1):**
    *   Integration with `pydantic-ai` is working.
    *   Valid JSON is returned from a test prompt.
    *   Invalid structure raises a caught exception.

2.  **Partner Selection (Story 3.2):**
    *   Agent outputs a valid `agent_id` from the provided list.
    *   Selection logic shows basic rationality (e.g., a hungry agent selects a Farmer).

3.  **Offer Generation (Story 3.3):**
    *   Agent generates a `TradeOffer` with valid resource names.
    *   Agent does not offer resources it doesn't have.

4.  **Evaluation (Story 3.4):**
    *   Agent returns `ACCEPT`, `REJECT`, or `COUNTER`.
    *   `ACCEPT` triggers a state update in the Engine (via Epic 1 logic).

5.  **Error Handling (Story 3.5):**
    *   Simulated API failure results in a "WAIT" action in the event log.
    *   Simulation continues to the next agent.

## Traceability Mapping

| Acceptance Criteria | Component | Module | Test Idea |
| :--- | :--- | :--- | :--- |
| Structured Output | Backend | `llm/service.py` | Unit test: Mock LLM response with valid/invalid JSON. |
| Partner Selection | Backend | `agents/decisions.py` | Test: Give agent specific needs, verify it picks a provider of that need. |
| Rational Offers | Backend | `agents/decisions.py` | Test: Ensure agent with 0 Food asks for Food. |
| Penalty Box | Backend | `core/engine.py` | Integration: Force an exception in agent logic; verify engine catches it. |

## Risks, Assumptions, Open Questions

*   **Risk:** LLM latency slows down the simulation significantly if run serially for many agents.
    *   *Mitigation:* MVP is small scale (10-20 agents). Future optimization: Parallel async requests.
*   **Risk:** "Rationality" is subjective. Agents might make "bad" trades.
    *   *Acceptance:* As long as they make *valid* trades, "bad" decisions are part of the simulation behavior to be studied, not necessarily a bug (unless it's hallucinated data).
*   **Assumption:** We are using Google Gemini models. API keys are available.

## Test Strategy Summary

*   **Unit Tests:**
    *   Test Pydantic models (validation logic).
    *   Mock the LLM client to test the `Agent` class logic flow without spending API credits.
*   **Integration Tests:**
    *   "Synthetic" Tests: Run a script where an Agent interacts with a Mock Agent to verify the handshake (Offer -> Eval -> Accept).
    *   Error Handling Test: Inject a failure and assert the system stays alive.
