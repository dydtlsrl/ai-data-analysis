from fastapi import FastAPI

app = FastAPI()

members = [
    {"id": 1, "name": "Kim", "email": "kim@example.com"},
    {"id": 2, "name": "Lee", "email": "lee@example.com"},
]

@app.get("/")
def read_root():
    return {"message": "Hello FastAPI"}

@app.get("/members")
def read_members():
    return members