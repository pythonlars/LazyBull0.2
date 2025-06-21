# LazyBull – Stock Chart Analyzer

LazyBull is a small toolbox that lets you capture any chart that is visible in your browser and instantly run an AI powered technical-analysis on it.

• **Chrome Extension** – grabs a screenshot from the current tab and sends it to the backend.
• **FastAPI Backend** – receives the image, calls Google Gemini (via the `google-generativeai` SDK) and returns a concise, data-driven analysis.
• **Python CLI** – `main.py` allows quick experiments without the browser extension.

## Quick start

1. **Create a virtualenv**
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```
2. **Install deps**
```bash
pip install -r requirements.txt
```
3. **Add your Google API key**
```
# .env
GOOGLE_API_KEY=<your-key>
```
4. **Run backend**
```bash
uvicorn fastapi_app:app --reload --port 8000
```
5. **Load the extension**
   • Navigate to `chrome://extensions` → Enable *Developer mode* → *Load unpacked* → choose the `extension/` folder.

Now browse to any chart, click the *LazyBull* icon and hit *Start Capture & Analyze*.

## Project layout

```
tradingadvisortry5/
│  fastapi_app.py   # FastAPI server
│  main.py          # Stand-alone CLI entrypoint
│  requirements.txt # Python deps
│  .env.example     # Example env file (copy to .env)
│
├─extension/        # Chrome extension (MV3)
│   manifest.json   # Extension metadata
│   popup.html      # Minimal UI
│   popup.js        # Capture + fetch logic
│
└─tests/            # pytest + Playwright tests (to be implemented)
```

## Tests
Run unit tests via `pytest`, E2E via `playwright test` (Playwright config TBD).

## Security & QA
* Input validated with Pydantic, API key loaded from `.env` (never commit secrets).
* CI (GitHub Actions) will run `black`, `flake8`, `bandit`, plus all tests.

## Roadmap
See `PLANNING.md` for detailed milestones.
