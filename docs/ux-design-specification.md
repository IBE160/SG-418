# UX Design Specification: AIES - AI Economy Simulator

## 1. Project Vision & Users

### 1.1. Project Summary
AIES is a web-based AI Economy Simulator for researchers to study emergent economic behaviors from LLM-powered agents. The platform includes a configurable simulation engine and a real-time monitoring dashboard with an agent interaction diagram, agent inspector, economic graphs, and an event log.

### 1.2. Target Audience
- **Primary:** Academic researchers in economics and sociology (e.g., Dr. Anya Sharma) who need an intuitive, powerful tool for behavioral studies without requiring programming expertise.
- **Secondary:** Graduate students, educators, and policymakers (e.g., Ben Carter) who require a flexible platform for simulating and analyzing economic and social scenarios.

## 2. Core Experience & Platform

### 2.1. Platform
The AIES platform is a **Web Application** designed primarily for use on desktop browsers. This provides the necessary screen real estate for a complex, multi-panel monitoring dashboard.

### 2.2. Core User Experience
The central user experience is a seamless loop of **"Configure → Monitor → Export."**

1.  **Configure:** The user's primary activity is setting up the simulation's economic parameters and agent behaviors. This process must be intuitive and efficient, empowering the researcher to translate their hypothesis into a viable simulation without friction.
2.  **Monitor:** Once running, the user's focus shifts to observing the simulation in real-time via the interactive dashboard. The design must prioritize the clear visualization of emergent behaviors and key economic indicators.
3.  **Export:** The final critical action is exporting the complete event log. This must be a simple, one-click action that produces research-ready data.

The single most critical experience to perfect is the flow from initial **configuration to seeing the first results** on the dashboard.

## 3. Desired Emotional Response
The design of the AIES platform aims to evoke a specific set of feelings in the user, ensuring the tool feels less like a piece of software and more like a world-class research laboratory.

-   **Empowered and in Control:** Users should feel like they are in command of a powerful and precise scientific instrument. The interface will provide a sense of direct manipulation and clear control over the simulation's parameters.
-   **Insightful and Enlightened:** The ultimate goal is discovery. The dashboard should be designed to facilitate "Aha!" moments, where complex data is presented so clearly that hidden patterns and emergent behaviors are revealed intuitively.
-   **Efficient and Productive:** The user's workflow, from hypothesis to data analysis, should feel frictionless. The tool should get out of the way, allowing the researcher to focus on their work, not on learning the software.

## 4. Inspiration & UX Pattern Analysis
To ensure a world-class user experience, we will draw inspiration from best-in-class tools that have solved similar design challenges related to data visualization, real-time interaction, and information-dense interfaces.

-   **Inspiration 1: Figma & Miro (The Collaborative Canvas):** These platforms excel at managing real-time object manipulation on a shared canvas. We will analyze their patterns for selection, zoom, pan, and relationship visualization to inform the design of the **Agent Interaction Diagram**.

-   **Inspiration 2: Tableau & Grafana (The Data Powerhouse):** As leaders in interactive data visualization, these tools provide proven models for dashboard composition, filter controls, and drill-down capabilities. Their UX patterns will heavily influence the **Economic Indicators** graph and the **Agent Inspector** panel.

-   **Inspiration 3: Visual Studio Code (Information Density & Layout):** VS Code demonstrates how to successfully implement a flexible, multi-panel interface that remains clear and efficient for power users. Its configurable layout and clear iconography will serve as a reference for the overall dashboard structure, ensuring it feels professional and customizable.

## 5. Project Synthesis

-   **Vision:** A web-based simulator for researchers to study emergent economic behavior in LLM-powered agents.
-   **Users:** Tech-savvy academics who value intuitive setup, powerful real-time monitoring, and research-grade data.
-   **Core Experience:** A seamless loop: **Configure → Monitor → Export**.
-   **Desired Feeling:** **Empowered, Insightful, and Efficient**—like a world-class lab at your fingertips.
-   **UX Complexity:** **Moderately Complex**, due to the multi-panel, real-time, and highly configurable nature of the dashboard.

## 6. Design System
The AIES user interface will be built using **shadcn/ui** as its foundational design system.

-   **Rationale:** This choice, pre-aligned with the project's technical brief, is ideal for creating the desired professional, data-dense, and highly-functional user experience. The system's modern aesthetic, comprehensive component library (including charts, forms, tables, and dialogs), and emphasis on accessibility and customization perfectly match the project's goals.
-   **Implementation:** By allowing direct source code ownership, `shadcn/ui` provides the flexibility to tailor every component to our specific needs, ensuring a polished and cohesive final product.

## 7. Defining Experience & Core Principles

### 7.1. The Defining Experience: Live Discovery
The defining moment of the AIES experience is **Live Discovery**: the real-time observation of emergent behaviors within the simulation. This is achieved when the user can intuitively connect visual patterns on the **Agent Interaction Diagram** with corresponding data trends in the **Economic Value Graph** and event logs, leading to novel insights. This experience will be crafted using established UX patterns (dashboards, node-graphs, inspector panels), focusing on refinement and clarity rather than inventing new interaction models.

### 7.2. Core Experience Principles
Four principles will guide all design decisions to ensure a cohesive and effective user experience:

1.  **Clarity Above All:** The interface will prioritize clear, at-a-glance understanding of the simulation's state. Information hierarchy will be strong, and visual noise will be minimized to allow the data to tell the story.
2.  **Direct Manipulation:** Users will feel a direct connection to the simulation. Interactions like clicking an agent to inspect it, hovering a data point to see its value, or dragging the canvas will be instant and intuitive.
3.  **Responsive Feedback:** The system will feel alive and communicative. Every user action will be met with immediate and clear visual feedback, from button states to loading indicators and simulation status updates.
4.  **Progressive Disclosure:** The primary dashboard will remain focused and uncluttered by default. Advanced configuration options, secondary data, and detailed settings will be revealed contextually, preventing information overload while keeping power and flexibility one click away.

## 8. Visual Foundation

### 8.1. Color Theme: Biosphere
The AIES interface will use the **Biosphere** theme. This theme was selected for its professional, clean aesthetic combined with an organic warmth that reflects the concept of a living, emergent system.

-   **Primary Color:** `#2F855A` (A deep, trustworthy green)
-   **Secondary/UI Backgrounds:** `#F0EBE6`, `#FAF9F6` (Warm, earthy off-whites and grays)
-   **Text Color:** `#312E2B` (A dark, warm brown for high readability)
-   **Accent Color:** `#48BB78` (A vibrant green for highlighting key actions and data points)

### 8.2. Typography
The typography system is designed for clarity, performance, and a native feel.

-   **UI Font:** A system sans-serif font stack (`-apple-system`, `BlinkMacSystemFont`, `"Segoe UI"`, `Roboto`, `"Helvetica Neue"`, `Arial`, `sans-serif`) will be used for all interface elements, ensuring optimal legibility and performance.
-   **Data/Code Font:** A system monospace font stack (`"SFMono-Regular"`, `Consolas`, `"Liberation Mono"`, `Menlo`, `Courier`, `monospace`) will be used for displaying raw data, logs, or code snippets to ensure clear differentiation and accurate representation.

### 8.3. Spacing & Layout
A consistent spacing system will be used to create a visually balanced and rhythmic layout.

-   **Base Unit:** The core of the system is an **8px base unit**.
-   **Scale:** All padding, margins, and element dimensions will be multiples of the base unit (e.g., 4px, 8px, 16px, 24px, 32px, 48px, 64px), ensuring a harmonious and predictable structure across the entire application.

## 9. Design Direction

### 9.1. Selected Direction: "Command Center"
Based on the need for a high-density, professional research environment, the **Command Center** design direction has been selected.

-   **Philosophy:** A "Scientific Instrument" aesthetic that prioritizes data visibility and control precision over decorative elements.
-   **Layout:** A persistent sidebar for global navigation and simulation controls, maximizing the central area for data visualization.
-   **Density:** High. The interface makes efficient use of screen real estate to show multiple data streams simultaneously (Graph, Charts, Logs) without requiring scrolling.
-   **Visual Hierarchy:** Data first. The most prominent elements are the visualization panels (Interaction Diagram, Economic Graph). Controls are grouped logically in the sidebar or collapsible panels to reduce visual clutter when not in use.

## 10. User Journey Flows

### 10.1. Journey 1: Configure & Start Simulation
**Goal:** A researcher wants to define simulation parameters (agents, resources, rules) and start the experiment.

1.  **Entry:** User clicks "New Simulation" from the dashboard.
2.  **Step 1: Global Configuration:** User sets global parameters like Day Duration (seconds), Daily Event Budget, Max Days, and Temperature.
3.  **Step 2: Job & Agent Configuration:**
    -   User defines the available Jobs and the Resources they produce (e.g., "Woodcutter" produces "Wood").
    -   User sets the Agent Count and Income for each Job.
    -   User configures agent personas (e.g., "Aggressive Trader", "Conservative Saver") and their Needs/Wants using sliders or a JSON editor for advanced control.
4.  **Step 3: Review & Launch:** User sees a summary of the configuration (Total Agents, Resources). Clicks "Start Simulation".
5.  **Feedback:** System transitions to the **Live Dashboard**. A loading state shows "Initializing Agents...", followed by the first tick of data appearing on the graphs.

### 10.2. Journey 2: Real-time Monitoring & Inspection
**Goal:** A researcher observes emergent behavior and investigates a specific agent's actions.

1.  **Context:** Simulation is running. The main view shows the **Agent Interaction Diagram** (agents moving/connecting) and **Subjective Economic Value Graph** (sum of self-reported trade outcome values minus need penalties).
2.  **Observation:** User notices a spike in the economy graph.
3.  **Investigation:** User hovers over the corresponding time point on the graph. A tooltip shows "Transaction Volume High".
4.  **Drill-down:** User looks at the **Agent Interaction Diagram**. One node is larger and red (high value).
5.  **Inspection:** User clicks the red agent node.
6.  **Result:** An **Inspector Panel** slides out from the right. It shows:
    -   Agent Name/ID.
    -   Current Stats (Satisfaction, Budget).
    -   Current Inventory (Cash, Resources).
    -   Recent Decisions (Log of LLM reasoning: "Price is high, I should sell.").
    -   Conversation History (Messages exchanged with other agents).
7.  **Action:** User pauses the simulation to analyze the log in detail without missing new events.

## 11. Component Library Strategy

### 11.1. Core Components (shadcn/ui)
We will leverage the robust `shadcn/ui` library for standard interface elements to ensure consistency and speed of development.

-   **Layout:** `Card`, `Sheet` (for Inspector), `Resizable` (for multi-panel layout).
-   **Forms:** `Slider` (params), `Switch`, `Input`, `Select`, `Button`.
-   **Feedback:** `Badge` (agent status), `Progress` (loading), `Toast` (system notifications).
-   **Data Display:** `Table` (event logs), `ScrollArea` (log containers).

### 11.2. Custom Components
Specific research requirements necessitate custom, high-performance visualization components.

-   **Agent Interaction Diagram:**
    -   **Purpose:** Visualizes the network of agents and their real-time interactions (trades, messages).
    -   **Tech:** Recharts.
    -   **Features:** Zoom/Pan, Node coloring by state (rich/poor), Edge thickness by transaction volume.
-   **Subjective Economic Value Graph:**
    -   **Purpose:** Real-time time-series plotting of the Total Subjective Economic Value (cumulative trade scores minus need penalties).
    -   **Tech:** Recharts.
    -   **Features:** Real-time updates, interactive tooltips, brush-to-zoom.
-   **Agent Inspector Panel:**
    -   **Purpose:** detailed view of a single agent's internal state.
    -   **Features:** Tabbed view (Inventory, Logic, Logs), raw JSON toggle.

## 12. UX Pattern Consistency Rules

### 12.1. Interaction Patterns
-   **Selection:** Single click on graph nodes selects the agent and opens the Inspector. Click on canvas background deselects.
-   **Hover:** Hovering over data points (graph or node) provides immediate, transient details via tooltips.
-   **Simulation Control:** Play/Pause/Stop controls are always visible and accessible in the primary sidebar/header area (Global State).

### 12.2. Visual Feedback
-   **Status Indicators:** Use color sparingly but consistently.
    -   **Green:** Active, Healthy, Profit, Growth.
    -   **Red:** Error, High Risk, Loss, Danger.
    -   **Yellow/Orange:** Warning, Caution, High Load.
    -   **Blue:** Neutral information, Selected state.
-   **Loading:** Skeleton loaders for initial data fetch. Spinner for async actions (e.g., "Step Simulation").

### 12.3. Layout & Navigation
-   **Dashboard Layout:** A resilient, grid-based layout. Panels should be collapsible to allow users to focus on specific views (e.g., expand Graph to full screen).
-   **Navigation:** Global navigation (Home, Simulations, Settings) is located in the left sidebar. Contextual navigation (Graph settings, View options) is located in the header of the specific panel.

## 13. Responsive & Accessibility Strategy

### 13.1. Responsive Strategy
Given the complex, data-heavy nature of the application, the primary target is **Desktop**.

-   **Desktop ( > 1024px):** Full dashboard experience. All panels visible.
-   **Tablet & Mobile:** Not supported in MVP. The application is designed exclusively for desktop/laptop usage to avoid unnecessary complexity, as defined in the Project Proposal.

### 13.2. Accessibility (WCAG 2.1 AA)
-   **Color Contrast:** Ensure all text meets 4.5:1 contrast ratio. Use patterns (dashes, shapes) in graphs in addition to color to distinguish data series.
-   **Keyboard Nav:** Ensure the dashboard grid is navigable via keyboard. Graphs should support keyboard focus for data points (using arrow keys to traverse time series).
-   **Screen Readers:** Provide `aria-label` for all icon-only buttons. Ensure data tables are properly marked up. Provide textual summaries for complex charts where possible.