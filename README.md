# Fitness Class Booking API


This is a simple FastAPI backend I built for managing bookings in a fictional fitness studio. It handles Yoga, Zumba, and HIIT sessions — just like a real booking system, but with in-memory data and no external database.

---

## 🔍 What It Does

- 📅 **See upcoming classes** – Only shows future sessions so you don't accidentally book the past!
- ✅ **Book your spot** – Prevents duplicate bookings and checks for availability before confirming.
- 📧 **Check bookings by email** – Search what you've booked using just your email.
- 🕒 **Timezone-aware** – Everything runs in IST (Indian Standard Time) using `pytz`.
- 🧠 **No DB hassle** – All data is stored in-memory for easy testing and demo.
- 🛡️ **Built-in validation** – Thanks to Pydantic + FastAPI.
- 🧪 **Includes tests** – I wrote some unit tests to make sure the main logic works correctly.

---

## Technology

- Python 3.10
- FastAPI– for building APIs fast
- Pydantic – for validating data
- Uvicorn – to serve the API
- pytz – for timezone handling


## Prerequisites

Make sure you have Python 3.10 or above installed on your machine.

--> Installation

1. Clone the repository : gh repo clone nidhi121099/fitness-class-booking-api
2. Create and activate a virtual environment (optional but recommended):
    python -m venv venv
    source venv/bin/activate   # On Windows use: venv\Scripts\activate
3. Install the dependencies:
    pip install -r requirements.txt
4. Running the Server:
    uvicorn app.main:app --reload
The API will be accessible at: http://127.0.0.1:8000
Interactive API docs (Swagger UI) are available at: http://127.0.0.1:8000/docs

## Postman Collection

You can test all endpoints using Postman.

🗂️ File: fitness-api.postman_collection.json

It includes:

GET /classes – view upcoming classes

POST /book – book a class

GET /bookings?email=abc@xyz.com – check bookings by email

- Sample Data

Use the included `fitness-api.postman_collection.json` to create sample classes and bookings.


## Testing
Unit tests are included to verify the key features of the API.
- To run tests:
    pytest
Make sure you have pytest installed (pip install pytest) before running tests.


## Contact
Feel free to reach out if you want to connect or have suggestions!

Email: nidhijp31@gmail.com

Thank you for checking out this project! 
