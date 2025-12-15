# Code Review: Errors and Inconsistencies

## CRITICAL Issues

### 1. **Missing Export Method in API Client** ⚠️
- **Location**: `frontend/lib/api.ts`
- **Issue**: No `exportEventLog()` method, but Layout component needs it
- **Impact**: Inconsistent API usage, hardcoded fetch in Layout component
- **Fix**: Add `exportEventLog()` method to ApiClient class

### 2. **Duplicate Store Files** 🔴
- **Location**: 
  - `frontend/src/store/simulation.ts`
  - `frontend/app/store/simulation.ts`
- **Impact**: Confusion about which file is used, potential import errors
- **Issue**: Both files contain identical code but are in different locations
- **Fix**: Remove one and standardize on a single location (prefer `app/store/` for Next.js App Router)

### 3. **Hardcoded API URL in Layout Component** 🔴
- **Location**: `frontend/src/components/dashboard/Layout.tsx:36`
- **Code**: `const response = await fetch('http://localhost:8000/api/export');`
- **Impact**: Inconsistent with API client pattern, breaks in production
- **Fix**: Use `apiClient.exportEventLog()` method or add export method to ApiClient

### 4. **Agent Inventory Never Initialized** 🔴
- **Location**: `backend/app/main.py:112`
- **Code**: `"inventory": {},  # Will be populated based on job`
- **Impact**: Agents start with empty inventory, cannot trade
- **Issue**: Comment indicates intent but implementation is missing
- **Fix**: Initialize inventory based on job configuration (jobs list contains `resource_produced`)

### 5. **Deprecated datetime.utcnow() Usage** 🔴
- **Location**: `backend/app/main.py:65`
- **Code**: `datetime.utcnow().isoformat() + "Z"`
- **Impact**: `datetime.utcnow()` is deprecated in Python 3.12+
- **Fix**: Use `datetime.now(timezone.utc)` instead

### 6. **Invalid asyncio Dependency** 🔴
- **Location**: `backend/pyproject.toml:7`
- **Code**: `"asyncio>=4.0.0"`
- **Impact**: `asyncio` is part of Python standard library, should not be in dependencies
- **Issue**: There is no `asyncio` package on PyPI version 4.0.0
- **Fix**: Remove from dependencies (asyncio is built-in)

### 7. **Missing Error Handling for Agent Creation** 🔴
- **Location**: `backend/app/agents/implementation.py:21-23`
- **Impact**: If `GEMINI_API_KEY` is missing, agent creation fails but error may not be caught
- **Fix**: Add proper error handling in agent instantiation

## IMPORTANT Issues

### 8. **Inconsistent Import Paths** ⚠️
- **Location**: Multiple frontend files
- **Issue**: Mix of `@/src/components` and `@/components` imports
- **Examples**:
  - `frontend/app/dashboard/page.tsx` uses `@/src/components/dashboard/Layout`
  - `frontend/app/config/page.tsx` uses `@/components/ui/button`
- **Impact**: Confusion about project structure, potential build issues
- **Fix**: Standardize on one import pattern (prefer `@/components` without `src`)

### 9. **Missing Type Definitions** ⚠️
- **Location**: `frontend/lib/api.ts:14-16`
- **Code**: `agents: any[]; event_log: any[]; market_history: any[];`
- **Impact**: Loss of type safety, potential runtime errors
- **Fix**: Define proper TypeScript interfaces for Agent, Event, and MarketHistory

### 10. **No Validation of Job-Resource Mapping** ⚠️
- **Location**: `backend/app/main.py:103-116`
- **Issue**: Agents are created with job names, but no validation that job exists in config.jobs
- **Impact**: Agents can have invalid jobs, breaking simulation logic
- **Fix**: Validate agent.job exists in config.jobs before creating agents

### 11. **Missing Metadata in Layout** ⚠️
- **Location**: `frontend/app/layout.tsx:15-18`
- **Code**: Generic "Create Next App" metadata
- **Impact**: Poor SEO and branding
- **Fix**: Update to "AIES - AI Economy Simulator" with proper description

### 12. **Unused Root main.py** ⚠️
- **Location**: `backend/main.py`
- **Code**: Just prints "Hello from backend!"
- **Impact**: Confusion about entry point
- **Fix**: Remove or document purpose (seems like test file)

### 13. **Missing .env File/Example** ⚠️
- **Location**: Root directory
- **Impact**: No documentation for required environment variables
- **Required**: `GEMINI_API_KEY`
- **Fix**: Create `.env.example` with required variables

### 14. **No Error Handling in Simulation Loop** ⚠️
- **Location**: `backend/app/main.py:16-28`
- **Issue**: If `engine.tick()` raises exception, simulation loop crashes
- **Impact**: Simulation stops without error message
- **Fix**: Add try-except block with logging

## MEDIUM Issues

### 15. **Inconsistent Polling Intervals** 📝
- **Location**: Multiple frontend components
- **Issue**: Different polling intervals across components:
  - `EventLog.tsx`: 2000ms
  - `EconomicGraph.tsx`: 3000ms
  - `AgentInspector.tsx`: 2000ms
  - `AgentInteractionDiagram.tsx`: 3000ms
- **Impact**: Inconsistent UI updates
- **Fix**: Standardize on single interval or make configurable

### 16. **Missing Input Validation for JSON Fields** 📝
- **Location**: `frontend/app/config/page.tsx:32-33`
- **Code**: `needs: z.string().default('{}')` and `wants: z.string().default('{}')`
- **Issue**: No validation that string is valid JSON
- **Impact**: Invalid JSON causes backend errors
- **Fix**: Add JSON validation to Zod schema

### 17. **Resource Inference Logic is Fragile** 📝
- **Location**: `backend/app/agents/implementation.py:70`
- **Code**: `target_resource = target_job.lower().replace('er', '').replace('man', '').capitalize()`
- **Issue**: Brittle string manipulation, won't work for many job names
- **Impact**: Incorrect resource inference for non-standard job names
- **Fix**: Use job-to-resource mapping from config

### 18. **No WebSocket Implementation** 📝
- **Location**: Architecture mentions WebSocket support but only REST is implemented
- **Impact**: Polling overhead, not real-time updates
- **Fix**: Implement WebSocket for real-time state updates (or remove from docs)

### 19. **Missing Agent Class Instantiation** 📝
- **Location**: `backend/app/main.py:105-115`
- **Issue**: Agents are created as plain dicts, not `GeminiAgent` instances
- **Impact**: Agent methods cannot be called, LLM integration not used
- **Fix**: Instantiate `GeminiAgent` objects instead of dicts

### 20. **Inconsistent Error Messages** 📝
- **Location**: Multiple files
- **Issue**: Some errors use console.error, some use print, some return error responses
- **Impact**: Difficult to debug, inconsistent logging
- **Fix**: Standardize on logging framework (e.g., Python `logging`, frontend error boundaries)

## VOLUNTARY Improvements

### 21. **Code Duplication in Error Handling** 💡
- **Location**: `backend/app/agents/implementation.py:56-60, 105-109, 148-152`
- **Issue**: Similar try-except blocks with ValidationError handling
- **Fix**: Extract to helper method

### 22. **Missing Type Hints** 💡
- **Location**: `backend/app/main.py:105-115`
- **Issue**: Agent dicts use `any` type implicitly
- **Fix**: Define TypedDict or use Pydantic models

### 23. **Hardcoded Magic Numbers** 💡
- **Location**: `backend/app/main.py:12`
- **Code**: `Engine(ticks_per_day=10)`
- **Issue**: Magic number should come from config
- **Fix**: Use `config.day_length_seconds` to calculate ticks

### 24. **Missing Loading States** 💡
- **Location**: Frontend components
- **Issue**: No loading indicators while fetching data
- **Fix**: Add loading states to all async operations

### 25. **No Rate Limiting** 💡
- **Location**: Backend API endpoints
- **Issue**: No protection against API abuse
- **Fix**: Add rate limiting middleware

### 26. **Missing Unit Tests** 💡
- **Location**: Entire codebase
- **Issue**: No test files found
- **Fix**: Add unit tests for core logic

### 27. **Inconsistent Naming** 💡
- **Location**: `backend/app/main.py:65`
- **Issue**: Uses `datetime.utcnow()` but adds "Z" manually
- **Fix**: Use proper timezone-aware datetime

### 28. **Missing Documentation Strings** 💡
- **Location**: Multiple Python files
- **Issue**: Some functions lack docstrings
- **Fix**: Add comprehensive docstrings

## UNNECESSARY / Cleanup

### 29. **Empty __init__.py Files** 🧹
- **Location**: All `__init__.py` files in backend
- **Issue**: Only contain comments, no actual code
- **Fix**: Remove or add actual package exports

### 30. **Unused Import** 🧹
- **Location**: `backend/app/agents/implementation.py:33, 56`
- **Issue**: `ValidationError` imported but check happens after import
- **Fix**: Move import to top or remove redundant check

### 31. **Commented Code** 🧹
- **Location**: `backend/app/core/engine.py:36-37`
- **Code**: `# Reset daily event budgets for all agents (to be implemented in Epic 3)`
- **Fix**: Remove or create TODO/issue tracker entry

### 32. **Duplicate Store Import Paths** 🧹
- **Location**: `frontend/app/config/page.tsx:20` vs `frontend/src/components/dashboard/Layout.tsx:5`
- **Issue**: Different import paths for same store
- **Fix**: Standardize import path

---

## Summary by Priority

- **CRITICAL**: 7 issues (must fix before production)
- **IMPORTANT**: 7 issues (should fix soon)
- **MEDIUM**: 6 issues (nice to have)
- **VOLUNTARY**: 8 issues (code quality improvements)
- **UNNECESSARY**: 4 issues (cleanup)

**Total Issues Found**: 32

---

## Quick Fix Priority Guide

### Must Fix Immediately (Critical)
1. Remove invalid `asyncio` dependency from `pyproject.toml`
2. Fix deprecated `datetime.utcnow()` usage
3. Initialize agent inventory based on job configuration
4. Add proper error handling in simulation loop
5. Fix hardcoded API URL in Layout component
6. Remove duplicate store files
7. Add validation for job-resource mapping

### Should Fix Soon (Important)
8. Standardize import paths (`@/src/components` vs `@/components`)
9. Add proper TypeScript interfaces (replace `any[]` types)
10. Add JSON validation for needs/wants fields
11. Update layout metadata
12. Create `.env.example` file
13. Instantiate GeminiAgent objects instead of plain dicts

### Nice to Have (Medium)
14. Standardize polling intervals
15. Fix resource inference logic
16. Add loading states to UI
17. Implement proper error logging
18. Add WebSocket support (or remove from docs)

### Code Quality (Voluntary)
19. Extract duplicate error handling code
20. Add type hints throughout
21. Remove magic numbers
22. Add unit tests
23. Improve documentation

### Cleanup (Unnecessary)
24. Remove empty `__init__.py` comments or add exports
25. Clean up unused imports
26. Remove commented code or create TODOs

