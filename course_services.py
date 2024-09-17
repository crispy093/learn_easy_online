import json
import os

from models import Course

# This is a stand-in for a courses table in a database
COURSES_FILE_NAME = "courses.json"

async def create_and_save_course(course: Course) -> Course or None:
    try:
        # Check if course exists
        if await get_course_by_title(course.title):
            # Raise an exception if course already exists
            return None

        # Validate advanced course has price
        if course.is_advanced and not course.price:
            return None
        await save_course_to_local_json(course)
        return course
    except Exception as e:
        print(f"Failed to save course to local json file: {e}")
        return None


async def list_all_courses() -> list[Course]:
    if os.path.exists(COURSES_FILE_NAME):
        with open(COURSES_FILE_NAME, "r") as file:
            courses_json = json.load(file)
    else:
        return []

    courses = []
    for course_json in courses_json:
        course = Course.model_validate_json(course_json)
        courses.append(course)

    return courses

async def get_course_by_title(title: str):
    if os.path.exists(COURSES_FILE_NAME):
        with open(COURSES_FILE_NAME, "r") as file:
            courses_json = json.load(file)
    else:
        return None

    for course_json in courses_json:
        course = Course.model_validate_json(course_json)
        if course.title == title:
            return course

    return None


async def save_course_to_local_json(course: Course):
    if os.path.exists(COURSES_FILE_NAME):
        with open(COURSES_FILE_NAME, "r") as file:
            courses = json.load(file)
    else:
        courses = []

    courses.append(course.model_dump_json())

    with open(COURSES_FILE_NAME, "w") as file:
        json.dump(courses, file)