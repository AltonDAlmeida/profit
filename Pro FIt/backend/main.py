from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
from datetime import datetime
import mysql.connector
from pydantic import BaseModel, EmailStr
import bcrypt
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")

# Mount static files if needed (skip this if not using them)
# app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# HTML routes
@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/progress", response_class=HTMLResponse)
async def progress(request: Request):
    return templates.TemplateResponse("progress.html", {"request": request})

@app.get("/schedule", response_class=HTMLResponse)
async def schedule(request: Request):
    return templates.TemplateResponse("schedule.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def log(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/signup", response_class=HTMLResponse)
async def log(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

# ✅ Fix: Add backend API endpoints
@app.get("/api/progress")
async def get_progress():
    dummy_data = {
        "steps_completed": 8,
        "total_steps": 10,
        "percentage": 80
    }
    return JSONResponse(content=dummy_data)

@app.get("/api/schedule")
async def get_schedule():
    dummy_data = {
        "day": "Wednesday",
        "workout": "Legs and Core",
        "duration": "45 mins"
    }
    return JSONResponse(content=dummy_data)


@app.post("/add-schedule")
async def add_schedule(request: Request):
    data = await request.json()

    # Extract data from the request
    day = data.get("day")
    workout = data.get("workout")
    duration = data.get("duration")
    notes = data.get("notes")

    # Validate the data
    if not day or not workout or not duration:
        raise HTTPException(status_code=400, detail="All fields are required")

    # Insert the data into your MySQL database (example code)
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        cursor = connection.cursor()
        query = "INSERT INTO schedule (day, workout, duration, notes) VALUES (%s, %s, %s, %s)"
        values = (day, workout, duration, notes)
        cursor.execute(query, values)
        connection.commit()

        cursor.close()
        connection.close()

        return JSONResponse(content={"message": "Workout added successfully"})

    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"An error occurred: {str(e)}")
    
class SignupRequest(BaseModel):
    name: str
    email: EmailStr
    password: str

@app.post("/signup")
async def signup(request: SignupRequest):
    name = request.name
    email = request.email
    password = request.password

    # Hash the password and decode it to a UTF-8 string
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    try:
        # Connect to the MySQL database
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        cursor = connection.cursor()

        # Check if the email already exists
        cursor.execute("SELECT email FROM users WHERE email = %s", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered.")

        # Insert new user into the database
        query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
        values = (name, email, hashed_password)
        cursor.execute(query, values)
        connection.commit()

        # Close connection
        cursor.close()
        connection.close()

        return JSONResponse(content={"message": "User registered successfully!"})

    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error occurred: {str(err)}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))    


class LoginRequest(BaseModel):
    email: EmailStr
    password: str

@app.post("/login")
async def login(request: LoginRequest):
    email = request.email
    password = request.password

    try:
        # Connect to the MySQL database
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        cursor = connection.cursor()

        # Check if the email exists
        cursor.execute("SELECT email, password FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user is None:
            raise HTTPException(status_code=400, detail="Invalid email or password.")

        stored_password = user[1]

        # Check if the password matches
        if not bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
            raise HTTPException(status_code=400, detail="Invalid email or password.")

        # Success - Return success message or token
        return JSONResponse(content={"message": "Login successful!"})

    except mysql.connector.Error as err:
        # Handle any database errors
        print("MySQL Error:", err) 
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.get("/get-schedule")
async def get_schedule():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT day, workout, duration, notes FROM schedule ORDER BY day")
        schedules = cursor.fetchall()

        cursor.close()
        connection.close()

        return schedules

    except mysql.connector.Error:
        raise HTTPException(status_code=500, detail="Database error")