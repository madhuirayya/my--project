# Campus Event Reporting Prototype

> Replace this README with **your own words** before submission. Do **not** paste AI content here.

## How to Run (Dev)
### Backend
```bash
cd backend
bash run.sh
# Server at http://localhost:8000 (Swagger at /docs)
```
Windows PowerShell:
```powershell
cd backend
python -m venv .venv
. .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend
Open `frontend/index.html` in your browser (or serve with any static server).

## Quick Start
1. Call `POST http://localhost:8000/seed` once to create sample data.
2. Use the UI to register, attend, and send feedback.
3. Open Swagger at `http://localhost:8000/docs` to try endpoints.

## Notes
- DB file is `backend/events.db` (auto-created).
- This project implements the assignment requirements: tracking registrations, attendance, feedback, and generating required reports.
- Include **AI conversation screenshots** in `ai_log/` before submitting.
