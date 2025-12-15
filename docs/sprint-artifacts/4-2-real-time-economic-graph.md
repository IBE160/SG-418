# Story 4.2: Real-Time Economic Graph

Status: drafted

## Story

As a **Researcher**,
I want **to see a live graph of the Total Economic Value**,
so that **I can assess if the economy is growing or crashing.**

## Acceptance Criteria

1.  **Data Availability:** The backend `WorldState` includes a `market_history` list containing time-series data (tick count and value) since the start of the simulation.
2.  **Metric Calculation:** The system calculates a "Total Economic Value" (e.g., sum of all agent resource counts or utility) at every tick and appends it to the history.
3.  **Visualization:** The Dashboard displays a Line Chart rendering the `market_history`.
4.  **Live Updates:** The chart updates automatically as new state is polled (without page refresh).
5.  **Performance:** The chart renders efficiently with up to 1000 data points.

## Tasks / Subtasks

- [ ] Backend: Update Domain Models
  - [ ] Update `WorldState` in `backend/models/domain.py` to include `market_history: List[MarketMetric]`.
  - [ ] Define `MarketMetric` model (tick: int, total_value: float).
- [ ] Backend: Implement Value Calculation
  - [ ] Add helper function `calculate_global_value(agents)` in `backend/core/engine.py`.
    -   *Metric:* Sum of all resources held by all agents (MVP simple wealth).
  - [ ] Update `Engine.step()` to calculate value and append to `state.market_history`.
- [ ] Frontend: Setup Visualization
  - [ ] Install `recharts` (if not already installed).
  - [ ] Create `components/dashboard/EconomyChart.tsx`.
  - [ ] Implement `ResponsiveContainer` and `LineChart` with XAxis (tick) and YAxis (value).
- [ ] Frontend: Integration
  - [ ] Update `DashboardPage` (or layout) to include `EconomyChart`.
  - [ ] Pass `market_history` from the `useSimulationState` hook to the chart.
- [ ] Testing
  - [ ] Unit Test: Verify `calculate_global_value` returns correct sum.
  - [ ] Manual Test: Start simulation, observe chart growing over time.

## Dev Notes

- **Metric Definition (MVP):** "Total Economic Value" = Sum of quantities of all resources in all agent inventories.
  -   *Future:* Switch to "Total Subjective Utility" once needs/wants are fully implemented.
- **Data Volume:** If `market_history` grows indefinitely, it will bloat the `/api/state` payload.
  -   *Mitigation (MVP):* Accept this risk for MVP. Post-MVP will need pagination or delta updates (as noted in Tech Spec).
- **Frontend Lib:** `recharts` is the standard choice. Ensure `ResponsiveContainer` is used so it fits the grid cell defined in Story 4.1.

### Project Structure Notes

- **Backend Models:** `backend/models/domain.py`
- **Backend Engine:** `backend/core/engine.py`
- **Frontend Component:** `frontend/src/components/dashboard/EconomyChart.tsx`

### References

- [Source: docs/sprint-artifacts/tech-spec-epic-4.md#Detailed-Design]
- [Source: docs/epics.md#Story-4.2]
- [Source: docs/architecture.md#Decision-Summary-Table]

## Dev Agent Record

### Context Reference

<!-- Path(s) to story context XML will be added here by context workflow -->

### Agent Model Used

Gemini 2.5 Flash

### Debug Log References

### Completion Notes List

### File List
