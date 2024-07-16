# app/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import redis

app = FastAPI()

# Connect to Redis
redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)

class ContactCreate(BaseModel):
    name: str
    email: str
    message: str

@app.post("/contacts/")
def create_contact(contact: ContactCreate):
    # Use email as the key
    redis_client.hset(contact.email, mapping={
        "name": contact.name,
        "message": contact.message
    })
    return {"message": "Contact saved successfully"}

@app.get("/contacts/{email}")
def get_contact(email: str):
    contact = redis_client.hgetall(email)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

@app.get("/")
def read_root():
    return {"message": "Welcome to the contact form API with Redis"}
