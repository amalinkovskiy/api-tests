from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import json
import uuid
from typing import List, Optional

app = FastAPI()

DB_FILE = "users.json"

# Ensure JSON storage exists
def load_users():
    try:
        with open(DB_FILE, "r") as f:
            data = json.load(f)
            if isinstance(data, dict):
                return []
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_users(users):
    with open(DB_FILE, "w") as f:
        json.dump(users, f, indent=4)

# Pydantic model for User
class User(BaseModel):
    name: str
    age: int
    profession: str
    salary: float
    uuid: Optional[str] = None

class UserResponse(User):
    uuid: str

@app.post("/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: User):
    users = load_users()
    user_id = str(uuid.uuid4())
    user_data = user.dict()
    user_data["uuid"] = user_id
    users.append(user_data)
    save_users(users)
    return user_data

@app.get("/users/", response_model=List[UserResponse])
def get_all_users():
    users = load_users()
    return users

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: str):
    users = load_users()
    for user in users:
        if user["uuid"] == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: str, user: User):
    users = load_users()
    for i, existing_user in enumerate(users):
        if existing_user["uuid"] == user_id:
            user_data = user.dict()
            user_data["uuid"] = user_id
            users[i] = user_data
            save_users(users)
            return user_data
    raise HTTPException(status_code=404, detail="User not found")

@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: str):
    users = load_users()
    for i, user in enumerate(users):
        if user["uuid"] == user_id:
            del users[i]
            save_users(users)
            return {"message": "User deleted successfully"}
    raise HTTPException(status_code=404, detail="User not found")