# Project Brief: AIES - AI Economy Simulator

## 1. Project Overview

**Project Name:** AIES: AI Economy Simulator

**Summary:** AIES is a web-based simulation platform where Large Language Models (LLMs) act as autonomous economic agents with hidden information. The primary purpose is to enable researchers to study emergent economic and social behaviors—such as negotiation, trust formation, and their effects on reservation prices—that arise from nuanced, human-like interactions. Unlike traditional agent-based models with rigid rules, AIES leverages LLMs to simulate behavior driven by culture, needs, and imperfect information.

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

## 4. Scope

### In-Scope (Minimum Viable Product - MVP)
-   **Simulation Setup:** Global, per-job, and per-agent configuration for parameters like temperature, day length, agent count, income, culture, needs, and wants.
-   **Real-Time Dashboard:**
    -   Agent interaction diagram.
    -   Detailed panel for selected agents.
    -   Global settings display.
    -   Graph for subjective economic value over time.
    -   A chronological event log with an export feature.
-   **Core Simulation Engine:**
    -   Negotiation-based turn engine with an "event budget" for agents.
    -   LLM-powered evaluation of trade offers.
    -   Handling of edge cases like timeouts and invalid offers.
    -   Initial economy with predefined jobs and resource production.
-   **Technology:** Next.js frontend, FastAPI backend, and Google AI (Gemini) for LLM integration.

### Out-of-Scope (Optional Extensions)
-   Trust system between agents.
-   Advanced roles (e.g., Merchants, Financiers).
-   Tiered production chains (Level 1 resources).
-   Advanced data visualizations (e.g., wealth distribution).
-   User participation mode.
-   Database integration for saving/loading simulations.
-   User authentication.

## 5. Key Deliverables

1.  **AIES Web Application:** A fully functional, deployed web platform accessible via modern browsers.
2.  **Simulation Engine:** The backend engine capable of running and managing the economic simulations.
3.  **Monitoring Dashboard:** The interactive frontend for real-time visualization and monitoring.
4.  **Exportable Event Logs:** Comprehensive log files in a format suitable for external analysis.
5.  **Project Documentation:**
    -   API documentation (OpenAPI/Swagger).
    -   User guide for setting up and running simulations.
    -   System architecture diagrams.

## 6. Technology Stack

-   **Frontend:** Next.js 14+, TypeScript, Tailwind CSS, shadcn/ui, Recharts, Zustand.
-   **Backend:** FastAPI (Python).
-   **AI Integration:** Pydantic-AI with Gemini models.
-   **Build/Package Management:** UV (Python).
-   **Deployment:** Vercel (Frontend), a suitable backend hosting service.

## 7. Timeline & Milestones

The project follows the 4-phase BMAD methodology over 5 weeks.

-   **Weeks 44 (Phase 1 & 2): Analysis & Planning**
    -   **Deliverables:** Requirements document, prioritized backlog, risk register.
-   **Weeks 45-46 (Phase 3): Solution Architecture & UI/UX Design**
    -   **Deliverables:** Data models, API specification, architecture diagrams, UI mockups, interactive prototype.
-   **Weeks 47-48 (Phase 4): Development & Deployment**
    -   **Deliverables:** Fully functional, tested, and deployed AIES platform with complete documentation.

## 8. Risks and Assumptions

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
