# Story 1.1: Project Initialization & Skeleton

Status: drafted

## Story

As a **Developer**,
I want **to initialize the frontend and backend repositories with the correct tech stack**,
so that **I have a working environment to build features upon.**

## Acceptance Criteria

1. **Frontend Initialization**: A Next.js 14 project is initialized with TypeScript and Tailwind CSS, and shadcn/ui is configured.
2. **Backend Initialization**: A Python project is initialized using `uv`, with `fastapi` and `uvicorn` installed.
3. **Concurrent Execution**: Both frontend and backend servers can run concurrently without errors.
4. **Git Configuration**: A `.gitignore` file is configured to exclude appropriate files (node_modules, .venv, etc.) for both projects.

## Tasks / Subtasks

- [ ] Initialize Next.js Frontend (AC: 1)
  - [ ] Run `npx create-next-app@latest frontend --typescript --tailwind --eslint`
  - [ ] Run `npx shadcn@latest init` in frontend directory
  - [ ] Verify frontend builds and runs (`npm run dev`)
- [ ] Initialize Python Backend (AC: 2)
  - [ ] Create `backend` directory
  - [ ] Run `uv init` in backend directory
  - [ ] Run `uv add fastapi uvicorn`
  - [ ] Create `backend/main.py` with basic "Hello World" endpoint
- [ ] Configure Git Ignore (AC: 4)
  - [ ] Create root `.gitignore` or verify individual `.gitignore` files
  - [ ] Ensure `node_modules/`, `.next/`, `.venv/`, `__pycache__/` are ignored
- [ ] Verify System Operation (AC: 3)
  - [ ] Start backend server (`uv run uvicorn main:app --reload`)
  - [ ] Start frontend server
  - [ ] Confirm both are accessible via browser/curl

## Dev Notes

- **Architecture**: Follows the split repository structure defined in the Architecture Document (Section 2).
- **Tech Stack**:
    - Frontend: Next.js 14, TypeScript, Tailwind CSS, shadcn/ui.
    - Backend: Python 3.12+, FastAPI, uv (package manager).
- **Testing**: Initial setup does not require complex tests, but ensure `npm run build` passes and python import works.

### References

- [Source: docs/epics.md#Story 1.1: Project Initialization & Skeleton]
- [Source: docs/architecture.md#2. System Architecture]

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
