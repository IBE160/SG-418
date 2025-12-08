# Story 3.1: LLM Integration Infrastructure

Status: drafted

## Story

As a Developer,
I want to integrate `pydantic-ai` with Google Gemini,
so that I can send structured prompts and receive validated JSON responses.

## Acceptance Criteria

1. **Environment Setup:** `pydantic-ai` and `google-generativeai` are installed and configured.
2. **Gemini Client Wrapper:** The service successfully authenticates with Google's API using `GEMINI_API_KEY` and uses `gemini-1.5-flash`.
3. **Structured Response Validation:** Sending a prompt requesting a specific Pydantic model structure returns a valid instance of that model.
4. **Validation Error Handling:** Invalid LLM output raises a catchable `ValidationError`.

## Tasks / Subtasks

- [ ] Dependency Management (AC: 1)
  - [ ] Add `pydantic-ai`, `google-generativeai`, `python-dotenv` via `uv`
  - [ ] Update `.env.example`
- [ ] Implement LLM Service Module (AC: 2)
  - [ ] Create `backend/app/llm/` directory
  - [ ] Create `backend/app/llm/config.py` for API key and model constants
  - [ ] Create `backend/app/llm/service.py` with `GeminiService` class/wrapper
- [ ] Implement Integration Test (AC: 3, 4)
  - [ ] Create `tests/test_llm_integration.py`
  - [ ] Define test Pydantic model
  - [ ] Test successful structured response
  - [ ] Test error handling/validation failure

## Dev Notes

- **Architecture Alignment:**
  - Follows "Cognitive Engine" components defined in Architecture Doc.
  - Backend (FastAPI) + Pydantic-AI.
  - No database persistence required for this story.
- **Source Tree Components:**
  - `backend/app/llm/`
  - `pyproject.toml`
  - `.env`
- **Testing Standards:**
  - Use `pytest` (implied by python env, verify if installed).
  - Mocking the API call is preferred for unit tests to save credits, but a live integration test (marked as such) is needed to verify the API connection.

### Project Structure Notes

- Alignment with unified project structure: `backend/app/` for application logic.
- Decision: Use `pydantic-ai` v0.0.1+ as per Tech Spec.

### References

- [Tech Spec Epic 3](../sprint-artifacts/tech-spec-epic-3.md#detailed-design)
- [Architecture Document](../architecture.md#technology-stack-details)

## Dev Agent Record

### Context Reference

<!-- Path(s) to story context XML will be added here by context workflow -->

### Agent Model Used

Gemini 2.5 Flash

### Debug Log References

### Completion Notes List

### File List