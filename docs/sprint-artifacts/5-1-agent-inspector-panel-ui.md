# Story 5.1: Agent Inspector Panel UI

Status: drafted

## Story

As a **Researcher**,
I want **to click on an agent to see their details**,
so that **I can understand their individual state**.

## Acceptance Criteria

1. **Open Panel:** Clicking an agent ID in the graph or log opens a side panel (`Sheet`).
2. **Static Info:** The panel displays the agent's Static Info: ID, Job, Culture.
3. **Dynamic Info:** The panel displays Dynamic Info: Current Inventory (item counts), Needs (status), Current Satisfaction/Score.
4. **Live Updates:** The data in the panel updates automatically with the next simulation tick (via polling).
5. **Close Panel:** Closing the panel clears the selection.

## Tasks / Subtasks

- [ ] **Frontend: Scaffold Inspector Component** (AC: 1, 5)
    - [ ] Create `src/components/dashboard/AgentInspector.tsx`.
    - [ ] Implement `shadcn/ui` `Sheet` component structure.
    - [ ] Add state for `isOpen` controlled by `selectedAgentId`.
- [ ] **Frontend: Define Data Types** (AC: 2, 3)
    - [ ] Define `AgentDetail` interface matching backend `Agent` model.
    - [ ] Ensure types align with `WorldState` structure.
- [ ] **Frontend: Implement Data Display** (AC: 2, 3)
    - [ ] Render static details (Name, Job, Culture).
    - [ ] Render dynamic inventory list/table.
    - [ ] Render needs status (e.g., using `Progress` bars or badges).
- [ ] **Frontend: Integration** (AC: 1, 4)
    - [ ] Connect `AgentInspector` to the global `WorldState` (via Zustand/Polling).
    - [ ] Implement selector logic: find agent in `WorldState.agents` by ID.
    - [ ] Add click handlers to `AgentInteractionDiagram` nodes to set `selectedAgentId`.
    - [ ] Add click handlers to `EventLog` agent IDs to set `selectedAgentId`.
- [ ] **Testing: Component Tests**
    - [ ] Test rendering with mock agent data.
    - [ ] Test open/close behavior.

## Dev Notes

- **Architecture:** Follows the "Command Center" design. The Inspector is a transient detail view overlaying the main dashboard.
- **State Management:** Use the existing polling mechanism. Do not create a separate API call for agent details unless `WorldState` becomes too large (unlikely for MVP). The Inspector should just filter the global state on the client side.
- **Component Library:** Use `shadcn/ui` `Sheet` for the sliding panel. Use `Badge` for jobs/culture.
- **Typing:** Strict TypeScript interfaces for the Agent data.

### Project Structure Notes

- **New Component:** `frontend/src/components/dashboard/AgentInspector.tsx`
- **Existing Hook:** Reuse `frontend/src/hooks/useSimulation.ts` (or similar polling hook created in Epic 4).

### References

- [Tech Spec Epic 5: Deep Inspection & Analysis](docs/sprint-artifacts/tech-spec-epic-5.md)
- [UX Design Specification: Agent Inspector](docs/ux-design-specification.md#112-custom-components)

## Dev Agent Record

### Context Reference

<!-- Path(s) to story context XML will be added here by context workflow -->

### Agent Model Used

Gemini 2.5 Flash

### Debug Log References

### Completion Notes List

### File List
