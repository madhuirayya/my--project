from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, List
from datetime import datetime

class CollegeCreate(BaseModel):
    name: str

    @field_validator('name')
    @classmethod
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('name must not be empty')
        return v.strip()

class CollegeOut(BaseModel):
    id: int
    name: str
    class Config:
        from_attributes = True

class StudentCreate(BaseModel):
    name: str
    email: EmailStr
    college_id: int

    @field_validator('name')
    @classmethod
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('name must not be empty')
        return v.strip()

class StudentOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    college_id: int
    class Config:
        from_attributes = True

class EventCreate(BaseModel):
    title: str
    description: Optional[str] = ""
    type: str = Field(description="Workshop/Fest/Seminar/Other")
    start_time: datetime
    end_time: datetime
    college_id: int

    @field_validator('end_time')
    @classmethod
    def end_time_must_be_after_start_time(cls, v, info):
        start_time = info.data.get('start_time')
        if start_time and v <= start_time:
            raise ValueError('end_time must be after start_time')
        return v

class EventOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    type: str
    start_time: datetime
    end_time: datetime
    college_id: int
    class Config:
        from_attributes = True

class RegistrationCreate(BaseModel):
    student_id: int
    event_id: int

class AttendanceCreate(BaseModel):
    student_id: int
    event_id: int

class FeedbackCreate(BaseModel):
    student_id: int
    event_id: int
    rating: int
    comment: Optional[str] = ""

    @field_validator('rating')
    @classmethod
    def rating_must_be_between_1_and_5(cls, v):
        if not (1 <= v <= 5):
            raise ValueError('rating must be between 1 and 5')
        return v

class EventStats(BaseModel):
    event_id: int
    registrations: int
    attendance: int
    attendance_percent: float
    avg_feedback: Optional[float]

class EventPopularity(BaseModel):
    id: int
    title: str
    type: str
    registrations: int
    class Config:
        from_attributes = True
