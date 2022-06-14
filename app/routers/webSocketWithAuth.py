from typing import List

from fastapi import FastAPI, WebSocket, Depends, Query, APIRouter
from fastapi.responses import HTMLResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from pydantic import BaseModel

router = APIRouter(
    prefix="/webSocketAuth",
    tags=['WebSocket Auth']
)

class Settingss(BaseModel):
    authjwt_secret_key: str = "secret"
    authjwt_token_location: set = {"cookies"}

@AuthJWT.load_config
def get_config():
    return Settingss()


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Authorize</title>
    </head>
    <body>
        <h1>WebSocket Authorize</h1>
        <button onclick="websocketfun()">Send</button>
        <ul id='messages'>
        </ul>
        <script>
            const getCookie = (name) => {
                const value = `; ${document.cookie}`;
                const parts = value.split(`; ${name}=`);
                if (parts.length === 2) return parts.pop().split(';').shift();
            }

            const websocketfun = () => {
                let csrf_token = getCookie("csrf_access_token")

                let ws = new WebSocket(`ws://127.0.0.1:8000/webSocketAuth/ws?csrf_token=${csrf_token}`)
                ws.onmessage = (event) => {
                    let messages = document.getElementById('messages')
                    let message = document.createElement('li')
                    let content = document.createTextNode(event.data)
                    message.appendChild(content)
                    messages.appendChild(message)
                }
            }
        </script>
    </body>
</html>
"""


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()



@router.get("/")
async def get():
    return HTMLResponse(html)

@router.websocket('/ws')
async def websocket(websocket: WebSocket, csrf_token: str = Query(...), Authorize: AuthJWT = Depends()):
    await manager.connect(websocket)
    print("run")
    try:
        Authorize.jwt_required("websocket",websocket=websocket,csrf_token=csrf_token)
        # Authorize.jwt_optional("websocket",websocket=websocket,csrf_token=csrf_token)
        # Authorize.jwt_refresh_token_required("websocket",websocket=websocket,csrf_token=csrf_token)
        # Authorize.fresh_jwt_required("websocket",websocket=websocket,csrf_token=csrf_token)
        await websocket.send_text("Successfully Login!")
        decoded_token = Authorize.get_raw_jwt()
        await websocket.send_text(f"Here your decoded token: {decoded_token}")
    except AuthJWTException as err:
        await websocket.send_text(f"not auth: {err}")
        await websocket.close()

