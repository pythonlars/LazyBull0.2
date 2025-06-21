# PLANNING – LazyBull

_Last updated: 2025-06-21_

## Goal
Provide traders with an instant, reliable technical-analysis of any chart, directly from the browser.

## Milestones
1. ✅ MVP – screenshot capture, FastAPI backend, Gemini analysis
2. ◻️ Test suite – unit (pytest), E2E (Playwright)
3. ◻️ UX polish – show loading spinner, copyable YAML output
4. ◻️ Deploy backend to Fly.io, add auth & rate limiting
5. ◻️ Release to Chrome Web Store

## Design decisions
* **Backend**: FastAPI for simplicity, served by Uvicorn.
* **AI**: Google Gemini models, try flash → pro-vision fallback strategy.
* **Extension**: Manifest V3, minimal permissions (`activeTab`, `tabs`), communicates via `fetch`.
* **Security**: No API keys in frontend; backend reads from environment. All untrusted file uploads stored in temp dir and deleted.
* **Testing**: pytest/Playwright. All new code requires tests.

## File/Folder rules
* Max 500 lines per file (see `user_global` rules).
* Keep frontend in `extension/`, backend at root.
* Relative imports only.
* Each module gets a `README.md` if it grows >1 file.

## TODO backlog
* Add Pydantic request/response models
* Create `/healthz` endpoint for uptime monitoring
* Add `Sentry` integration (backend + extension)
* Write Playwright test that captures dummy page and asserts YAML fields

> All TODOs found during coding must also be logged under **Discovered During Work** in `TASK.md`.
