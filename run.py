from fastapi import FastAPI, HTTPException, Request, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from fastapi.responses import JSONResponse

from database import *

app = FastAPI()

connected_clients = []


class LoginRequest(BaseModel):
    id: str
    password: str


class LoginResponse(BaseModel):
    role: str
    data: dict = {}
    error: dict = {}


class CourseRequest(BaseModel):
    course_id: str


class CourseResponse(BaseModel):
    course_id: str
    course_type: str
    name: str
    department_name: str
    credit: int
    sections: list


class PersonRequest(BaseModel):
    id: str


@app.post('/login', response_model=LoginResponse)
async def login(credentials: LoginRequest):
    print(credentials.id, credentials.password)
    role_data = await check_user_credentials(credentials.id, credentials.password)

    if not role_data:
        raise HTTPException(
            status_code=401,
            detail="Invalid ID or password"
        )

    if isinstance(role_data, dict) and 'role' in role_data:
        return {
            "role": role_data['role'],
            "data": {k: v for k, v in role_data.items() if k != 'role'},
            "error": {}
        }

    raise HTTPException(
        status_code=500,
        detail="Unexpected error occurred"
    )


@app.post('/course')
async def get_course_details(course_request: CourseRequest):
    course_data = await fetch_course_data(course_request.course_id)

    if not course_data:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    return course_data


@app.post('/person')
async def get_person_details(person_request: PersonRequest):
    person_data = await fetch_person_data(person_request.id)

    if not person_data:
        raise HTTPException(
            status_code=404,
            detail="Person not found"
        )

    return person_data


# --------------------------------------------------------------------------------------------------
@app.websocket("/ws/notifications")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        connected_clients.remove(websocket)


@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "accepted": False,
            "error": exc.detail if isinstance(exc.detail, dict) else {
                "code": 1001,
                "message": str(exc.detail)
            }
        }
    )
