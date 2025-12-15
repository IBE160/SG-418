# Story 4.4: Agent Interaction Diagram

Status: drafted

## Story

As a **Researcher**,
I want **visual representation of which agents are interacting**,
so that **I can identify social clusters or central trading hubs.**

## Acceptance Criteria

1.  **Nodes:** The diagram displays a node for every active agent in the simulation.
2.  **Labels:** Each node is clearly labeled with the Agent ID (e.g., "A1", "A2").
3.  **Links:** A visual line connects two agents if they are currently negotiating or have executed a trade in the current tick.
4.  **Updates:** The diagram updates in real-time (per the dashboard polling cycle) to reflect new interactions.
5.  **Layout:** Nodes are arranged in a layout that prevents total overlap (e.g., circular or random distribution), allowing distinct identification.

## Tasks / Subtasks

- [ ] Implement Graph Layout Logic
  - [ ] Create utility function to assign (x, y) coordinates to agents (e.g., Circular layout based on index).
  - [ ] Ensure coordinates remain stable for the same agent ID across renders to prevent jitter.
- [ ] Implement InteractionGraph Component
  - [ ] Create `components/dashboard/InteractionGraph.tsx`.
  - [ ] Use `Recharts` `ScatterChart` (or `ComposedChart`) to render nodes.
  - [ ] Implement Custom Node shape to display Agent ID.
- [ ] Implement Edge/Link Rendering
  - [ ] Logic to parse `event_log` (or agent state) to identify active pairs (Source -> Target).
  - [ ] Render lines connecting the coordinates of interacting pairs (using `ReferenceLine` in Recharts or an SVG overlay).
- [ ] Integration
  - [ ] Connect component to `WorldState` via props.
  - [ ] Place component in the Dashboard Main Content area (from Story 4.1).

## Dev Notes

- **Tech Stack:** Next.js (Frontend) + Recharts.
- **Visualization:** Recharts is primarily for charts, but `ScatterChart` can mimic a graph. Use `Scatter` for nodes and `ReferenceLine` (segment) for edges.
  - *Alternative:* If Recharts proves too difficult for node-link diagrams, a pure SVG implementation within the React component is acceptable and often simpler for this specific use case.
- **Data Source:**
  - **Nodes:** `WorldState.agents` list.
  - **Edges:** Derived from `WorldState.event_log` (look for 'NEGOTIATION' or 'TRADE' events in the latest tick) OR a dedicated `active_partner_id` field on the Agent model if added.
- **Layout:** Start with a simple **Circular Layout**. Calculate angle based on `index / total_agents`. Radius = fixed.
- **Performance:** Ensure the graph doesn't re-calculate layout on every tick if the agent list hasn't changed. Memoize the coordinate mapping.

### Project Structure Notes

- **Path:** `frontend/src/components/dashboard/InteractionGraph.tsx`

### References

- [Source: docs/epics.md#Story-4.4]
- [Source: docs/sprint-artifacts/tech-spec-epic-4.md#Detailed-Design]

## Dev Agent Record

### Context Reference

<!-- Path(s) to story context XML will be added here by context workflow -->

### Agent Model Used

Gemini 2.0 Flash

### Debug Log References

### Completion Notes List

### File List
