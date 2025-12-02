# ibe160 - Epic Breakdown

**Author:** BIP
**Date:** Tuesday, December 2, 2025
**Project Level:** Beginner
**Target Scale:** MVP

---

## Overview

This document provides the complete epic and story breakdown for {{project_name}}, decomposing the requirements from the [PRD](./PRD.md) into implementable stories.

**Living Document Notice:** This is the initial version. It will be updated after UX Design and Architecture workflows add interaction and technical details to stories.

## Epics Summary

1.  **Epic 1: Foundation & Simulation Engine** - Infrastructure setup and core loop.
2.  **Epic 2: Simulation Configuration Interface** - UI for defining the simulation scenario.
3.  **Epic 3: Autonomous Agent Intelligence** - LLM integration and trade logic.
4.  **Epic 4: Real-Time Monitoring Dashboard** - High-level visualization of the economy.
5.  **Epic 5: Deep Inspection & Analysis** - Individual agent details and data export.

---

## Functional Requirements Inventory

- **FR1.1 Global Configuration:** Users can set global parameters (simulation day length, max days, agent count).
- **FR1.2 Job & Resource Configuration:** Users can define jobs and the resources they produce.
- **FR1.3 Agent Configuration:** Users can specify agent attributes (ID, job, culture, needs, wants, income).
- **FR2.1 Structured LLM Communication:** All LLM communication must use `pydantic-ai` for structured validation.
- **FR2.2 Negotiation Turn Engine:** Simulation proceeds in turns where agents use an event budget.
- **FR2.3 Agent Decision Making:** LLMs decide trade partners, requests, offers, and evaluations.
- **FR2.4 Error Handling:** LLM failures are handled gracefully (turn skip) without crashing the simulation.
- **FR3.1 Agent Interaction Diagram:** Dynamic graph showing interacting agents.
- **FR3.2 Agent Inspector Panel:** Detailed panel showing agent inventory, state, and logs.
- **FR3.3 Global Economic Indicators:** Time-series graph of global metrics (e.g., economic value).
- **FR3.4 Live Event Log:** Chronological feed of simulation events.
- **FR4.1 Export Event Log:** Users can export the event log as CSV.

---

## FR Coverage Map

- **Epic 1 (Foundation & Simulation Engine):** FR2.2, FR2.1 (partial)
- **Epic 2 (Simulation Configuration):** FR1.1, FR1.2, FR1.3
- **Epic 3 (Autonomous Agent Intelligence):** FR2.1, FR2.3, FR2.4
- **Epic 4 (Real-Time Monitoring Dashboard):** FR3.1, FR3.3, FR3.4
- **Epic 5 (Deep Inspection & Analysis):** FR3.2, FR4.1

---

## Epic 1: Foundation & Simulation Engine

**Goal:** Establish the technical infrastructure (Next.js + FastAPI) and the core simulation loop so that the system can execute time steps and manage state, providing a platform for the AI agents.

### Story 1.1: Project Initialization & Skeleton

As a **Developer**,
I want **to initialize the frontend and backend repositories with the correct tech stack**,
So that **I have a working environment to build features upon.**

**Acceptance Criteria:**

**Given** a clean development environment
**When** I run the initialization commands
**Then** I should have a Next.js 14 frontend with shadcn/ui configured
**And** I should have a Python FastAPI backend with `uv` package manager initialized
**And** I should be able to run both servers concurrently without errors

**Prerequisites:** None

**Technical Notes:**
- Follow Architecture Doc Section 2 exactly.
- Frontend: `npx create-next-app` (TS, Tailwind).
- Backend: `uv init`, install `fastapi`, `uvicorn`.
- Set up `.gitignore` for both.

### Story 1.2: Core Simulation Loop (Engine)

As a **Researcher**,
I want **the simulation to advance in discrete "turns" or "ticks"**,
So that **agents have a structured opportunity to act.**

**Acceptance Criteria:**

**Given** the backend server is running
**When** I trigger a "step" or "tick" (internal function call initially)
**Then** the system should increment the `current_day` or `tick_count`
**And** the system should reset daily event budgets for all agents
**And** the state should be updated in memory

**Prerequisites:** 1.1

**Technical Notes:**
- Implement `backend/core/engine.py`.
- Create a basic `WorldState` model (Architecture Section 9).
- No agents needed yet, just the time-keeping logic.

### Story 1.3: Backend State Management

As a **Developer**,
I want **a centralized in-memory store for the simulation state**,
So that **all components (and the frontend) access the same source of truth.**

**Acceptance Criteria:**

**Given** the application has started
**When** I request the current state via an internal API call
**Then** I should receive the singleton `WorldState` object
**And** modifications to this state should persist across requests (until server restart)

**Prerequisites:** 1.1

**Technical Notes:**
- Implement `backend/core/state.py`.
- Use a simple global variable or singleton pattern as per Architecture Decision 3 (In-Memory Singleton).

### Story 1.4: Frontend-Backend Connection

As a **User**,
I want **the frontend to connect to the backend API**,
So that **I can verify the system is operational.**

**Acceptance Criteria:**

**Given** both servers are running
**When** I load the frontend home page
**Then** I should see a "System Status: Online" indicator (fetched from backend)
**And** if the backend is down, it should show "System Status: Offline"

**Prerequisites:** 1.1, 1.3

**Technical Notes:**
- Create `GET /health` endpoint in FastAPI.
- Create a basic API client in frontend (`lib/api.ts`).
- Use a simple `useEffect` to fetch status on mount.

---

## Epic 2: Simulation Configuration Interface

**Goal:** Enable researchers to define the specific economic scenario they want to study (agents, jobs, resources) via a user-friendly UI.

### Story 2.1: Global Configuration Form

As a **Researcher**,
I want **to set global parameters like simulation duration**,
So that **I can control the scope of the experiment.**

**Acceptance Criteria:**

**Given** I am on the "New Simulation" page
**When** I enter values for "Day Length (seconds)" and "Max Days"
**Then** the form should validate that inputs are positive integers
**And** I should be able to proceed to the next step

**Prerequisites:** 1.4

**Technical Notes:**
- UX Journey 1, Step 1.
- Use shadcn `Input` and `Form` components.
- Define Pydantic model `GlobalConfig` in backend to match.

### Story 2.2: Job & Resource Definition UI

As a **Researcher**,
I want **to define the jobs available in the economy and what resources they produce**,
So that **I can simulate different economic structures.**

**Acceptance Criteria:**

**Given** I am on the configuration page
**When** I add a new Job (e.g., "Woodcutter")
**Then** I should be able to specify the Resource it produces (e.g., "Wood")
**And** I can add multiple jobs to the list

**Prerequisites:** 2.1

**Technical Notes:**
- UX Journey 1, Step 2.
- Use a dynamic list component (add/remove rows).
- Data structure: List of `JobConfig` objects.

### Story 2.3: Agent Configuration UI

As a **Researcher**,
I want **to specify the number of agents and their personalities**,
So that **I can study how different populations behave.**

**Acceptance Criteria:**

**Given** I have defined jobs
**When** I specify "Agent Count" for a specific Job
**And** I define their "Culture" (e.g., "Aggressive") and "Needs"
**Then** the system should generate a configuration payload for all agents

**Prerequisites:** 2.2

**Technical Notes:**
- UX Journey 1, Step 2 continued.
- Allow bulk configuration (e.g., "Create 5 Woodcutters with these stats").
- Validation: Total agents > 1.

### Story 2.4: Backend Configuration Endpoint

As a **Developer**,
I want **an API endpoint to receive the full simulation configuration**,
So that **the backend can initialize the simulation state.**

**Acceptance Criteria:**

**Given** a valid JSON configuration payload
**When** `POST /api/config` is called
**Then** the backend should validate it using Pydantic models
**And** initialize the `WorldState` with the specified agents and resources
**And** return 200 OK

**Prerequisites:** 2.3, 1.3

**Technical Notes:**
- Implement `backend/models/domain.py` with full config schema.
- The endpoint resets any existing state.

### Story 2.5: Start/Stop Simulation Controls

As a **Researcher**,
I want **buttons to Start, Pause, and Stop the simulation**,
So that **I can control the execution flow.**

**Acceptance Criteria:**

**Given** a configuration has been submitted
**When** I click "Start Simulation"
**Then** the backend engine should begin processing ticks (Epic 1.2)
**And** the frontend should switch to the "Monitor" view

**Prerequisites:** 2.4, 1.2

**Technical Notes:**
- Implement `POST /api/control/start` and `/stop`.
- Frontend state management (Zustand) to switch views.

---

## Epic 3: Autonomous Agent Intelligence

**Goal:** Empower agents to negotiate and trade using LLMs, creating the actual "AI economy" behavior.

### Story 3.1: LLM Integration Infrastructure

As a **Developer**,
I want **to integrate `pydantic-ai` with Google Gemini**,
So that **I can send structured prompts and receive validated JSON responses.**

**Acceptance Criteria:**

**Given** a valid Google Gemini API key
**When** I send a test prompt via the internal agent wrapper
**Then** I should receive a response that matches the defined Pydantic model
**And** if the model structure is invalid, `pydantic-ai` should raise a validation error

**Prerequisites:** 1.1

**Technical Notes:**
- Implement `backend/agents/implementation.py`.
- Architecture Decision: Pydantic-AI v0.0.1+.
- Store API key in `.env`.

### Story 3.2: Agent Decision: Trade Partner Selection

As a **Researcher**,
I want **agents to intelligently select who to trade with**,
So that **market networks emerge organically.**

**Acceptance Criteria:**

**Given** it is an agent's turn
**When** the agent is asked to act
**Then** it should analyze its current needs and the known jobs of others
**And** output the ID of a target agent to approach

**Prerequisites:** 3.1, 2.4 (agents exist)

**Technical Notes:**
- Prompt should include: Agent's own state (Needs, Inventory) and Public Info (List of other agents/jobs).
- Output Model: `TargetSelection(agent_id: str)`.

### Story 3.3: Agent Decision: Generate Offer

As a **Researcher**,
I want **agents to formulate specific trade proposals**,
So that **economic exchange can occur.**

**Acceptance Criteria:**

**Given** a target agent has been selected
**When** the agent formulates an offer
**Then** it should specify: Resource to Give, Amount to Give, Resource Requested, Amount Requested
**And** the offer should be rational based on its needs (e.g., asking for food if hungry)

**Prerequisites:** 3.2

**Technical Notes:**
- Output Model: `TradeOffer(offered_resource, offered_amount, requested_resource, requested_amount)`.

### Story 3.4: Agent Decision: Evaluate Offer

As a **Researcher**,
I want **agents to accept, reject, or counter incoming offers**,
So that **negotiations are two-sided.**

**Acceptance Criteria:**

**Given** an agent receives a `TradeOffer`
**When** it evaluates the offer
**Then** it should output a decision: `ACCEPT`, `REJECT`, or `COUNTER`
**And** the decision should increase the agent's utility (subjective value)

**Prerequisites:** 3.3

**Technical Notes:**
- Prompt includes the incoming offer details.
- Output Model: `OfferResponse(decision: Enum, reasoning: str)`.

### Story 3.5: Agent Error Handling (The "Penalty Box")

As a **System**,
I want **to handle cases where the LLM produces invalid output or crashes**,
So that **the entire simulation doesn't stop due to one agent's failure.**

**Acceptance Criteria:**

**Given** the LLM returns an error or invalid JSON
**When** the simulation engine catches this exception
**Then** the agent's turn ends immediately (Action.WAIT)
**And** the error is logged to the event stream
**And** the simulation proceeds to the next agent

**Prerequisites:** 3.1

**Technical Notes:**
- Architecture Decision: "Penalty Box" pattern.
- Try/except block around the agent step execution.

---

## Epic 4: Real-Time Monitoring Dashboard

**Goal:** Visualize the economy in real-time so researchers can observe high-level patterns and specific interactions.

### Story 4.1: Dashboard Layout & Sidebar

As a **User**,
I want **a responsive dashboard layout with a sidebar**,
So that **I can navigate between different monitoring views.**

**Acceptance Criteria:**

**Given** the simulation is running
**When** I view the dashboard
**Then** I should see a sidebar with global controls and navigation
**And** a main content area for graphs

**Prerequisites:** 2.5

**Technical Notes:**
- UX Journey 2.
- Use `shadcn` `Resizable` or simple CSS Grid.
- "Command Center" design direction.

### Story 4.2: Real-Time Economic Graph

As a **Researcher**,
I want **to see a live graph of the Total Economic Value**,
So that **I can assess if the economy is growing or crashing.**

**Acceptance Criteria:**

**Given** the simulation is progressing
**When** new ticks occur
**Then** the line chart should update automatically with the new value
**And** I should be able to see history since day 0

**Prerequisites:** 4.1, 1.2

**Technical Notes:**
- Use `Recharts` LineChart.
- Poll `GET /api/state` every X seconds (Architecture Decision).
- Compute "Total Value" on backend and send as part of state.

### Story 4.3: Live Event Log Feed

As a **Researcher**,
I want **a scrolling log of all major events (trades, conversations)**,
So that **I can follow the narrative of the simulation.**

**Acceptance Criteria:**

**Given** agents are interacting
**When** a trade or error occurs
**Then** a new text line should appear in the log panel
**And** it should show the Day/Time and a description

**Prerequisites:** 4.1, 3.3

**Technical Notes:**
- Use `shadcn` `ScrollArea`.
- Backend maintains a list of `Event` objects.

### Story 4.4: Agent Interaction Diagram

As a **Researcher**,
I want **visual representation of which agents are interacting**,
So that **I can identify social clusters or central trading hubs.**

**Acceptance Criteria:**

**Given** two agents are negotiating
**When** I look at the interaction diagram
**Then** I should see a line connecting their nodes
**And** the nodes should be labeled with Agent IDs

**Prerequisites:** 4.1

**Technical Notes:**
- Use `Recharts` ScatterChart or a specialized graph library if needed (simple Recharts Scatter with custom shape is often enough for MVP).
- UX Spec mentions "Node-graph".

---

## Epic 5: Deep Inspection & Analysis

**Goal:** Allow researchers to drill down into individual agent logic and export data for publication.

### Story 5.1: Agent Inspector Panel UI

As a **Researcher**,
I want **to click on an agent to see their details**,
So that **I can understand their individual state.**

**Acceptance Criteria:**

**Given** the dashboard is active
**When** I click an agent ID (in graph or log)
**Then** a side panel (Sheet) should open
**And** it should show the agent's name, job, and current inventory

**Prerequisites:** 4.1

**Technical Notes:**
- Use `shadcn` `Sheet` component.
- Fetch specific agent data if not already in global state, or filter from global state.

### Story 5.2: Agent Detail Data Fetching

As a **User**,
I want **to see the "Needs" and "Recent Thoughts" of the inspected agent**,
So that **I can debug their behavior.**

**Acceptance Criteria:**

**Given** the Inspector is open
**When** the polling cycle triggers
**Then** the displayed values (Inventory, Satisfaction) should update live

**Prerequisites:** 5.1

**Technical Notes:**
- Ensure `WorldState` includes sufficient detail, or add `GET /api/agent/{id}`.

### Story 5.3: Export Event Log to CSV

As a **Researcher**,
I want **to download the full simulation history as a CSV file**,
So that **I can perform statistical analysis in Excel or Python.**

**Acceptance Criteria:**

**Given** a simulation has run (or is running)
**When** I click "Export Data"
**Then** my browser should download a `.csv` file
**And** the file should contain columns: Tick, AgentID, Action, Details, Result

**Prerequisites:** 4.3

**Technical Notes:**
- Implement `GET /api/export` in backend.
- Convert in-memory event log to CSV string.
- Return with correct content-type headers.

---

<!-- End epic repeat -->

---

## FR Coverage Matrix

| FR ID | Description | Covered By |
| :--- | :--- | :--- |
| **FR1.1** | Global Configuration | Story 2.1 |
| **FR1.2** | Job & Resource Config | Story 2.2 |
| **FR1.3** | Agent Configuration | Story 2.3 |
| **FR2.1** | Structured LLM Comm | Story 3.1 |
| **FR2.2** | Negotiation Turn Engine | Story 1.2 |
| **FR2.3** | Agent Decision Making | Story 3.2, 3.3, 3.4 |
| **FR2.4** | Error Handling | Story 3.5 |
| **FR3.1** | Agent Interaction Diagram | Story 4.4 |
| **FR3.2** | Agent Inspector Panel | Story 5.1, 5.2 |
| **FR3.3** | Global Economic Indicators | Story 4.2 |
| **FR3.4** | Live Event Log | Story 4.3 |
| **FR4.1** | Export Event Log | Story 5.3 |

---

## Summary

The project requirements have been successfully decomposed into **5 Epics** and **21 Stories**, ensuring 100% coverage of the MVP Functional Requirements defined in the PRD.

- **Epics 1 & 2** establish the foundation and configuration capabilities.
- **Epic 3** delivers the core AI value proposition (Autonomous Agents).
- **Epics 4 & 5** provide the necessary research tools for monitoring and analysis.

The breakdown incorporates key decisions from the **Architecture Document** (FastAPI/Next.js split, Pydantic-AI, In-Memory State) and the **UX Specification** (Command Center layout, Real-time graphs). Each story is sized for a single developer session.

---

_For implementation: Use the `create-story` workflow to generate individual story implementation plans from this epic breakdown._

_This document will be updated after UX Design and Architecture workflows to incorporate interaction details and technical details._
