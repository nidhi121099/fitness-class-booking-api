from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from app.main import app
from app.database import get_db, Database
from app import services

client = TestClient(app)

def setup_module():
    db = get_db()
    db.classes.clear()
    db.bookings.clear()
    db.email_to_booking_ids.clear()
    services.initialize_sample_data(db)

def test_get_classes():
    response = client.get("/classes")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

def test_successful_booking():
    response = client.post("/book", json={
        "class_id": "1",
        "client_name": "Test User",
        "client_email": "test@example.com"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["class_name"] == "Morning Yoga"
    assert data["client_email"] == "test@example.com"

def test_duplicate_booking():
    # Book same class again with same email
    response = client.post("/book", json={
        "class_id": "1",
        "client_name": "Test User",
        "client_email": "test@example.com"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Already booked this class"

def test_class_not_found():
    response = client.post("/book", json={
        "class_id": "999",
        "client_name": "Ghost",
        "client_email": "ghost@example.com"
    })
    assert response.status_code == 404
    assert response.json()["detail"] == "Class doesn't exist"

def test_no_slots_available():
    db = get_db()
    # Make class 2 full
    class2 = db.classes["2"]
    class2.available_slots = 0
    response = client.post("/book", json={
        "class_id": "2",
        "client_name": "Overflow User",
        "client_email": "overflow@example.com"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "No slots left"

def test_get_bookings_success():
    response = client.get("/bookings", params={"email": "test@example.com"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["client_email"] == "test@example.com"

def test_get_bookings_none():
    response = client.get("/bookings", params={"email": "noone@example.com"})
    assert response.status_code == 200
    assert response.json() == []

def test_upcoming_classes_filtering():
    db = get_db()
    # Add past class
    past_id = "999"
    db.classes[past_id] = services.FitnessClass(
        id=past_id,
        name="Old Class",
        description="Past session",
        instructor="Expired",
        start_time=datetime.now(services.local_tz) - timedelta(days=1),
        duration_minutes=60,
        total_slots=10,
        available_slots=10,
        bookings=[]
    )
    response = client.get("/classes")
    assert response.status_code == 200
    classes = response.json()
    ids = [cls["id"] for cls in classes]
    assert past_id not in ids
