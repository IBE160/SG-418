# Implementation Patterns

## Category: Naming Patterns
*   **Pattern:** Python Snake Case vs. JS Camel Case
*   **Convention:**
    *   **Python (Backend):** `user_id`, `simulation_state` (snake_case)
    *   **API JSON:** `userId`, `simulationState` (camelCase) - *Automatic Conversion*
    *   **JS (Frontend):** `userId`, `simulationState` (camelCase)
*   **Enforcement:** Configure Pydantic to `populate_by_name=True` and use `alias_generator=to_camel`. This prevents the "variable_name mismatch" bugs.

## Category: Structure Patterns
*   **Pattern:** Feature-First Organization
*   **Convention:** Group code by *what it does*, not *what it is*.
*   **Example:** Instead of `components/buttons` and `components/graphs`, use `components/features/simulation-controls` and `components/features/economic-graph`.

## Category: API Patterns
*   **Pattern:** Typed API Client
*   **Convention:** Frontend `api.ts` must use TypeScript interfaces that match Backend Pydantic models 1:1.
*   **Enforcement:** "If you change a Pydantic model, you MUST update the TypeScript interface."

## Category: Error Patterns
*   **Pattern:** Graceful Degradation
*   **Convention:** If the simulation engine is busy or slow, the frontend shows a "Syncing..." spinner, never a crash.
