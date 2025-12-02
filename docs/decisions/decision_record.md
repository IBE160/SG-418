# Architecture Decisions

## Decision 1: Real-Time Data Sync (The Nervous System)
**Category:** Communication Patterns
**Decision:** Short Polling (Client-initiated)
**Version:** HTTP/1.1 (Standard)
**Affects FR Categories:** Monitoring
**Rationale:**
*   **Simplicity:** Polling is the easiest pattern to implement ("Are we there yet?" every 1 second).
*   **Reliability:** If a request fails, the next one just retries. No complex connection management like WebSockets.
*   **Fit for Purpose:** For a simulation ticking every few seconds, sub-millisecond latency (WebSockets) is overkill.
**Provided by Starter:** No

## Decision 2: Simulation State Management (The Brain)
**Category:** State Management
**Decision:** Singleton Service in Memory (Python Global)
**Version:** Python 3.12+
**Affects FR Categories:** Simulation Engine
**Rationale:**
*   **Single Source of Truth:** The simulation is one continuous event. A Singleton ensures all agents live in the same "world".
*   **MVP Scope:** We explicitly excluded databases. In-memory is fast and sufficient for non-persistent runs.
*   **Simplicity:** No external dependencies (like Redis) required.
**Provided by Starter:** No

## Decision 3: Agent Logic Isolation (The Personality)
**Category:** Architecture Patterns
**Decision:** "Blind" Agent Interface Pattern
**Version:** Custom Pattern
**Affects FR Categories:** Agent Logic
**Rationale:**
*   **Integrity:** Agents should only "know" what they perceive.
*   **Implementation:** Agents receive a `Perception` object (limited data) and return an `Action` object. They never access the full `WorldState` directly.
*   **Research Validity:** Prevents data leakage where agents could act on hidden information.
**Provided by Starter:** No

## Decision 4: Error Handling Strategy (The Safety Net)
**Category:** Consistency Patterns
**Decision:** "Penalty Box" Failure Mode
**Version:** Pydantic-AI + Custom Middleware
**Affects FR Categories:** Agent Logic, Simulation Engine
**Rationale:**
*   **Resilience:** If an LLM fails (timeout, bad JSON), the simulation must not crash.
*   **Logic:** The failing agent "skips a turn" (does nothing).
*   **Feedback:** The error is logged to the dashboard so the researcher sees *why* the agent did nothing.
**Provided by Starter:** No
