from datetime import datetime, timedelta
from app.models import FitnessClass
from pytz import timezone

local_tz = timezone("Asia/Kolkata")

def get_sample_classes():
    now = datetime.now(local_tz)
    tomorrow = now + timedelta(days=1)

    return [
        FitnessClass(
            id="1",
            name="Morning Yoga",
            description="Gentle stretches to start your day",
            instructor="Priya Sharma",
            start_time=tomorrow.replace(hour=7, minute=0),
            duration_minutes=60,
            total_slots=15,
            available_slots=15,
            bookings=[]
        ),
        FitnessClass(
            id="2",
            name="Power Zumba",
            description="High-energy dance workout",
            instructor="Rahul Mehta",
            start_time=tomorrow.replace(hour=18, minute=30),
            duration_minutes=45,
            total_slots=20,
            available_slots=20,
            bookings=[]
        ),
        FitnessClass(
            id="3",
            name="HIIT Blast",
            description="High-intensity interval training",
            instructor="Anjali Kapoor",
            start_time=tomorrow.replace(hour=18, minute=30),
            duration_minutes=45,
            total_slots=20,
            available_slots=20,
            bookings=[]
        )
    ]
