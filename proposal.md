## Case Title
AIES: AI Economy Simulator

## Background
Modeling complex economic and social systems is challenging because human behavior is often nuanced and driven by diverse motivations. Traditional agent-based models use rigid rules, failing to capture emergent behaviors that arise from imperfect information, negotiation, cultural values, and interpersonal dynamics like trust. The main benefit of LLM simulation over traditional simulations is that we can analyze how the reservation price depends on different factors, instead of hard-coding the reservation price as is done in traditional simulations.

## Purpose
To create a simulation platform where Large Language Models (LLMs) act as autonomous economic agents with hidden information. By defining agent motivations ("culture"), needs/desires, etc. through system prompts, the simulator will allow researchers to study emergent behaviors like negotiation, the formation of trust and the effects they have on the reservation price and the economic outcome.

## Target Users

**Primary Users:**
1.  Researchers in economics, sociology, and computer science
2.  Economists and social scientists studying market dynamics and behavior

**Secondary Users:**
1.  Students and educators in relevant academic fields
2.  Policymakers interested in simulating economic scenarios

## Core Functionality

### Must Have (MVP)

**1. Simulation Setup & Configuration:**
-   **Global Simulation Parameters:**
    -   **Temperature (slider):** Controls the randomness of LLM responses for all agents globally.
    -   **Day Length (slider):** Sets the maximum number of events an agent can perform per day (event budget).
    -   **Day Count (slider):** Defines the total number of days the simulation will run.
-   **Per-Job Configuration:**
    -   **Agent Count (slider):** Set the number of agents assigned to a specific job.
    -   **Agent Income (slider):** Define the income for agents with a specific job.
-   **Per-Agent Configuration:**
    -   **Culture/Personality (dropdown/text):** Assign a cultural or personality profile to an agent to influence its behavior.
    -   **Needs (sliders):** Set the required level of different resources for each agent.
    -   **Wants (sliders):** Set the desired level of different resources for each agent.

**2. Real-Time Monitoring Dashboard:**
-   **Agent Interaction Diagram:** A central, real-time visualization of agents as nodes and their interactions (trades) as directed edges. 
-   **Selected Agent Panel:** Displays detailed information for a selected agent, including its current parameters, resource inventory, and key stats.
-   **Global Settings Panel:** Shows the current global simulation parameters. The settings are configurable before the simulation starts.
-   **Subjective Economic Value Graph:** A scrollable time-series graph plotting each agent's cumulative subjective economic value over time. This value is calculated by: (1) converting accepted trade offer evaluations ("very good"=+20, "good"=+10, "neutral"=0, "bad"=-10, "very bad"=-20) to numerical scores, (2) adding these scores to the agent's running total, and (3) subtracting penalties for unfulfilled needs as negative values.
-   **Event Log:** A chronological, scrollable log of all significant simulation events (negotiations, trades, state changes), with an option to export the log locally.

**3. Core Simulation Engine:**
-   **Negotiation-Based Turn Engine:**
    -   **Event Budget:** Agents have a limited number of actions (events) per day, encouraging strategic decision-making. Event costs include initiating a trade or making an offer. Rejecting or accepting an offer is free to encourage efficiency. The event costs resemble real-life situations, where negotiating takes time but ensures better prices, while making quick decisions leads to some worse or fewer deals, but saves time for other, better deals.
    -   **Negotiation Flow:** Agents initiate negotiations to fulfill needs, assess potential partners, and exchange offers. The flow follows a structured process from request to rejection, acceptance, or counter-offer.
-   **LLM-Powered Offer Evaluation:**
    -   Agents (as LLMs) evaluate trade offers based on their internal state (inventory), goals (culture), and negotiation history. This allows for nuanced, context-aware decisions instead of hard-coded rules.
-   **Edge Case Handling:**
    -   The engine handles unresponsive agents, negotiation timeouts, and invalid offers by automatically failing the negotiation.
    -   Agents are restricted to one negotiation at a time to simplify resource management.
-   **Initial Economy:**
    -   The simulation starts with agents in predefined "jobs" that produce various Level 0 (foundational) resources with a set income per day.

### Nice to Have (Optional Extensions)

-   **Trust System:** Implement a trust score between agents that is updated based on negotiation outcomes and influences future decisions.
-   **Advanced Roles:** Introduce new roles like Merchants (who can see others' inventories), Financiers (who introduce money as a primary income source)
-   **Tiered Production:** Add level 1 resources that require level 0 resources to be produced, creating more complex supply chains.
-   **Advanced Data Visualization:** Historical charts showing wealth distribution, resource scarcity, and agent trust networks over time.
-   **Participation Mode:** Allow a user to take on the role of an agent to interact with the simulation directly.
-   **Database Integration:** Use a database (e.g., Supabase) to save, load, and analyze simulation states and results.

## Data Requirements

-   **Agent:** `agent_id`, `job`, `system_prompt` (defining culture/personality), `inventory` (JSON), `needs` (JSON), `wants` (JSON), `subjective_economic_value` (number), `event_budget_remaining` (number).
-   **Job:** `job_name`, `income`
-   **TradeOffer:** `offer_id`, `proposer_id`, `responder_id`, `offer` (JSON), `request` (JSON), `justification` (text), `evaluation` (text: "very good", "good", "neutral", "bad", or "very bad"), `status` ('proposed', 'accepted', 'rejected').
-   **NegotiationSession:** `session_id`, `consumer_id`, `producer_id`, `state` ('resource requested', 'trade proposed', 'trade accepted', 'trade failed'), `initial_request` (JSON), `history` (array of `TradeOffer` objects), `status` ('ongoing', 'accepted', 'rejected').
-   **SimulationLog:** A log file recording all negotiations, outcomes, and agent state changes in chronological order for post-simulation analysis.

## User Flows

### Flow 1: Researcher Configures and Runs a Simulation

1.  **Entry Point:** Researcher opens the web application.
2.  **Set Global Parameters:** The user adjusts sliders for global **Temperature**, **Day Length** (event budget), and **Day Count**.
3.  **Configure Jobs:** The user sets the **Agent Count** and **Income** for each job.
4.  **Configure Agents:** The user selects individual agents to assign a specific **Culture/Personality** and adjust their **Needs** and **Wants** for various resources.
5.  **Start Simulation:** The user clicks a "Start Simulation" button.
6.  **Exit Point:** The system initializes the simulation, and the user is taken to the real-time monitoring dashboard.

### Flow 2: Researcher Monitors and Analyzes the Simulation

1.  **Entry Point:** The simulation is running, and the monitoring dashboard is active.
2.  **Observe Interactions:** The user watches the **Agent Interaction Diagram** to see trades happening in real-time.
3.  **Inspect Agent:** The user clicks on an agent in the diagram. The **Selected Agent Panel** populates with that agent's detailed stats and inventory.
4.  **Track Value:** The user monitors the **Subjective Economic Value Graph** to see how agents' valuations of trades evolve.
5.  **Review Events:** The user scrolls through the **Event Log** to trace the history of specific negotiations or agent actions.
6.  **Conclude Simulation:** Once the simulation ends (Day Count reached), a "Download Log" button appears.
7.  **Export Data:** The user clicks the button to save the complete event log locally for external analysis.
8.  **Exit Point:** The user opens the log file in their preferred analysis tool.

## Technical Constraints

**Platform Requirements:** 
-   Must be a web-based application accessible via modern desktop browsers (Chrome, Firefox, Edge).

**Performance Requirements:** 
-   The simulation backend must handle numerous concurrent agent interactions without significant slowdown. 
-   The frontend must render visualizations smoothly.

**Integration Requirements:**
- Must integrate with Google AI Python SDK or similar LLM service for AI decision-making and offer evaluation.

**Connectivity Requirements:** 
-   Requires a stable internet connection to communicate with the LLM API.

**Data Integrity Requirements:** 
-   Simulation logs must be accurate and complete to ensure the validity of research results.

**Development Constraints:**
-   Must complete development within 6 weeks with AI-assisted development tools
-   Must use proven, well-documented technologies suitable for AI-assisted coding
-   Must include comprehensive API documentation

## Success Criteria

**Functional Success:**
-   Criterion 1: Users can configure and launch a simulation with a variety of global and agent-specific parameters.
-   Criterion 2: The simulation runs autonomously, with agents successfully negotiating and executing trades to fulfill their needs.
-   Criterion 3: The dashboard provides a clear, real-time, and understandable view of the simulation's state.
-   Criterion 4: The final event log is comprehensive and provides useful data for post-simulation analysis.

**Technical Success:**
-   Criterion 5: The backend engine maintains stable performance with a moderate number of agents, at least 20.
-   Criterion 6: The frontend visualizations update in near real-time without lagging.
-   Criterion 7: LLM API integration is reliable, with proper error handling.

**Research Success:**
-   Criterion 8: The simulation produces emergent economic behaviors that are non-trivial and worthy of study.
-   Criterion 9: The reservation price of goods is demonstrably influenced by configurable factors like agent culture, needs, and negotiation history.

## Technical Specifications

### Frontend Specification
-   **Language:** TypeScript for type safety and better AI-assisted development.
-   **Framework:** Next.js 14+ with App Router for server-side rendering and optimal performance.
-   **Styling:** Tailwind CSS and shadcn/ui for rapid and responsive component development.
-   **State Management:** Zustand for lightweight, scalable global state management.
-   **Data Visualization:** Recharts for the economic value graph and agent interaction diagram.
-   **Deployment:** Vercel for frontend hosting with automatic CI/CD.

-   **Architecture Pattern:** Component-based architecture with clear separation between presentation components, container components, and negotiation logic hooks.

### Backend Specification
-   **Language:** Python for AI integration compatibility and rapid development.
-   **Framework:** FastAPI (Python) for high-performance RESTful API development.
-   **AI Integration:** 
    - Gemini model accessed via the official Google AI Python SDK for reliability and ease of use.
    - Custom prompt engineering for consistent AI behavior
    - Fallback logic for API failures.
-   **Testing:** Pytest for unit and integration tests.
-   **Build Tool:** UV for fast Python package management.
-   **API Architecture:** A RESTful API with versioning (/api/v1) to manage simulation state and a WebSocket connection to stream real-time updates to the frontend.

### Database Specification
-   **None**

### AI Integration Specification
**AI Use Cases**:
1. **Trade Partner Selection**
2. **Resource Request**
3. **Request Evaluation**
4. **Offer Generation**
5. **Offer Evaluation**

**Subjective Economic Value Tracking**:
- Each trade offer receives an evaluation from both agents: "very good", "good", "neutral", "bad", or "very bad"
- The final offer's evaluations are converted to numerical scores: +20, +10, 0, -10, -20 respectively
- Each agent maintains a running subjective economic value sum by adding these scores
- Unfulfilled needs contribute negative values to this sum, representing the cost of unmet requirements
- This cumulative value is tracked over time and visualized in the Subjective Economic Value Graph
- **Key Design Rationale**: Using text evaluations instead of direct numerical scores ensures proper AI immersion in their roles. The LLMs are not told they are in a simulation, allowing them to respond naturally as economic agents would, leading to more authentic and interesting emergent behaviors

**Implementation:**
-   **Model:** Gemini 2.5 pro/flash.
-   **Prompt Design:** 
    - System prompts will be carefully engineered to define each agent's culture, goals, and constraints. 
    - Prompts during negotiation will include the agent's state, goals, and the full history of the current negotiation session. 
    - The agents will NOT be told that this is a simulation, but will be instructed on what format to respond in and to consider all factors.
    - Few-shot examples for consistent output format.
-   **Rate Limiting:** The simulation will pause to wait for refreshed limits. Alternatively, an API key can be provided.
-   **Fallback:** Automatic negotiation rejection.

## Platform Type
-   **Primary Platform:** Web application (browser-based).
-   **Target Devices:** Desktop or laptop computers exclusively, to avoid unnecessary complexity.
-   **Browser Compatibility:**
    - Chrome 90+ (primary testing target)
    - Firefox 88+
    - Edge 90+
    - Safari 14+
-   **Responsive Breakpoints**:
    - Desktop: 1280px+ (optimal experience)
    - Laptop: 1024px-1279px (full features)

## User Authentication Specification
-   For the MVP, no user authentication will be implemented. The tool is designed to be run as a standalone instance by a single researcher. Future versions with database integration may add user accounts to save and manage multiple simulation studies.

## Timeline and Milestones

**Total Duration**: 5 weeks following BMAD-methodology (4-phase model)

This timeline follows the 4-phase model of the BMAD-methodology, where phases 1 and 2 are done in 1 week, phase 3 is done in 2 weeks, and phase 4 is done in 2 weeks.

| Phase | Duration | Week | Focus |
|-------|----------|------|-------|
| Phase 1 & 2: Analyze and Planning | 1 week | Week 44 | Requirements analysis, project planning, stakeholder alignment |
| Phase 3: Solution Architecture and UI/UX Design | 2 weeks | Week 45-46 | Technical architecture, database design, UI/UX mockups, API design |
| Phase 4: Development and Deployment | 2 weeks | Week 47-48 | Implementation, testing, deployment |

---

### Phase 1 & 2: Analyze and Planning (Week 44)

**Lead Agents**: Analyst, Researcher
**Supporting Agents**: PM, PO

**Activities**:
- Requirements gathering
- Feature prioritization and MVP scope definition
- Risk analysis and mitigation planning
- Project charter and timeline finalization
- Budget planning (AI API costs)

**Deliverables**:
- Comprehensive requirements document
- Prioritized feature backlog
- Risk register with mitigation strategies


---

### Phase 3: Solution Architecture and UI/UX Design (Week 45-46)

**Lead Agents**: Architect
**Supporting Agents**: PM, Tech Lead

#### Week 45: Technical Architecture
**Activities**:
- Data model design (in-memory, with option for future database)
- API endpoint design (RESTful structure with versioning and WebSocket for real-time updates)
- System architecture diagram (frontend, backend, LLM service)
- Technology stack finalization and validation
- AI integration architecture (Gemini API, prompt engineering strategy)
- Development environment setup

**Deliverables**:
- Data models documentation
- API specification (OpenAPI/Swagger documentation)
- System architecture diagrams
- Technology stack decision document
- Development environment setup guide

#### Week 46: UI/UX Design
**Activities**:
- Information architecture and site mapping
- Wireframing for all key screens:
  - Simulation setup and configuration screen
  - Real-time monitoring dashboard
- High-fidelity mockups with design system
- Component library planning (shadcn/ui + Tailwind CSS)
- Responsive design breakpoints definition
- User flow diagrams
- Design prototype for user testing

**Deliverables**:
- Complete wireframe set
- High-fidelity UI mockups
- Design system documentation (colors, typography, spacing)
- Component library specification
- Responsive design guidelines
- Interactive prototype
- User flow diagrams

---

### Phase 4: Development and Deployment (Week 47-48)

**Lead Agents**: Scrum Master (SM), Developer (DEV)
**Supporting Agents**: SR, PM (for course correction)

#### Week 47: Core Development Sprint 1
**Day 1-2: Foundation**
- Project initialization (Next.js frontend, FastAPI backend)
- Backend setup for simulation engine
- Basic simulation state management

**Day 3-5: Simulation Engine**
- Core simulation logic implementation (turn-based engine, event budget)
- Agent and job configuration logic
- LLM integration for offer evaluation (Gemini API connection, initial prompts)
- In-memory data handling

**Day 6-7: Frontend Foundation**
- Simulation setup UI components
- Basic dashboard layout
- WebSocket connection for real-time updates

**Daily Standups**: Progress review, blocker identification, course correction

**Deliverables**: Working simulation engine with basic setup and real-time updates.

#### Week 48: Core Development Sprint 2 & Launch
**Day 1-2: Frontend Polish**
- Agent Interaction Diagram visualization (Recharts)
- Selected Agent Panel and Global Settings Panel
- Subjective Economic Value Graph
- Event Log implementation

**Day 3-4: Finalizing Features & Testing**
- Finalize UI/UX and ensure responsiveness
- Implement log export functionality
- Unit tests for simulation logic (Pytest)
- Integration tests for API endpoints
- End-to-end testing for critical user flows (setup -> run -> monitor -> export)
- Cross-browser testing

**Day 5: Deployment Preparation**
- Production environment setup (Vercel for frontend, and a backend hosting service)
- Environment variables and secrets configuration
- Documentation finalization (user guide, API docs)

**Day 6-7: Launch**
- Production deployment
- Documentation finalization (user guide, API docs)

**Daily Standups**: Intensive daily coordination, bug triaging, priority management

**Deliverables**: Fully functional, tested, and deployed AIES platform.

---

### BMAD-Methodology Alignment

**Phase 1 (Analyze)**: Deep understanding of business problem, user needs, and constraints
**Phase 2 (Planning)**: Strategic planning of solution approach with clear milestones
**Phase 3 (Architecture & Design)**: Complete technical and visual blueprint before coding
**Phase 4 (Development)**: Rapid AI-assisted implementation following the blueprint

**Key Success Factors**:
- Clear separation of design and development phases prevents rework
- Comprehensive architecture in Phase 3 enables confident AI-assisted coding in Phase 4
- Week 44 planning prevents scope creep
- Weeks 45-46 design work provides clear implementation roadmap
- AI-assisted development in Phase 4 accelerates coding
- Daily standups in Phase 4 ensure rapid issue resolution

**Risk Mitigation**:
- Phase 3 architecture reviews catch issues before development
- Two-week development sprint focuses team on MVP features
- Testing integrated into Week 48 prevents last-minute surprises
- Day 6 deployment prep allows Day 7 low-stress launch

## Development Approach
**AI-Assisted Development:** 
- Gemini CLI generates code and architecture
- Human oversight for logic, AI prompts and architecture decisions

**Testing Strategy**:
- Unit tests for simulation logic (initialization, state transitions)
- Integration tests for API endpoints
- Manual testing for AI-generated content quality

**Iterative Build:** Develop the core simulation logic first, then layer on the AI integration and frontend visualization.

**Version Control:** Use Git with a feature-branch workflow to manage code.

## Risk Assessment

**Technical Risks:**
-   **LLM Consistency:** The behavior of LLM agents may be unpredictable or produce inconsistent results, affecting the validity of the simulation.
    -   *Mitigation:* Use lower temperature settings for more predictable outcomes and implement robust prompt engineering.
-   **LLM Rate Limits/Pricing:** Exceeding API rate limits could disrupt simulations, and high usage could lead to unexpected costs.
    -   *Mitigation:* Optimize prompt length, monitor API usage closely, and quickly reject failed API calls.
-   **Real-time Visualization Performance:** Rendering a large number of agents and interactions could cause frontend performance issues.
    -   *Mitigation:* Use an efficient rendering library and optimize data streaming from the backend.

**Project Risks:**
-   **Scope Creep:** The "Nice to Have" features are extensive and could distract from the core MVP.
    -   *Mitigation:* Strictly adhere to the MVP feature set and move all other ideas to a post-launch backlog.
-   **Complexity of Emergent Behavior:** Analyzing the results to find meaningful emergent behavior may be more complex than anticipated.
    -   *Mitigation:* Focus the success criteria on the *presence* of emergent phenomena, with deep analysis being the subject of subsequent research.

**Assumptions**:
- AI-assisted development will increase productivity for coding tasks
- Gemini Models through Google AI Python SDK will maintain consistent availability and performance
- Modern web browsers support all required features (WebSockets, local storage, modern JavaScript)
- 6 weeks is sufficient for a feature-complete MVP given AI assistance and focused scope
