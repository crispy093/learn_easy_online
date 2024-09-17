from models import User, ReturnableUser
import bcrypt
import os
import json

# This is a stand-in for a users table in a database
USERS_FILE_NAME = "users.json"

async def create_and_save_user(user: User) -> ReturnableUser or None:
    # Check if user exists
    if await get_user_by_name(user.name):
        # Raise an exception if user already exists
        return None

    user.password = await encrypt_password(user.password)
    try:
        await save_user_to_local_json(user)
        return ReturnableUser(**user.model_dump())
    except Exception as e:
        print(f"Failed to save user to local json file: {e}")
        return None


async def get_user_by_name(name: str):
    if os.path.exists(USERS_FILE_NAME):
        with open(USERS_FILE_NAME, "r") as file:
            users_json = json.load(file)
    else:
        return None

    for user_json in users_json:
        user = User.model_validate_json(user_json)
        if user.name == name:
            return ReturnableUser(**user.model_dump())

    return None


async def encrypt_password(password: str):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


async def save_user_to_local_json(user: User):
    if os.path.exists(USERS_FILE_NAME):
        with open(USERS_FILE_NAME, "r") as file:
            users = json.load(file)
    else:
        users = []

    users.append(user.model_dump_json())

    with open(USERS_FILE_NAME, "w") as file:
        json.dump(users, file)
