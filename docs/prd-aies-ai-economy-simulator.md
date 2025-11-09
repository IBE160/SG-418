# Product Requirements Document: AIES - AI Economy Simulator

## 1. Introduction

The AI Economy Simulator (AIES) is a web-based platform designed for researchers to study emergent economic and social behaviors in Large Language Model (LLM) agents. Unlike traditional rule-based simulations, AIES leverages LLMs to drive agent behavior, allowing for the observation of nuanced interactions such as negotiation, trust formation, and their impact on reservation prices. The platform aims to provide a robust and user-friendly environment for economic research, enabling the analysis of complex human-like behaviors in a controlled, simulated economy.

## 2. Goals and Objectives

The main goal of this project is to create a robust and user-friendly platform for economic research.

**Key Objectives:**
-   **Develop a configurable simulation engine:** Allow users to set up and run economic simulations with customizable global, job-specific, and agent-specific parameters.
-   **Enable LLM-powered agents:** Implement agents whose decisions are driven by LLMs, allowing for emergent and unpredictable behaviors.
-   **Provide real-time monitoring:** Create an interactive dashboard to visualize agent interactions, track economic value, and log events as they happen.
-   **Produce research-ready data:** Ensure that the simulation generates comprehensive logs that can be exported for detailed post-simulation analysis.
-   **Validate research potential:** Demonstrate that the simulation can produce non-trivial emergent behaviors and show that reservation prices are influenced by configurable factors.

## 3. Target Audience

-   **Primary:** Researchers in economics, sociology, and computer science; economists studying market dynamics.
-   **Secondary:** Students, educators, and policymakers interested in simulating economic scenarios.

## 4. Scope (Minimum Viable Product - MVP)

### In-Scope Features:

-   **Simulation Setup & Configuration:**
    -   **Global Simulation Parameters:**
        -   Temperature (slider): Controls LLM response randomness.
        -   Day Length (slider): Sets max events per agent per day.
        -   Day Count (slider): Defines total simulation days.
    -   **Per-Job Configuration:**
        -   Agent Count (slider): Number of agents per job.
        -   Agent Income (slider): Income for agents with a specific job.
    -   **Per-Agent Configuration:**
        -   Culture/Personality (dropdown/text): Assign cultural/personality profile.
        -   Needs (sliders): Set required resource levels.
        -   Wants (sliders): Set desired resource levels.

-   **Real-Time Monitoring Dashboard:**
    -   Agent Interaction Diagram: Real-time visualization of agents and trades.
    -   Selected Agent Panel: Detailed info for a selected agent (parameters, inventory, stats).
    -   Global Settings Panel: Displays current global simulation parameters.
    -   Subjective Economic Value Graph: Time-series graph of agents' cumulative subjective economic value.
    -   Event Log: Chronological, scrollable log of events with export option.

-   **Core Simulation Engine:**
    -   Negotiation-Based Turn Engine:
        -   Event Budget: Limited actions per day for strategic decision-making.
        -   Negotiation Flow: Structured process for trade initiation, offers, counter-offers, acceptance, rejection.
    -   LLM-Powered Offer Evaluation: Agents evaluate offers based on internal state, goals, and history.
    -   Edge Case Handling: Manages unresponsive agents, timeouts, invalid offers.
    -   Initial Economy: Predefined jobs producing Level 0 resources with set income.

## 5. Key Features / User Stories

### User Flow 1: Researcher Configures and Runs a Simulation

1.  **Entry Point:** Researcher opens the web application.
2.  **Set Global Parameters:** The user adjusts sliders for global Temperature, Day Length (event budget), and Day Count.
3.  **Configure Jobs:** The user sets the Agent Count and Income for each job.
4.  **Configure Agents:** The user selects individual agents to assign a specific Culture/Personality and adjust their Needs and Wants for various resources.
5.  **Start Simulation:** The user clicks a "Start Simulation" button.
6.  **Exit Point:** The system initializes the simulation, and the user is taken to the real-time monitoring dashboard.

### User Flow 2: Researcher Monitors and Analyzes the Simulation

1.  **Entry Point:** The simulation is running, and the monitoring dashboard is active.
2.  **Observe Interactions:** The user watches the Agent Interaction Diagram to see trades happening in real-time.
3.  **Inspect Agent:** The user clicks on an agent in the diagram. The Selected Agent Panel populates with that agent's detailed stats and inventory.
4.  **Track Value:** The user monitors the Subjective Economic Value Graph to see how agents' valuations of trades evolve.
5.  **Review Events:** The user scrolls through the Event Log to trace the history of specific negotiations or agent actions.
6.  **Conclude Simulation:** Once the simulation ends (Day Count reached), a "Download Log" button appears.
7.  **Export Data:** The user clicks the button to save the complete event log locally for external analysis.
8.  **Exit Point:** The user opens the log file in their preferred analysis tool.

## 6. Non-Functional Requirements

### Performance
-   The simulation backend must handle numerous concurrent agent interactions without significant slowdown.
-   The frontend must render visualizations smoothly.

### Scalability
-   The architecture should allow for future expansion (e.g., more agents, complex economies).

### Reliability
-   LLM API integration must be reliable with proper error handling and fallback mechanisms.
-   Simulation logs must be accurate and complete.

### Usability
-   Intuitive user interface for configuration and monitoring.
-   Clear and understandable visualizations.

### Security
-   No user authentication for MVP, but future versions should consider it for data persistence.

### Maintainability
-   Codebase should be well-documented and follow established coding standards.

### Compatibility
-   Web-based application accessible via modern desktop browsers (Chrome 90+, Firefox 88+, Edge 90+, Safari 14+).
-   Target Devices: Desktop or laptop computers exclusively.

## 7. Technology Stack

-   **Frontend:** Next.js 14+, TypeScript, Tailwind CSS, shadcn/ui, Recharts, Zustand.
-   **Backend:** FastAPI (Python).
-   **AI Integration:** Pydantic-AI with Gemini models.
-   **Build/Package Management:** UV (Python).
-   **Deployment:** Vercel (Frontend), suitable backend hosting service.

## 8. AI Integration Specification

**AI Use Cases**:
1.  Trade Partner Selection
2.  Resource Request
3.  Request Evaluation
4.  Offer Generation
5.  Offer Evaluation

**Subjective Economic Value Tracking**:
-   Each trade offer receives an evaluation from both agents: "very good", "good", "neutral", "bad", or "very bad".
-   The final offer's evaluations are converted to numerical scores: +20, +10, 0, -10, -20 respectively.
-   Each agent maintains a running subjective economic value sum by adding these scores.
-   Unfulfilled needs contribute negative values to this sum.
-   This cumulative value is tracked over time and visualized in the Subjective Economic Value Graph.
-   **Key Design Rationale**: Using text evaluations instead of direct numerical scores ensures proper AI immersion in their roles.

**Implementation:**
-   **Model:** Gemini 2.5 pro/flash.
-   **Structured Output:** `pydantic-ai` will be used to ensure all LLM outputs strictly conform to predefined Pydantic models.
-   **Prompt Design:** System prompts will define agent culture, goals, and constraints. Prompts during negotiation will include agent state, goals, and negotiation history. Agents will not be told it's a simulation. `pydantic-ai` will inject JSON schemas into prompts. A **Prompt Quality Checklist** will be developed.
-   **Rate Limiting:** The simulation will pause to wait for refreshed limits.
-   **Fallback:** Automatic negotiation rejection if LLM API fails or `pydantic-ai` validation fails.

## 9. Success Criteria

### Functional Success:
-   Criterion 1: Users can configure and launch a simulation with a variety of global and agent-specific parameters.
-   Criterion 2: The simulation runs autonomously, with agents successfully negotiating and executing trades to fulfill their needs.
-   Criterion 3: The dashboard provides a clear, real-time, and understandable view of the simulation's state.
-   Criterion 4: The final event log is comprehensive and provides useful data for post-simulation analysis.

### Technical Success:
-   Criterion 5: The backend engine maintains stable performance with a moderate number of agents (at least 20).
-   Criterion 6: The frontend visualizations update in near real-time without lagging.
-   Criterion 7: LLM API integration is reliable, with proper error handling.

### Research Success:
-   Criterion 8: The simulation produces emergent economic behaviors that are non-trivial and worthy of study.
-   Criterion 9: The reservation price of goods is demonstrably influenced by configurable factors like agent culture, needs, and negotiation history.

## 10. Risks and Assumptions

### Risks
-   **LLM Consistency:** Agent behavior may be unpredictable.
    -   *Mitigation:* Use lower temperature settings and robust prompt engineering.
-   **API Rate Limits/Costs:** High usage may lead to disruptions or unexpected costs.
    -   *Mitigation:* Optimize prompts and monitor API usage.
-   **Frontend Performance:** Visualizing many agents may cause performance issues.
    -   *Mitigation:* Use efficient rendering libraries and optimize data streaming.
-   **Scope Creep:** "Nice to have" features could delay the MVP.
    -   *Mitigation:* Strictly adhere to the MVP scope.

### Assumptions
-   AI-assisted development will accelerate coding tasks.
-   The Gemini API will be consistently available and performant.
-   Modern web browsers will support all required technologies.
-   The 5-week timeline is sufficient for the MVP, given the focused scope and AI assistance.

## 11. Timeline & Milestones

The project follows the 4-phase BMAD methodology over 5 weeks.

-   **Weeks 44 (Phase 1 & 2): Analysis & Planning**
    -   **Deliverables:** Requirements document, prioritized backlog, risk register.
-   **Weeks 45-46 (Phase 3): Solution Architecture & UI/UX Design**
    -   **Deliverables:** Data models, API specification, architecture diagrams, UI mockups, interactive prototype.
-   **Weeks 47-48 (Phase 4): Development & Deployment**
    -   **Deliverables:** Fully functional, tested, and deployed AIES platform with complete documentation.
