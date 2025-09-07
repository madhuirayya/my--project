# Campus Event Reporting Prototype

This project is a prototype for managing campus events, including creating colleges, students, and events, as well as tracking registrations, attendance, and feedback. It also provides reports on event popularity and student participation.

## How to Run (Development)

### Backend
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Run the setup and start the server:
   - On Linux/macOS:
     ```bash
     bash run.sh
     ```
   - On Windows PowerShell:
     ```powershell
     cd backend
     python -m venv .venv
     . .venv\Scripts\activate
     pip install -r requirements.txt
     uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
     ```
3. The backend server will be running at [http://localhost:8000](http://localhost:8000). You can access the Swagger UI for API documentation at [http://localhost:8000/docs](http://localhost:8000/docs).

### Frontend
Open the `frontend/index.html` file in your web browser directly, or serve it using any static file server.

## Quick Start
- Call the POST endpoint `/seed` once to populate the database with sample data.
- Use the frontend UI to create colleges, students, events, register students, mark attendance, and submit feedback.
- View reports on event popularity, student participation, and top active students.

## Notes
- The SQLite database file is located at `backend/events.db` and is created automatically.
- This project fulfills the assignment requirements for tracking registrations, attendance, feedback, and generating reports.

## AI Conversation Logs
Please include screenshots of AI conversations and relevant links in the `ai_log/` directory before submission.

---

Feel free to customize this README further to suit your needs.
