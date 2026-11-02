
from fastapi import FastAPI, HTTPException

app = FastAPI()

members = [
    {"id": 1, "name": "Kim", "email": "kim@example.com", "age": 25},
    {"id": 2, "name": "Lee", "email": "lee@example.com", "age": 19},
    {"id": 3, "name": "Park", "email": "park@example.com", "age": 31},
]


@app.get("/members")
def get_members():
    return members


@app.get("/members/{member_id}")
def get_member(member_id: int):
    for member in members:
        if member["id"] == member_id:
            return member

    raise HTTPException(
        status_code=404,
        detail="Member not found"
        )


@app.get("/members/search/")
def search_members(name: str | None = None):

    if name is None:
        return members
    keyword = name.lower()
    return [
        member
        for member in members
        if keyword in member["name"].lower()
    ]



@app.get("/members/filter/")
def filter_members(
    name: str | None = None,
    min_age: int | None = None,
):
    result = members

    if name is not None:
        keyword = name.lower()
        result = [
            member
            for member in result
            if keyword in member["name"].lower()
        ]

    if min_age is not None:
        result = [
            member
            for member in result
            if member["age"] >= min_age
        ]

    return result
