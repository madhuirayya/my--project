from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy import func, select
from typing import List, Optional
from datetime import datetime, timedelta

from . import models, schemas
from .database import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Campus Event Platform - Prototype", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
import os
frontend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "..", "frontend")
frontend_path = os.path.abspath(frontend_path)
app.mount("/frontend", StaticFiles(directory=frontend_path, html=True), name="frontend")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------- CRUD Endpoints ----------

@app.post("/colleges", response_model=schemas.CollegeOut)
def create_college(college: schemas.CollegeCreate, db: Session = Depends(get_db)):
    c = models.College(name=college.name)
    db.add(c)
    try:
        db.commit()
        db.refresh(c)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    return c

@app.get("/colleges", response_model=List[schemas.CollegeOut])
def list_colleges(db: Session = Depends(get_db)):
    return db.query(models.College).all()

import logging

logger = logging.getLogger("uvicorn.error")

@app.post("/students", response_model=schemas.StudentOut)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    s = models.Student(**student.model_dump())
    db.add(s)
    try:
        db.commit()
        db.refresh(s)
        logger.info(f"Student created: {s.name} with ID {s.id}")
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating student: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    return s

@app.get("/students", response_model=List[schemas.StudentOut])
def list_students(college_id: Optional[int] = None, db: Session = Depends(get_db)):
    q = db.query(models.Student)
    if college_id:
        q = q.filter(models.Student.college_id == college_id)
    return q.all()

@app.post("/events", response_model=schemas.EventOut)
def create_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
    e = models.Event(**event.model_dump())
    db.add(e)
    try:
        db.commit()
        db.refresh(e)
        logger.info(f"Event created: {e.title} with ID {e.id}")
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating event: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    return e

@app.get("/events", response_model=List[schemas.EventOut])
def list_events(college_id: Optional[int] = None, type: Optional[str] = None, db: Session = Depends(get_db)):
    q = db.query(models.Event)
    if college_id:
        q = q.filter(models.Event.college_id == college_id)
    if type:
        q = q.filter(models.Event.type.ilike(type))
    return q.order_by(models.Event.start_time.desc()).all()

@app.post("/register")
def register_student(payload: schemas.RegistrationCreate, db: Session = Depends(get_db)):
    reg = models.Registration(student_id=payload.student_id, event_id=payload.event_id)
    db.add(reg)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Registration failed or already exists")
    return {"status": "ok"}

@app.post("/attendance")
def mark_attendance(payload: schemas.AttendanceCreate, db: Session = Depends(get_db)):
    att = models.Attendance(student_id=payload.student_id, event_id=payload.event_id)
    db.add(att)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Attendance already marked or invalid data")
    return {"status": "ok"}

@app.post("/feedback")
def submit_feedback(payload: schemas.FeedbackCreate, db: Session = Depends(get_db)):
    if not (1 <= payload.rating <= 5):
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")
    fb = models.Feedback(
        student_id=payload.student_id,
        event_id=payload.event_id,
        rating=payload.rating,
        comment=payload.comment or ""
    )
    db.add(fb)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Feedback already submitted or invalid data")
    return {"status": "ok"}

# ---------- Reports ----------

@app.get("/reports/event-popularity", response_model=List[schemas.EventPopularity])
def event_popularity(college_id: Optional[int] = None, type: Optional[str] = None, db: Session = Depends(get_db)):
    q = (
        db.query(models.Event.id, models.Event.title, models.Event.type, func.count(models.Registration.id).label("registrations"))
        .join(models.Registration, models.Event.id == models.Registration.event_id, isouter=True)
    )
    if college_id:
        q = q.filter(models.Event.college_id == college_id)
    if type:
        q = q.filter(models.Event.type.ilike(type))
    q = q.group_by(models.Event.id).order_by(func.count(models.Registration.id).desc())
    result = []
    for e in q.all():
        result.append(schemas.EventPopularity(
            id=e[0],
            title=e[1],
            type=e[2],
            registrations=e[3]
        ))
    return result



@app.get("/reports/student-participation/{student_id}")
def student_participation(student_id: int, db: Session = Depends(get_db)):
    reg_count = db.query(func.count(models.Registration.id)).filter(models.Registration.student_id == student_id).scalar() or 0
    att_count = db.query(func.count(models.Attendance.id)).filter(models.Attendance.student_id == student_id).scalar() or 0
    return {"student_id": student_id, "registered_events": reg_count, "attended_events": att_count}

@app.get("/reports/top-active")
def top_active(limit: int = 3, db: Session = Depends(get_db)):
    q = (
        db.query(models.Student.id, models.Student.name, func.count(models.Attendance.id).label("attended"))
        .join(models.Attendance, models.Student.id == models.Attendance.student_id)
        .group_by(models.Student.id)
        .order_by(func.count(models.Attendance.id).desc())
        .limit(limit)
    )
    return [dict(student_id=r[0], name=r[1], attended=r[2]) for r in q.all()]

@app.get("/reports/event-stats/{event_id}", response_model=schemas.EventStats)
def event_stats(event_id: int, db: Session = Depends(get_db)):
    regs = db.query(func.count(models.Registration.id)).filter(models.Registration.event_id == event_id).scalar() or 0
    atts = db.query(func.count(models.Attendance.id)).filter(models.Attendance.event_id == event_id).scalar() or 0
    avg_fb = db.query(func.avg(models.Feedback.rating)).filter(models.Feedback.event_id == event_id).scalar()
    percent = float(atts) / regs * 100 if regs else 0.0
    return schemas.EventStats(event_id=event_id, registrations=regs, attendance=atts, attendance_percent=round(percent,2), avg_feedback=float(avg_fb) if avg_fb is not None else None)

# ---------- Seed helper ----------

@app.post("/seed")
def seed(db: Session = Depends(get_db)):
    if db.query(models.College).count() > 0:
        return {"status": "skipped", "reason": "Already seeded"}
    c = models.College(name="Acharya Institute of Technology")
    db.add(c)
    db.flush()

    s1 = models.Student(name="Alice", email="alice@example.com", college_id=c.id)
    s2 = models.Student(name="Bob", email="bob@example.com", college_id=c.id)
    db.add_all([s1, s2])
    db.flush()

    now = datetime.utcnow()
    e1 = models.Event(title="Intro to FastAPI", description="Hands-on workshop", type="Workshop",
                      start_time=now + timedelta(days=1), end_time=now + timedelta(days=1, hours=2), college_id=c.id)
    e2 = models.Event(title="Tech Talk: AI", description="Seminar on AI trends", type="Seminar",
                      start_time=now + timedelta(days=2), end_time=now + timedelta(days=2, hours=1), college_id=c.id)
    db.add_all([e1, e2])
    db.commit()
    return {"status": "ok"}
