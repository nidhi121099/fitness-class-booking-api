# # Core business logic for fitness class operations
# from datetime import datetime, timedelta
# from typing import List
# from pytz import timezone

# from app import schemas
# from app.models import FitnessClass, Booking, Database
# from app.errors import ClassNotFoundError, NoSlotsAvailableError, DuplicateBookingError

# # Use India timezone for all datetime operations
# local_tz = timezone('Asia/Kolkata')

# def get_upcoming_classes(db: Database) -> List[schemas.FitnessClassResponse]:
#     """Filters and returns future classes in chronological order"""
#     current_time = datetime.now(local_tz)
#     upcoming = []
    
#     for class_id, cls in db.classes.items():
#         if cls.start_time >= current_time:
#             upcoming.append(schemas.FitnessClassResponse(
#                 id=class_id,
#                 name=cls.name,
#                 description=cls.description,
#                 instructor=cls.instructor,
#                 start_time=cls.start_time,
#                 duration_minutes=cls.duration_minutes,
#                 total_slots=cls.total_slots,
#                 available_slots=cls.available_slots
#             ))
    
#     return sorted(upcoming, key=lambda c: c.start_time)

# def create_booking(db: Database, request: schemas.BookingRequest) -> schemas.BookingResponse:
#     """Handles the booking creation process with validation"""
#     # First verify the class exists
#     if request.class_id not in db.classes:
#         raise ClassNotFoundError()
    
#     cls = db.classes[request.class_id]
    
#     # Check for duplicate bookings
#     if request.client_email in db.email_to_booking_ids:
#         for booking_id in db.email_to_booking_ids[request.client_email]:
#             if db.bookings[booking_id].class_id == request.class_id:
#                 raise DuplicateBookingError()
    
#     # Verify availability
#     if cls.available_slots < 1:
#         raise NoSlotsAvailableError()
    
#     # Create the new booking
#     new_id = str(len(db.bookings) + 1)
#     booking_time = datetime.now(local_tz)
    
#     new_booking = Booking(
#         id=new_id,
#         class_id=request.class_id,
#         class_name=cls.name,
#         client_name=request.client_name,
#         client_email=request.client_email,
#         booking_time=booking_time
#     )
    
#     # Update all database references
#     db.bookings[new_id] = new_booking
#     cls.bookings.append(new_id)
#     cls.available_slots -= 1
    
#     if request.client_email not in db.email_to_booking_ids:
#         db.email_to_booking_ids[request.client_email] = []
#     db.email_to_booking_ids[request.client_email].append(new_id)
    
#     return schemas.BookingResponse(
#         id=new_id,
#         class_id=new_booking.class_id,
#         class_name=new_booking.class_name,
#         client_name=new_booking.client_name,
#         client_email=new_booking.client_email,
#         booking_time=new_booking.booking_time
#     )

# def get_bookings_by_email(db: Database, email: str) -> List[schemas.BookingResponse]:
#     """Retrieves all bookings for a given email, newest first"""
#     bookings = []
    
#     if email in db.email_to_booking_ids:
#         for booking_id in db.email_to_booking_ids[email]:
#             booking = db.bookings[booking_id]
#             bookings.append(schemas.BookingResponse(
#                 id=booking.id,
#                 class_id=booking.class_id,
#                 class_name=booking.class_name,
#                 client_name=booking.client_name,
#                 client_email=booking.client_email,
#                 booking_time=booking.booking_time
#             ))
    
#     return sorted(bookings, key=lambda b: b.booking_time, reverse=True)

# def initialize_sample_data(db: Database):
#     """Loads example classes into an empty database"""
#     now = datetime.now(local_tz)
#     tomorrow = now + timedelta(days=1)
#     day_after = now + timedelta(days=2)
    
#     sample_classes = [
#         FitnessClass(
#             id="1",
#             name="Morning Yoga",
#             description="Gentle stretches to start your day",
#             instructor="Priya Sharma",
#             start_time=tomorrow.replace(hour=7, minute=0),
#             duration_minutes=60,
#             total_slots=15,
#             available_slots=15,
#             bookings=[]
#         ),
#         FitnessClass(
#             id="2",
#             name="Power Zumba",
#             description="High-energy dance workout",
#             instructor="Rahul Mehta",
#             start_time=tomorrow.replace(hour=18, minute=30),
#             duration_minutes=45,
#             total_slots=20,
#             available_slots=20,
#             bookings=[]
#         ),
#         FitnessClass(
#             id="3",
#             name="HIIT Blast",
#             description= "High-intensity interval training",
#             instructor= "Anjali Kapoor",
#             start_time=tomorrow.replace(hour=18, minute=30),
#             duration_minutes=45,
#             total_slots=20,
#             available_slots=20,
#             bookings=[]
#         )
#     ]
    
#     for cls in sample_classes:
#         db.classes[cls.id] = cls

# app/services.py

from datetime import datetime
from typing import List
from pytz import timezone

from app import schemas
from app.models import FitnessClass, Booking, Database
from app.errors import ClassNotFoundError, NoSlotsAvailableError, DuplicateBookingError
from app.sample_data import get_sample_classes  
# Use India timezone for all datetime operations
local_tz = timezone('Asia/Kolkata')


def get_upcoming_classes(db: Database) -> List[schemas.FitnessClassResponse]:
    """Filters and returns future classes in chronological order"""
    current_time = datetime.now(local_tz)
    upcoming = []

    for class_id, cls in db.classes.items():
        if cls.start_time >= current_time:
            upcoming.append(schemas.FitnessClassResponse(
                id=class_id,
                name=cls.name,
                description=cls.description,
                instructor=cls.instructor,
                start_time=cls.start_time,
                duration_minutes=cls.duration_minutes,
                total_slots=cls.total_slots,
                available_slots=cls.available_slots
            ))

    return sorted(upcoming, key=lambda c: c.start_time)


def create_booking(db: Database, request: schemas.BookingRequest) -> schemas.BookingResponse:
    """Handles the booking creation process with validation"""
    if request.class_id not in db.classes:
        raise ClassNotFoundError()

    cls = db.classes[request.class_id]

    # Check for duplicate bookings
    if request.client_email in db.email_to_booking_ids:
        for booking_id in db.email_to_booking_ids[request.client_email]:
            if db.bookings[booking_id].class_id == request.class_id:
                raise DuplicateBookingError()

    if cls.available_slots < 1:
        raise NoSlotsAvailableError()

    new_id = str(len(db.bookings) + 1)
    booking_time = datetime.now(local_tz)

    new_booking = Booking(
        id=new_id,
        class_id=request.class_id,
        class_name=cls.name,
        client_name=request.client_name,
        client_email=request.client_email,
        booking_time=booking_time
    )

    db.bookings[new_id] = new_booking
    cls.bookings.append(new_id)
    cls.available_slots -= 1

    if request.client_email not in db.email_to_booking_ids:
        db.email_to_booking_ids[request.client_email] = []

    db.email_to_booking_ids[request.client_email].append(new_id)

    return schemas.BookingResponse(
        id=new_id,
        class_id=new_booking.class_id,
        class_name=new_booking.class_name,
        client_name=new_booking.client_name,
        client_email=new_booking.client_email,
        booking_time=new_booking.booking_time
    )


def get_bookings_by_email(db: Database, email: str) -> List[schemas.BookingResponse]:
    """Retrieves all bookings for a given email, newest first"""
    bookings = []

    if email in db.email_to_booking_ids:
        for booking_id in db.email_to_booking_ids[email]:
            booking = db.bookings[booking_id]
            bookings.append(schemas.BookingResponse(
                id=booking.id,
                class_id=booking.class_id,
                class_name=booking.class_name,
                client_name=booking.client_name,
                client_email=booking.client_email,
                booking_time=booking.booking_time
            ))

    return sorted(bookings, key=lambda b: b.booking_time, reverse=True)


def initialize_sample_data(db: Database):
    """Loads example classes into an empty database from external sample_data.py"""
    for cls in get_sample_classes(): 
        db.classes[cls.id] = cls
