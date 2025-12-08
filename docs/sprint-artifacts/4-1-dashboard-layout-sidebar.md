# Story 4.1: Dashboard Layout & Sidebar

Status: drafted

## Story

As a **User**,
I want **a responsive dashboard layout with a sidebar**,
so that **I can navigate between different monitoring views.**

## Acceptance Criteria

1.  **Dashboard Layout:** The `/dashboard` route renders a layout with a persistent sidebar and a main content area.
2.  **Navigation:** The sidebar contains global controls and navigation links (even if some are placeholders for now).
3.  **Responsiveness:** The layout adapts to screen size (e.g., sidebar collapses or becomes a drawer on mobile).
4.  **Placeholders:** The main content area has defined regions (grid/cards) ready for the Graph, Log, and Diagram widgets.
5.  **Offline Indicator:** A placeholder or mechanism for showing system status (connected/offline) is visible (per Tech Spec AC5 foundation).

## Tasks / Subtasks

- [ ] Initialize Dashboard Route
  - [ ] Create `app/dashboard/page.tsx`
  - [ ] Create `app/dashboard/layout.tsx` (if using Next.js layouts)
- [ ] Implement Sidebar Component
  - [ ] Create `components/dashboard/Sidebar.tsx`
  - [ ] Add navigation links (Overview, Agents, Events, Settings) using `lucide-react` icons
  - [ ] Style with `shadcn/ui` components (Button, Separator)
- [ ] Implement Main Content Shell
  - [ ] Create grid layout for widgets (Top: Stats/Controls, Middle: Charts, Bottom: Logs)
  - [ ] Create placeholder components (`EconomyChartPlaceholder`, `EventLogPlaceholder`, `InteractionGraphPlaceholder`)
- [ ] Responsive Design
  - [ ] Implement mobile toggle for sidebar (Sheet component from `shadcn`)
  - [ ] Verify layout on mobile, tablet, and desktop breakpoints

## Dev Notes

- **Architecture:** Follow Split-Stack. Frontend (Next.js) only for this story.
- **Design:** "Command Center" style. Dark mode compatibility is recommended.
- **Components:** Use `shadcn/ui` `Resizable` panel group or CSS Grid for the main layout.
- **Future Proofing:** Ensure the layout structure supports the widget placement defined in the Tech Spec (Chart, Log, Graph).

### Project Structure Notes

- **Path:** `frontend/src/app/dashboard/...` (assuming src directory, verify project structure)
- **Components:** `frontend/src/components/dashboard/...`

### References

- [Source: docs/epics.md#Story-4.1]
- [Source: docs/sprint-artifacts/tech-spec-epic-4.md#Detailed-Design]

## Dev Agent Record

### Context Reference

<!-- Path(s) to story context XML will be added here by context workflow -->

### Agent Model Used

Gemini 2.0 Flash

### Debug Log References

### Completion Notes List

### File List
