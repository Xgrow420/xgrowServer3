from typing import List

from fastapi import WebSocket, WebSocketDisconnect, APIRouter, Depends
from fastapi.responses import HTMLResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from sqlalchemy.orm import Session

from app.schemas import schemas
from app.data import database
from app.schemas.schemas import Settings
from app.utils.currentUserUtils import userUtils
import app.utils.stringUtils as stringUtils
from app.websocket.repository.commandManager import getCommandManager

from app.websocket.repository.connectionManagerXgrow import getConnectionManagerXgrow
from app.websocket.repository.connectionManagerFrontend import getConnectionManagerFrontend

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
async def webSocketXgrow(websocket: WebSocket, csrf_token: str = "", client_id: str = "empty",
                              Authorize: AuthJWT = Depends(), db: Session = Depends(dataBase)):
    await websocket.accept()
    try:
        Authorize.jwt_required("websocket", websocket=websocket, csrf_token=csrf_token)
        uName = Authorize.get_jwt_subject()
        user: schemas.User = await stringUtils.getUserSchemaFromName(uName, db)
        xgrowKey: str = await userUtils.asyncGetXgrowKeyForCurrentUser(user)
        userName = await userUtils.asyncGetUserNameForCurrentUser(user)
        connection = await getConnectionManagerXgrow().connect(websocket=websocket, xgrowKey=xgrowKey)

        print(uName, user.name, userName, xgrowKey)

        try:
            while True:
                command = await websocket.receive_text()
                await getCommandManager().sendCommandToFrontend(command=command, xgrowKey=xgrowKey, userName=userName)

        except WebSocketDisconnect:
            await getConnectionManagerXgrow().disconnect(xgrowKey)
            #await websocket.close() #<<=== niepotrzebne
            # await manager.broadcast(f"Client #{Authorize.get_jwt_subject()} left the chat")
    except AuthJWTException:
        await websocket.send_text("[Server] webSocket login failed...")
        await websocket.close()




'''
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
                await getConnectionManager().send_personal_message(f"You wrote: {command}", websocket)
                await getConnectionManager().send_personal_message(f"Client {xgrowKey}", websocket)
'''
