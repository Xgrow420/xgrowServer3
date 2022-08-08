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
from app.websocket.repository.connectionManager import Connection, getConnectionManager

router = APIRouter(
    prefix="/api/webSocketConnection",
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
            
            var ws = new WebSocket(`ws://127.0.0.1:8000/webSocketConnection/?csrf_token=${csrf_token}&client_id=${client_id}`);
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

#ws://xgrow.pl/webSocketConnection/?csrf_token=${csrf_token}&client_id=${client_id}
#ws://127.0.0.1:8000/webSocketConnection/?csrf_token=${csrf_token}&client_id=${client_id}


@AuthJWT.load_config
def get_config():
    return Settings()



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
        connection = await getConnectionManager().connect(websocket=websocket, xgrowKey=xgrowKey)

        try:
            while True:
                data = await websocket.receive_text()

                # FIXME: test loop
                await getConnectionManager().sendMessageToDevice(f"Connected user:{userName}, xkey: {connection.getXgrowKey()}", xgrowKey)

                count = 0
                xklist = []
                for connection in getConnectionManager().active_connections:
                    count = count + 1
                    connection: Connection
                    xklist.append(connection.getXgrowKey())
                    await getConnectionManager().sendMessageToDevice(f"Pobierz Pot{connection.getXgrowKey()}",
                                                                     connection.getXgrowKey())
                await getConnectionManager().sendMessageToDevice(f'chuj {getConnectionManager().active_connections}, count: {count}, xkeyList: {xklist}', connection.getXgrowKey())

                await getConnectionManager().send_personal_message(f"", websocket)
                await getConnectionManager().send_personal_message(f"You wrote: {data}", websocket)
                await getConnectionManager().send_personal_message(f"Client {xgrowKey}", websocket)
        except WebSocketDisconnect:
            getConnectionManager().disconnect(xgrowKey)
            #await websocket.close() #<<=== niepotrzebne
            # await manager.broadcast(f"Client #{Authorize.get_jwt_subject()} left the chat")
    except AuthJWTException:
        await websocket.send_text("login failed...")
        await websocket.close()
