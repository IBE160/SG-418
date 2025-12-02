# Architectural Decisions Plan

**Facilitation Mode:** Beginner
*   *Goal:* Explain technical choices using analogies (The Brain, The Nervous System, The Heartbeat).
*   *Focus:* Simplicity and "Boring Technology" to ensure success.

**Decision Priority List:**

1.  **CRITICAL: Real-Time Data Sync (The Nervous System)**
    *   *Context:* How does the dashboard get updates? (Polling vs. SSE)
    *   *Why:* Defines the "Live Discovery" experience.

2.  **CRITICAL: Simulation State Management (The Brain)**
    *   *Context:* Where does the simulation live? (Singleton vs. Global)
    *   *Why:* Determines how robust the simulation is.

3.  **IMPORTANT: Agent Logic Isolation (The Personality)**
    *   *Context:* How to prevent agents from "cheating" by seeing global data?
    *   *Why:* Essential for valid research results.

4.  **IMPORTANT: Error Handling Strategy (The Safety Net)**
    *   *Context:* What happens when an LLM crashes?
    *   *Why:* Prevents one agent breaking the whole economy.

**Next Steps:**
We will step through these decisions one by one to build the architecture.
