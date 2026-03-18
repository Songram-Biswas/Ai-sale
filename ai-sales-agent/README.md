## ai-sales-agent

Minimal production-style scaffold for an AI Sales Agent API (FastAPI) backed by MongoDB (pymongo), plus a small Streamlit UI.

### What’s included
- **FastAPI**: `/health`, `/analyze_company`, `/generate_report`
- **MongoDB**: connection wrapper in `app/models/db.py`
- **Config via env vars**: `app/config.py`
- **Basic logging**: `app/utils/logger.py`
- **Streamlit**: input a company URL and view insights
- **Tests**: basic pytest smoke tests

### Run locally (Python)
Create a virtualenv, install deps, then start the API:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Optional Streamlit UI:

```bash
streamlit run streamlit_app/app.py
```

### Run with Docker

```bash
docker compose up --build
```

Then open:
- API: `http://localhost:8000/health`

