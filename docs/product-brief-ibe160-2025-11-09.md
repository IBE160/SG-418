# Product Brief: AIES - AI Economy Simulator

## 1. Executive Summary

The AI Economy Simulator (AIES) is a novel web-based platform designed to enable researchers to study emergent economic and social behaviors by simulating autonomous LLM agents with hidden information. Unlike traditional agent-based models, AIES leverages LLMs to introduce nuanced decision-making, negotiation, and the formation of trust, allowing for a deeper analysis of factors influencing reservation prices and economic outcomes. The project prioritizes a robust, scalable, and user-friendly system, built with a Python/FastAPI backend and a Next.js frontend, with a critical technical decision to utilize `pydantic-ai` for ensuring structured and reliable LLM outputs.

## 2. Problem Statement

Traditional economic simulations often rely on rigid, pre-defined rules for agent behavior, which fail to capture the complexity of human-like interactions, imperfect information, and emergent social dynamics. This limitation hinders the study of phenomena such as negotiation, trust, and the subtle influences on economic decisions like reservation prices. Furthermore, challenges exist in ensuring LLMs consistently adhere to instructions and produce reliable, structured outputs, which is crucial for the integrity of any LLM-driven simulation.

## 3. Product Description: AIES - AI Economy Simulator

AIES is a web application that provides a configurable environment for running economic simulations powered by Large Language Models. Researchers can define global simulation parameters (temperature, day length, day count), configure agents with specific jobs, incomes, cultures/personalities, needs, and wants. The platform features a real-time monitoring dashboard with an agent interaction diagram, detailed agent panels, a subjective economic value graph, and an event log. The core simulation engine employs a negotiation-based turn system, where LLM agents evaluate trade offers based on their internal states and goals, leading to emergent behaviors.

## 4. Target Users

*   **Primary Users:** Researchers in economics, sociology, and computer science; economists and social scientists studying market dynamics and behavior.
*   **Secondary Users:** Students and educators in relevant academic fields; policymakers interested in simulating economic scenarios.

## 5. Key Features (Minimum Viable Product - MVP)

### 5.1. Simulation Setup & Configuration
*   **Global Parameters:** Adjustable sliders for LLM response randomness (Temperature), maximum events per agent per day (Day Length), and total simulation duration (Day Count).
*   **Per-Job Configuration:** Set agent count and income for specific job roles.
*   **Per-Agent Configuration:** Assign cultural/personality profiles, and define resource needs and wants via sliders.

### 5.2. Real-Time Monitoring Dashboard
*   **Agent Interaction Diagram:** Visualizes agents as nodes and trades as directed edges.
*   **Selected Agent Panel:** Displays detailed information for a chosen agent (parameters, inventory, stats).
*   **Global Settings Panel:** Shows current simulation parameters.
*   **Subjective Economic Value Graph:** Time-series graph of agents' cumulative subjective economic value.
*   **Event Log:** Chronological log of all simulation events with export functionality.

### 5.3. Core Simulation Engine
*   **Negotiation-Based Turn Engine:** Agents have an event budget for actions, initiating negotiations to fulfill needs.
*   **LLM-Powered Offer Evaluation:** Agents (LLMs) evaluate trade offers based on internal state, goals, and negotiation history.
*   **Edge Case Handling:** Manages unresponsive agents, timeouts, and invalid offers.
*   **Initial Economy:** Agents start with predefined jobs producing foundational resources.

## 6. Technical Highlights

*   **Frontend:** Next.js 14+ (TypeScript), Tailwind CSS, shadcn/ui, Zustand, Recharts.
*   **Backend:** FastAPI (Python), Pytest, UV.
*   **AI Integration:**
    *   **Structured Output:** `pydantic-ai` is the chosen framework to force LLM responses into Pydantic models, ensuring type-safe, predictable, and validated data. This directly addresses the critical need for reliable LLM outputs identified in brainstorming.
    *   **LLM Service:** Google Gemini model via `pydantic-ai`'s model-agnostic Python library.
    *   **Error Handling:** Automatic negotiation rejection if LLM API fails or `pydantic-ai` validation fails.
    *   **Prompt Design:** System prompts define agent culture/goals; negotiation prompts include agent state and history. JSON schemas are injected by `pydantic-ai` to guide output format.
*   **Architecture:** Component-based frontend, RESTful API with WebSocket for real-time updates.
*   **No Database for MVP:** In-memory data handling for initial version.

## 7. Success Criteria

*   **Functional:** Users can configure and launch simulations; agents successfully negotiate and trade; dashboard provides clear views; event log is comprehensive.
*   **Technical:** Backend maintains stable performance with at least 20 agents; frontend visualizations update in real-time; LLM API integration is reliable.
*   **Research:** Simulation produces non-trivial emergent economic behaviors; reservation prices are demonstrably influenced by configurable factors.

## 8. Future Considerations (Nice-to-Have & Brainstorming Insights)

*   **Trust System:** Implement a trust score between agents.
*   **Advanced Roles:** Introduce Merchants, Financiers.
*   **Tiered Production:** Create more complex supply chains.
*   **Advanced Data Visualization:** Historical charts for wealth, scarcity, trust networks.
*   **Participation Mode:** User can act as an agent.
*   **Database Integration:** For saving/loading simulations (e.g., Supabase).
*   **Prompt Quality Checklist:** Develop best practices for prompt specificity and consistency.
*   **Debugging Test Harness:** Build an environment to test agent logic in isolation.
*   **"Agent Economy" Game Pivot:** A moonshot idea to redesign the project around a measurable goal where agents "get rich," involving currency and performance-based testing.

## 9. High-Level Timeline

The project follows the BMAD-methodology 4-phase model over 5 weeks:
*   **Phase 1 & 2 (Analyze & Planning):** 1 week (Week 44) - Requirements, planning, risk analysis.
*   **Phase 3 (Solution Architecture & UI/UX Design):** 2 weeks (Week 45-46) - Data models, API design, system architecture, wireframing, mockups.
*   **Phase 4 (Development & Deployment):** 2 weeks (Week 47-48) - Core development, testing, deployment.
