# Story 2.3: Agent Configuration UI

Status: drafted

## Story

As a **Researcher**,
I want **to specify the number of agents and their personalities**,
so that **I can study how different populations behave.**

## Acceptance Criteria

1. **Agent Group Definition**: Users can define multiple "groups" of agents (e.g., "5 Cooperative Farmers"), specifying the count for each group.
2. **Job Assignment**: Each agent group must be assigned a valid Job ID from the list defined in the Job Configuration (Story 2.2).
3. **Attribute Configuration**: Users can define specific attributes for the agent group: "Culture" (string), "Needs" (dictionary/key-value), "Wants" (dictionary/key-value), and initial "Income".
4. **Validation**: The system must validate that the Agent Count is a positive integer and that required fields are populated.
5. **Config Integration**: The defined agent groups must be correctly structured to match the `AgentConfig` Pydantic model expected by the backend.

## Tasks / Subtasks

- [ ] Create `AgentEditor` Component (AC: 1)
  - [ ] Implement a list view for "Agent Groups" (similar to Job list).
  - [ ] Add "Add Agent Group" and "Remove Group" functionality.
- [ ] Implement Agent Group Form Fields (AC: 3)
  - [ ] Add numeric input for `count`.
  - [ ] Add text input for `culture`.
  - [ ] Add structured input (or JSON text area) for `needs` and `wants`.
  - [ ] Add numeric input for `income`.
- [ ] Integrate Job Selection (AC: 2)
  - [ ] Use a `Select` component populated with available Job IDs from the parent configuration state.
- [ ] Implement Validation Logic (AC: 4)
  - [ ] Ensure `count` > 0.
  - [ ] Ensure `job_id` is selected.
  - [ ] Ensure `needs`/`wants` are valid formats.
- [ ] Integrate with Parent Form (AC: 5)
  - [ ] Ensure the component updates the `agents` array in the main `SimulationConfig` object.

## Dev Notes

- **Architecture**: Follows the "Command Center" pattern (Frontend-driven config).
- **Tech Stack**: Next.js, React (State), shadcn/ui components (`Card`, `Input`, `Label`, `Select`, `Button`).
- **Data Model**:
  ```typescript
  // Frontend Interface matching Backend Pydantic
  interface AgentConfig {
    count: number;
    job_id: string;
    culture: string;
    needs: Record<string, number>;
    wants: Record<string, number>;
    income: number;
  }
  ```
- **UX**:
  - Consider using a `Card` for each Agent Group to visually separate them.
  - For `needs` and `wants`, a simple JSON text input is acceptable for MVP, or a dynamic Key-Value pair list if time permits.
  - This component is a child of the main `ConfigForm` wizard/page.

### References

- [Source: docs/epics.md#Story 2.3: Agent Configuration UI]
- [Source: docs/sprint-artifacts/tech-spec-epic-2.md]

## Dev Agent Record

### Context Reference

<!-- Path(s) to story context XML will be added here by context workflow -->

### Agent Model Used

Gemini 2.5 Flash

### Debug Log References

### Completion Notes List

### File List

## Change Log

- **[2025-12-08]**: Initial draft created by SM Agent.
