# ibe160 UX Design Specification

_Created on 2025-11-09 by BIP_
_Generated using BMad Method - Create UX Design Workflow v1.0_

---

## Executive Summary

AIES is a web-based simulation platform for researchers to study emergent economic and social behaviors in LLM-powered agents. The core idea is to observe nuanced, human-like interactions such as negotiation and trust formation. A recent pivot idea suggests reframing this as a measurable game where agents compete to maximize wealth, providing a clear success metric.

---

## 1. Design System Foundation

### 1.1 Design System Choice

Based on the project's technical stack and goals, **shadcn/ui** has been selected as the foundational component library.

*   **System:** shadcn/ui
*   **Rationale:** This choice aligns perfectly with the specified `Tailwind CSS` frontend stack. It provides an ideal balance of development speed, high-quality accessible components, and deep customizability. Unlike traditional component libraries, `shadcn/ui` allows us to own the code for each component, providing flexibility while ensuring a consistent and modern aesthetic. The user has approved this recommendation.
*   **Provided Components:** The system provides a comprehensive set of foundational components, including buttons, forms, menus, dialogs, and more.
*   **Customization Strategy:** We will leverage the full power of `Tailwind CSS` to style the `shadcn/ui` components to match our specific visual identity. While the library is extensive, we anticipate the need to build or heavily customize components for our specialized data visualizations (e.g., the agent interaction diagram).

---

## 2. Core User Experience

### 2.1 Defining Experience

The core user experience is centered on the seamless manipulation of simulation parameters and the clear, real-time observation of results.

*   **Defining Interaction:** The most frequent and important user action is the configuration and adjustment of simulation parameters. This must be intuitive and immediate.
*   **Effortless Action:** Starting and stopping the simulation should be a single, unambiguous action, providing immediate feedback.
*   **Critical Focus:** The success of the platform hinges on the accuracy, clarity, and real-time nature of the output graphs and event logs. These are the primary sources of insight for the researcher and must be treated as the most critical part of the user interface.
*   **Platform:** The experience is exclusively designed for a desktop web browser, allowing for a focus on a larger screen layout optimized for complex data visualization.

**Desired Emotional Goal:** The primary emotional goal for the user is to feel **"curious and surprised."** The design should foster a sense of discovery, revealing insights in delightful ways and making the researcher feel like they are on the verge of a breakthrough.

**Guiding Design Principles:**
*   **Trustworthy & Reliable:** Inspired by Microsoft Office, the platform must be perceived as robust and dependable. Data must be accurate, and the simulation must run predictably. Data export must be seamless.
*   **Fast & Simple:** Inspired by Google Chrome, the interface will be clean, uncluttered, and highly responsive. Core actions will be immediate, avoiding unnecessary complexity.
*   **Clear & Organized:** Inspired by threaded email conversations, the critical event log must present a clear, hierarchical, and easily scannable history of agent interactions.

**Defining Experience Statement:** When describing the app, a researcher would say: "It's the app where you can **finally see how hidden information and negotiation change an economy.**"

### 2.2 Novel UX Patterns

The core research goal is delivered through a novel UX pattern: **The Real-Time Agent Interaction Diagram**. This visualization provides an at-a-glance understanding of the simulation's state and serves as the primary window into emergent behaviors.

**Design Specification:**

*   **Visual Language:**
    *   **Agents:** Represented as circular dots.
    *   **Agent's Job:** Indicated by the dot's color. A clear legend will be provided.
    *   **Agent's Subjective Value:** Indicated by the dot's size. The size will animate (growing or shrinking) in real-time as the agent's cumulative subjective economic value changes, providing immediate visual feedback on their success.
    *   **Negotiations:** Represented as arrows between agent dots.
    *   **Negotiation State:** Indicated by the arrow's color, which changes dynamically to reflect the state of the negotiation (e.g., Initiated, Offer Made, Accepted, Rejected).

*   **Core Interactions:**
    *   **Inspect Agent:** Clicking on an agent dot will open a dedicated panel displaying that agent's detailed state, including their job, configuration parameters, resource inventory, and historical statistics.
    *   **Inspect Negotiation:** Clicking on a negotiation arrow will open a panel displaying the detailed state and history of that specific negotiation, including offers, counter-offers, and final outcome.

*   **Exceptional Experience & "Surprise":**
    *   **Synchronized Event Log:** The main event log will scroll and update in perfect sync with the events visualized on the diagram.
    *   **Interactive Value Graphs:** The time-series graphs showing agents' subjective economic value will be interactive, allowing the user to scroll horizontally through time to explore different stages of the simulation.

This design directly addresses the core UX challenges by providing a clear visual language and intuitive drill-down capabilities, enabling the researcher to feel "curious and surprised" as they uncover patterns in the simulation.

---

## 3. Visual Foundation

### 3.1 Color System

{{visual_foundation}}

**Interactive Visualizations:**

- Color Theme Explorer: [ux-color-themes.html](./ux-color-themes.html)

---

## 4. Design Direction

### 4.1 Chosen Design Approach

{{design_direction_decision}}

**Interactive Mockups:**

- Design Direction Showcase: [ux-design-directions.html](./ux-design-directions.html)

---

## 5. User Journey Flows

### 5.1 Critical User Paths

{{user_journey_flows}}

---

## 6. Component Library

### 6.1 Component Strategy

{{component_library_strategy}}

---

## 7. UX Pattern Decisions

### 7.1 Consistency Rules

{{ux_pattern_decisions}}

---

## 8. Responsive Design & Accessibility

### 8.1 Responsive Strategy

{{responsive_accessibility_strategy}}

---

## 9. Implementation Guidance

### 9.1 Completion Summary

{{completion_summary}}

---

## Appendix

### Related Documents

- Product Requirements: `/home/eirik/ibe160/SG-418/docs/prd-aies-ai-economy-simulator.md`
- Product Brief: `/home/eirik/ibe160/SG-418/docs/project-brief.md`
- Brainstorming: `/home/eirik/ibe160/SG-418/docs/brainstorming-session-results-2025-11-09.md`

### Core Interactive Deliverables

This UX Design Specification was created through visual collaboration:

- **Color Theme Visualizer**: ux-color-themes.html
  - Interactive HTML showing all color theme options explored
  - Live UI component examples in each theme
  - Side-by-side comparison and semantic color usage

- **Design Direction Mockups**: ux-design-directions.html
  - Interactive HTML with 6-8 complete design approaches
  - Full-screen mockups of key screens
  - Design philosophy and rationale for each direction

### Optional Enhancement Deliverables

_This section will be populated if additional UX artifacts are generated through follow-up workflows._

<!-- Additional deliverables added here by other workflows -->

### Next Steps & Follow-Up Workflows

This UX Design Specification can serve as input to:

- **Wireframe Generation Workflow** - Create detailed wireframes from user flows
- **Figma Design Workflow** - Generate Figma files via MCP integration
- **Interactive Prototype Workflow** - Build clickable HTML prototypes
- **Component Showcase Workflow** - Create interactive component library
- **AI Frontend Prompt Workflow** - Generate prompts for v0, Lovable, Bolt, etc.
- **Solution Architecture Workflow** - Define technical architecture with UX context

### Version History

| Date     | Version | Changes                         | Author        |
| -------- | ------- | ------------------------------- | ------------- |
| 2025-11-09 | 1.0     | Initial UX Design Specification | BIP |

---

_This UX Design Specification was created through collaborative design facilitation, not template generation. All decisions were made with user input and are documented with rationale._
