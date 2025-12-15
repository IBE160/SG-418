# Story 2.2: Job & Resource Definition UI

**Status:** drafted

## Story

As a **Researcher**,
I want **to define the jobs available in the economy and what resources they produce**,
so that **I can simulate different economic structures.**

## Acceptance Criteria

1.  **Job List Interface:** Users can view a list of currently defined jobs.
2.  **Add/Remove Capability:** Users can add a new job definition and remove an existing one.
3.  **Job Definition Fields:** Each job entry must specify:
    *   **Job ID** (e.g., "Woodcutter")
    *   **Resource Produced** (e.g., "Wood")
4.  **Validation:**
    *   Duplicate Job IDs are prevented.
    *   Job ID and Resource fields cannot be empty.
5.  **Defaults:** The configuration defaults to including at least two jobs (e.g., "Woodcutter", "Stonemason") when initialized.

## Tasks / Subtasks

- [ ] **Backend: Define Job Configuration Model**
    - [ ] Create `JobConfig` Pydantic model in `backend/models/domain.py`.
    - [ ] Fields: `job_id` (str), `resource_produced` (str).
    - [ ] Add unit tests for model validation (non-empty fields).

- [ ] **Frontend: Create JobEditor Component**
    - [ ] Create `frontend/app/config/JobEditor.tsx`.
    - [ ] Implement `JobEditor` as a controlled component (props: `jobs`, `onChange`).
    - [ ] Use `shadcn/ui` `Table` or `Card` list for layout.
    - [ ] Use `Input` fields for Job ID and Resource Produced.
    - [ ] Add "Add Job" button and "Remove" (trash icon) button per row.

- [ ] **Frontend: Implement Validation Logic**
    - [ ] Prevent adding/saving duplicates in the `JobEditor` state.
    - [ ] Display error message if duplicate Job ID is detected.
    - [ ] Ensure inputs are required.

- [ ] **Frontend: Integration & Defaults**
    - [ ] Define default jobs constant (Woodcutter, Stonemason).
    - [ ] Create a Storybook story or a temporary test page to verify `JobEditor` functionality in isolation (since Story 2.1 might not be ready).

- [ ] **Testing**
    - [ ] Unit test `JobConfig` model constraints.
    - [ ] Component test `JobEditor`:
        - [ ] Verify adding a row works.
        - [ ] Verify removing a row works.
        - [ ] Verify validation error on duplicate ID.

## Dev Notes

- **Dependencies:** This story relies on the UI library (`shadcn/ui`) being set up (Story 1.1).
- **State Management:** The `JobEditor` should be a "dumb" component that receives data and emits changes, allowing the parent `ConfigForm` (Story 2.1) to manage the global configuration state.
- **Validation:** While the backend will ultimately validate the full config, client-side validation in this component is crucial for immediate user feedback.

### Project Structure Notes

- **Backend:** `backend/models/domain.py` is the home for shared configuration models.
- **Frontend:** `frontend/app/config/` is the designated directory for configuration-related components as per the Tech Spec.

### References

- [Epic 2 Tech Spec: Detailed Design](../sprint-artifacts/tech-spec-epic-2.md#detailed-design)
- [PRD: FR1.2 Job & Resource Configuration](../PRD.md#31-simulation-setup--configuration)
- [Architecture: Data Models](../architecture.md#9-data-architecture)

## Dev Agent Record

### Context Reference

<!-- Path(s) to story context XML will be added here by context workflow -->

### Agent Model Used

Gemini 2.0 Flash

### Debug Log References

### Completion Notes List

### File List
