# Story 2.1: Global Configuration Form

Status: drafted

## Story

As a **Researcher**,
I want **to set global parameters like simulation duration**,
so that **I can control the scope of the experiment.**

## Acceptance Criteria

1.  **Given** I am on the "New Simulation" page
    **When** I enter values for "Day Length (seconds)" and "Max Days"
    **Then** the form should validate that inputs are positive integers
    **And** I should be able to proceed to the next step

## Tasks / Subtasks

- [ ] Backend: Define `GlobalConfig` Pydantic model
    - [ ] Create `backend/models/domain.py` if not exists
    - [ ] Implement `GlobalConfig` with fields `day_length_seconds` and `max_days`
    - [ ] Add validation (gt=0)
- [ ] Frontend: Create Configuration Form Shell
    - [ ] Initialize `frontend/app/config/` directory
    - [ ] Create `ConfigForm` component using `react-hook-form` and `zod`
    - [ ] Implement UI for "Day Length" and "Max Days" using shadcn `Input`
- [ ] Frontend: Implement Validation Logic
    - [ ] Define Zod schema matching backend constraints (positive integers)
    - [ ] Display error messages for invalid inputs
- [ ] Frontend: State Management
    - [ ] Set up local state or Zustand store to hold partial config
    - [ ] Ensure valid data is persisted when moving to next step

## Dev Notes

- **Architecture**: This story implements the "Global Configuration" part of the `SimulationConfig` schema defined in the [Tech Spec](../sprint-artifacts/tech-spec-epic-2.md).
- **Backend Model**:
    ```python
    class GlobalConfig(BaseModel):
        day_length_seconds: int = Field(..., gt=0)
        max_days: int = Field(..., gt=0)
    ```
- **Frontend Components**: Use `shadcn/ui` Form and Input components.
- **Previous Story**: Story 1.4 (Frontend-Backend Connection) is currently `drafted`, so no implementation learnings are available yet.

### Project Structure Notes

- Backend models should reside in `backend/models/domain.py`.
- Frontend config components should reside in `frontend/app/config/`.

### References

- [Epic 2 Tech Spec](../sprint-artifacts/tech-spec-epic-2.md)
- [PRD - FR1.1 Global Configuration](../PRD.md#31-simulation-setup--configuration)

## Dev Agent Record

### Context Reference

<!-- Path(s) to story context XML will be added here by context workflow -->

### Agent Model Used

Gemini 2.5 Flash

### Debug Log References

### Completion Notes List

### File List
