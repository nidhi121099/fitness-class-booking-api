from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List
import uuid

@dataclass
class FitnessClass:
    id: str
    name: str
    description: str
    instructor: str
    start_time: datetime
    duration_minutes: int
    total_slots: int
    available_slots: int
    bookings: List[str]  # List of booking IDs

@dataclass
class Booking:
    id: str
    class_id: str
    class_name: str
    client_name: str
    client_email: str
    booking_time: datetime

class Database:
    def __init__(self):
        self.classes: Dict[str, FitnessClass] = {}
        self.bookings: Dict[str, Booking] = {}
        self.email_to_booking_ids: Dict[str, List[str]] = {}