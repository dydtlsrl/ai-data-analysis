from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI()


class MemberCreate(BaseModel):
    name: str
    email: str
    age: int


@app.post("/members", status_code=status.HTTP_201_CREATED)
def create_member(member: MemberCreate):
    return member
