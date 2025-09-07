import requests
import json

BASE_URL = "http://localhost:8000"

def test_get_colleges():
    response = requests.get(f"{BASE_URL}/colleges")
    print("GET /colleges:", response.status_code, response.json())

def test_create_student_valid():
    data = {"name": "Charlie", "email": "charlie@example.com", "college_id": 1}
    response = requests.post(f"{BASE_URL}/students", json=data)
    try:
        print("POST /students (valid):", response.status_code, response.json())
    except:
        print("POST /students (valid):", response.status_code, response.text)

def test_create_student_invalid():
    # Missing name
    data = {"email": "charlie@example.com", "college_id": 1}
    response = requests.post(f"{BASE_URL}/students", json=data)
    try:
        print("POST /students (missing name):", response.status_code, response.json())
    except:
        print("POST /students (missing name):", response.status_code, response.text)

    # Invalid email
    data = {"name": "Charlie", "email": "invalid", "college_id": 1}
    response = requests.post(f"{BASE_URL}/students", json=data)
    try:
        print("POST /students (invalid email):", response.status_code, response.json())
    except:
        print("POST /students (invalid email):", response.status_code, response.text)

    # Invalid college_id
    data = {"name": "Charlie", "email": "charlie@example.com", "college_id": 999}
    response = requests.post(f"{BASE_URL}/students", json=data)
    try:
        print("POST /students (invalid college_id):", response.status_code, response.json())
    except:
        print("POST /students (invalid college_id):", response.status_code, response.text)

def test_get_students():
    response = requests.get(f"{BASE_URL}/students")
    print("GET /students:", response.status_code, len(response.json()), "students")

def test_create_event():
    import datetime
    now = datetime.datetime.utcnow()
    data = {
        "title": "Test Event",
        "description": "Test description",
        "type": "Workshop",
        "start_time": (now + datetime.timedelta(days=1)).isoformat(),
        "end_time": (now + datetime.timedelta(days=1, hours=2)).isoformat(),
        "college_id": 1
    }
    response = requests.post(f"{BASE_URL}/events", json=data)
    print("POST /events:", response.status_code, response.json())
    return response.json()["id"] if response.status_code == 200 else None

def test_get_events():
    response = requests.get(f"{BASE_URL}/events")
    print("GET /events:", response.status_code, len(response.json()), "events")

def test_register():
    data = {"student_id": 1, "event_id": 1}
    response = requests.post(f"{BASE_URL}/register", json=data)
    print("POST /register:", response.status_code, response.json())

def test_attendance():
    data = {"student_id": 1, "event_id": 1}
    response = requests.post(f"{BASE_URL}/attendance", json=data)
    print("POST /attendance:", response.status_code, response.json())

def test_feedback():
    data = {"student_id": 1, "event_id": 1, "rating": 5, "comment": "Great event!"}
    response = requests.post(f"{BASE_URL}/feedback", json=data)
    print("POST /feedback:", response.status_code, response.json())

def test_reports():
    response = requests.get(f"{BASE_URL}/reports/event-popularity")
    print("GET /reports/event-popularity:", response.status_code, len(response.json()), "results")

    response = requests.get(f"{BASE_URL}/reports/student-participation/1")
    print("GET /reports/student-participation/1:", response.status_code, response.json())

    response = requests.get(f"{BASE_URL}/reports/top-active")
    print("GET /reports/top-active:", response.status_code, len(response.json()), "results")

    response = requests.get(f"{BASE_URL}/reports/event-stats/1")
    print("GET /reports/event-stats/1:", response.status_code, response.json())

if __name__ == "__main__":
    print("Starting backend tests...")
    test_get_colleges()
    test_create_student_valid()
    test_create_student_invalid()
    test_get_students()
    event_id = test_create_event()
    test_get_events()
    test_register()
    test_attendance()
    test_feedback()
    test_reports()
    print("Backend tests completed.")
