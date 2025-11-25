# Project Requirements Document: AIES - AI Economy Simulator

## 1. Introduction

### 1.1. Project Overview
AIES (AI Economy Simulator) is a web-based research platform designed to simulate economic and social behaviors using Large Language Models (LLMs) as autonomous agents. Unlike traditional agent-based models, which rely on predefined rules, AIES empowers agents to make decisions based on nuanced factors like culture, needs, and hidden information, allowing for the study of emergent, human-like interactions.

### 1.2. Problem Statement
Economic and social researchers lack accessible tools to study the emergent behaviors that arise from complex, information-asymmetric interactions. Existing models are often too rigid to capture the subtleties of human negotiation, trust formation, and subjective value assessment. AIES will bridge this gap by providing a configurable environment where these complex dynamics can be simulated, monitored, and analyzed.

### 1.3. Goals & Objectives
The primary goal is to create a robust and user-friendly platform for economic and social research.

**Key Objectives:**
*   **Build a configurable simulation engine:** Enable researchers to define and run simulations with specific global, job-related, and agent-specific parameters.
*   **Implement realistic agent behavior:** Utilize LLMs to drive agent decisions, fostering emergent and unpredictable negotiation strategies.
*   **Provide insightful real-time monitoring:** Develop an interactive dashboard to visualize agent interactions, economic metrics, and system events as they unfold.
*   **Generate research-ready data:** Ensure all simulation events are logged and can be easily exported for detailed post-hoc analysis.

### 1.4. Non-Goals (Post-MVP)
The initial release will not include:
*   A persistent trust system between agents.
*   Advanced economic roles like merchants or financiers.
*   Multi-tiered production chains.
*   User authentication or the ability to save/load simulation states.

## 2. User Personas

*   **Dr. Anya Sharma (Primary Persona):** A university researcher in behavioral economics. She needs a tool to test hypotheses about negotiation and trust without spending months on custom software development. She is tech-savvy but not a programmer. She values ease of setup, real-time feedback, and high-quality data output for her publications.
*   **Ben Carter (Secondary Persona):** A graduate student in computational sociology. He is exploring how cultural attributes affect market dynamics. He needs a platform that is flexible enough to model custom social parameters and can handle a moderate number of agents for his dissertation research.

## 3. Functional Requirements (MVP)

### 3.1. Simulation Setup & Configuration
Users must be able to configure the simulation environment before execution.

*   **FR1.1: Global Configuration:** Users can set global parameters that apply to the entire simulation, including:
    *   `simulation_day_length_seconds`: Duration of a simulation day in real-time seconds.
    *   `max_days`: The total number of days the simulation will run.
    *   `agent_count`: The total number of agents in the economy.
*   **FR1.2: Job & Resource Configuration:** Users can define the available jobs and the resources they produce. At least two initial jobs (e.g., "Woodcutter," "Stonemason") must be pre-configured.
*   **FR1.3: Agent Configuration:** For each agent, users can specify:
    *   `agent_id`: A unique identifier.
    *   `job`: The agent's assigned profession.
    *   `culture`: A descriptive string influencing behavior (e.g., "Cooperative," "Aggressive").
    *   `needs`: A dictionary of essential resources and their importance (e.g., `{"food": 10, "water": 10}`).
    *   `wants`: A dictionary of desirable resources (e.g., `{"tools": 5}`).
    *   `income`: The daily income received by the agent.

### 3.2. LLM-Powered Agent Logic
The core of the simulation relies on LLM-driven decisions, which must be structured and reliable.

*   **FR2.1: Structured LLM Communication:** All communication between the simulation engine and the LLM must use `pydantic-ai` to ensure that LLM outputs conform to predefined Pydantic models. This applies to all agent decision points.
*   **FR2.2: Negotiation Turn Engine:** The simulation will proceed in turns, where each agent has an "event budget" per day to perform actions (e.g., initiate a trade, respond to an offer).
*   **FR2.3: Agent Decision Making:** LLMs will power the following key decisions for each agent:
    *   **Trade Partner Selection:** Choose a potential partner to negotiate with.
    *   **Resource Request:** Decide which resource to seek in a trade.
    *   **Offer Generation:** Propose a trade offer (e.g., "I will give you 10 wood for 5 stone").
    *   **Offer Evaluation:** Assess an incoming offer and decide whether to accept, reject, or propose a counter-offer.
*   **FR2.4: Error Handling:** If the LLM fails to produce a valid, structured response for a decision (as validated by `pydantic-ai`), the current negotiation action for that agent will fail cleanly without crashing the simulation.

### 3.3. Real-Time Monitoring Dashboard
A web-based dashboard must provide real-time insights into the running simulation.

*   **FR3.1: Agent Interaction Diagram:** A dynamic graph visualization showing which agents are currently interacting or have recently interacted.
*   **FR3.2: Agent Inspector Panel:** Clicking on an agent in the diagram reveals a detailed panel displaying their current inventory, job, culture, needs/wants, and recent activity.
*   **FR3.3: Global Economic Indicators:** A time-series graph showing the change in a global metric, such as total subjective economic value, over the course of the simulation.
*   **FR3.4: Live Event Log:** A chronological feed of all major simulation events (e.g., "Agent A started negotiation with Agent B," "Trade of 10 wood for 5 stone accepted").

### 3.4. Data Export
Research-ready data must be exportable from the application.

*   **FR4.1: Export Event Log:** Users must be able to export the entire event log from the dashboard as a CSV file for offline analysis.

## 4. Technical Requirements

### 4.1. Technology Stack
*   **Frontend:** Next.js 14+, TypeScript, Tailwind CSS, shadcn/ui, Recharts.
*   **Backend:** FastAPI (Python), UV for package management.
*   **AI Integration:** `pydantic-ai` with Google Gemini models.
*   **State Management (Frontend):** Zustand.
*   **Deployment:** Vercel (Frontend), a suitable Python-compatible hosting service for the backend (e.g., Render, Fly.io).

### 4.2. Performance & Reliability
*   **TR2.1: Minimal Latency:** The `pydantic-ai` integration should add minimal overhead to LLM API calls to ensure a smooth simulation flow.
*   **TR2.2: API Rate Limiting:** The backend should gracefully handle potential API rate limits from the LLM provider, logging warnings without failing the entire simulation.

## 5. Success Metrics

*   **SM1: End-to-End Simulation Run:** Successfully run a 10-agent simulation for 5 days without critical errors.
*   **SM2: Emergent Behavior Observation:** Observe at least one instance of non-trivial emergent behavior (e.g., an agent consistently negotiating for higher prices than others).
*   **SM3: Data Integrity:** The exported CSV log must accurately reflect all events that occurred during the simulation.
*   **SM4: User Feedback:** Primary persona (Dr. Sharma) confirms that the platform is intuitive and that the exported data is useful for her research needs.

## 6. Risks and Mitigation

| Risk | Likelihood | Impact | Mitigation Strategy |
| :--- | :--- | :--- | :--- |
| **LLM Unpredictability** | Medium | High | Use low temperature settings in LLM configuration and employ robust prompt engineering with few-shot examples. Rely on `pydantic-ai` to enforce output structure. |
| **API Costs & Rate Limits** | High | Medium | Implement prompt optimization to reduce token count. Add caching for identical, deterministic LLM calls. Monitor API usage closely. |
| **Frontend Performance** | Medium | Medium | Use efficient rendering libraries (e.g., Recharts) and virtualized lists for the event log. Optimize data payload streamed to the frontend. |
| **Scope Creep** | High | High | Strictly adhere to the MVP feature set defined in this document. All new feature requests must be deferred to a post-MVP backlog. |
