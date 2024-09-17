from typing import Optional

from fastapi import HTTPException

from fastapi import FastAPI


from course_services import list_all_courses, create_and_save_course, get_course_by_title
from models import User, ReturnableUser, Course
from user_services import create_and_save_user, get_user_by_name

app = FastAPI()

@app.post("/api/users/create_user")
async def create_user(name: str, password: str, phone_number: str, age: str) -> ReturnableUser or dict:
    # Sanitize and validate user input
    user = User(
        name=name,
        password=password,
        phone_number=phone_number,
        age=age
    )

    # Create user in database
    user = await create_and_save_user(user)

    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="User already exists")


@app.get("/api/users/get_user")
async def get_user(name: str) -> ReturnableUser or dict:
    user = await get_user_by_name(name=name)

    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")


@app.post("/api/courses/create_course")
async def create_course(title: str, description: str, is_advanced: bool, price: Optional[float] = None) -> Course:
    course = Course(
        title=title,
        description=description,
        is_advanced=is_advanced,
        price=price
    )

    course = await create_and_save_course(course)

    if course:
        return course
    else:
        raise HTTPException(status_code=404, detail="Course already exists")


@app.get("/api/courses/get_course")
async def get_course(title: str) -> Course:
    course = await get_course_by_title(title=title)

    if course:
        return course
    else:
        raise HTTPException(status_code=404, detail="Course not found")


@app.get("/api/courses/list")
async def list_courses() -> list[Course]:
    return await list_all_courses()