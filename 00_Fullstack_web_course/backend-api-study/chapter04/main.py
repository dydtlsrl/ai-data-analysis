from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()


class MemberCreate(BaseModel):
    name: str
    email: str
    age: int


class MemberResponse(BaseModel):
    id: int
    name: str
    email: str
    age: int


members = [
    {
        "id": 1,
        "name": "Kim",
        "email": "kim@example.com",
        "age": 25,
    },
    {
        "id": 2,
        "name": "Lee",
        "email": "lee@example.com",
        "age": 31,
    },
]


@app.get(
    "/members",
    response_model=list[MemberResponse],
    status_code=status.HTTP_200_OK,
)
def get_members():
    return members

@app.get(
    "/members/{member_id}",
    response_model=MemberResponse,
    status_code=status.HTTP_200_OK,
)


def get_member(member_id: int):
    for member in members:
        if member["id"] == member_id:
            return member

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Member not found",
    )


@app.post(
    "/members",
    response_model=MemberResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_member(member: MemberCreate):
    new_member = {
        "id": len(members) + 1,
        "name": member.name,
        "email": member.email,
        "age": member.age,
    }

    members.append(new_member)
    return new_member