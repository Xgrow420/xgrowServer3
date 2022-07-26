from typing import List

from fastapi import WebSocket, WebSocketDisconnect, APIRouter, Depends
from fastapi.responses import HTMLResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from sqlalchemy.orm import Session

from app.schemas import schemas, schemasPot
from app.data import database
from app.schemas.schemas import Settings
from app.utils.currentUserUtils import userUtils
import app.utils.stringUtils as stringUtils

from app.restApi.repository import pot

router = APIRouter(
    prefix="/webSocketConnection",
    tags=['WebSocket Connection']
)

dataBase = database.getDataBase

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            const getCookie = (name) => {
                const value = `; ${document.cookie}`;
                const parts = value.split(`; ${name}=`);
                if (parts.length === 2) return parts.pop().split(';').shift();
            }
        
            var client_id = Date.now()
            document.querySelector("#ws-id").textContent = client_id;
            let csrf_token = getCookie("csrf_access_token")
            
            var ws = new WebSocket(`ws://xgrow.pl/webSocketConnection/?csrf_token=${csrf_token}&client_id=${client_id}`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""

#ws://127.0.0.1:8000/webSocketConnection/?csrf_token=${csrf_token}&client_id=${client_id}

class Connection:
    def __init__(self, websocket: WebSocket, xgrowKey=None):
        self._webSocket: WebSocket = websocket
        self._xgrowKey: str = xgrowKey

    def getWebSocket(self):
        return self._webSocket

    def setWebSocket(self, websocket: WebSocket):
        self._webSocket = websocket

    def getXgrowKey(self):
        return self._xgrowKey

    def setXgrowKey(self, xgrowKey: str):
        self._xgrowKey = xgrowKey

    def getConnectionByWebSocket(self, websocket: WebSocket):
        if websocket == self._webSocket:
            return websocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[Connection] = []

    async def connect(self, websocket: WebSocket, xgrowKey: str):
        connection = Connection(websocket=websocket, xgrowKey=xgrowKey)
        self.active_connections.append(connection)
        return connection

    def disconnect(self, websocket: WebSocket):
        for connection in self.active_connections:
            if connection.getConnectionByWebSocket(websocket):
                print(f"{connection.getXgrowKey()} disconnected")
                self.active_connections.remove(connection)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def sendMessageToDevice(self, message: str, xgrowKey: str):
        for connection in self.active_connections:
            if connection.getXgrowKey() == xgrowKey:
                await connection.getWebSocket().send_text(message)
    # TODO: add if statment connection not found info

@AuthJWT.load_config
def get_config():
    return Settings()

manager = ConnectionManager()


def getConnectionManager():
    return manager


@router.get("/")
async def get():
    return HTMLResponse(html)


@router.websocket("/")
async def web_socket_endpoint(websocket: WebSocket, csrf_token: str = "", client_id: str = "empty",
                              Authorize: AuthJWT = Depends(), db: Session = Depends(dataBase)):
    await websocket.accept()
    try:
        Authorize.jwt_required("websocket", websocket=websocket, csrf_token=csrf_token)
        userName = Authorize.get_jwt_subject()
        user: schemas.User = await stringUtils.getUserSchemaFromName(userName, db)
        xgrowKey: str = await userUtils.asyncGetXgrowKeyForCurrentUser(user)
        connection = await manager.connect(websocket=websocket, xgrowKey=xgrowKey)

        try:
            while True:
                data = await websocket.receive_text()

                # FIXME: test loop
                await manager.sendMessageToDevice(f"Connected user:{userName}, xkey: {connection.getXgrowKey()}", xgrowKey)

                await manager.send_personal_message(f"", websocket)
                await manager.send_personal_message(f"You wrote: {data}", websocket)
                await manager.send_personal_message(f"Client {xgrowKey}", websocket)
        except WebSocketDisconnect:
            manager.disconnect(websocket)
            # await manager.broadcast(f"Client #{Authorize.get_jwt_subject()} left the chat")
    except AuthJWTException:
        await websocket.send_text("login failed...")
        await websocket.close()
