from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import logging
from app import schemas, services, errors
from app.database import get_db, Database

# init logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger("main")

app = FastAPI()

# CORS - allow all origins for now
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/classes", response_model=List[schemas.FitnessClassResponse])
async def all_classes(db: Database = Depends(get_db)):
    # fetch classes from db
    try:
        return services.get_upcoming_classes(db)
    except Exception as err:
        log.error("Err in get_upcoming_classes: %s", err)
        raise HTTPException(500, detail="error loading classes")

@app.post("/book", response_model=schemas.BookingResponse)
async def book_it(payload: schemas.BookingRequest, db: Database = Depends(get_db)):
    # make a booking
    try:
        result = services.create_booking(db, payload)
        return result
    except errors.ClassNotFoundError:
        raise HTTPException(404, detail="Class doesn't exist")
    except errors.NoSlotsAvailableError:
        raise HTTPException(400, detail="No slots left")
    except errors.DuplicateBookingError:
        raise HTTPException(400, detail="Already booked this class")
    except Exception as e:
        print("Unhandled error:", e)
        raise HTTPException(500, detail="Something broke")

@app.get("/bookings", response_model=List[schemas.BookingResponse])
async def get_my_bookings(email: str = Query(..., regex=r"^[^@]+@[^@]+\.[^@]+$"), db: Database = Depends(get_db)):
    try:
        data = services.get_bookings_by_email(db, email)
        return data
    except Exception as e:
        log.warning(f"booking fetch failed for {email}: {e}")
        raise HTTPException(500, detail="Could not fetch bookings")

@app.on_event("startup")
async def on_start():
    try:
        db = get_db()
        services.initialize_sample_data(db)
        log.info("sample data ok")
    except Exception as e:
        log.error("Init failed: %s", e)
