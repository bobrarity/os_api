from fastapi import FastAPI, HTTPException, Request, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from fastapi.responses import JSONResponse

from database import *

# uvicorn run:app --reload
app = FastAPI()

users_db = {
    # student_id below
    "admin": {"password": "123"}
}

valid_device_tokens = ["device1", "device2"]
valid_nfc_tags = ["tag1", "tag2"]

connected_clients = []


class LoginRequest(BaseModel):
    id: str
    password: str


class LoginResponse(BaseModel):
    role: str
    error: dict = {}


class SuccessResponse(BaseModel):
    data: dict
    error: dict = {}


class ErrorResponse(BaseModel):
    error: dict


class NFCRequest(BaseModel):
    device_token: str
    nfc_tag: str


class NFCResponse(BaseModel):
    accepted: bool
    error: dict


@app.post('/login', response_model=LoginResponse)
async def login(credentials: LoginRequest):
    print(credentials.id, credentials.password)
    role = await check_user_credentials(credentials.id, credentials.password)

    if not role:
        raise HTTPException(
            status_code=401,
            detail="Invalid ID or password"
        )

    return {"role": role, "error": {}}


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
