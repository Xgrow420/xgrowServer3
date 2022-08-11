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
from app.websocket.repository.commandManagerFrontend import getCommandManagerFrontend
from app.websocket.repository.connectionManagerFrontend import getConnectionManagerFrontend, ConnectionFrontend

router = APIRouter(
    prefix="/api/webSocketFrontend",
    tags=['WebSocket Frontend Connection']
)

dataBase = database.getDataBase


# ws://xgrow.pl/webSocketConnection/?csrf_token=${csrf_token}&client_id=${client_id}
# ws://127.0.0.1:8000/webSocketConnection/?csrf_token=${csrf_token}&client_id=${client_id}


@AuthJWT.load_config
def get_config():
    return Settings()


@router.websocket("/")
async def web_socket_endpoint(websocket: WebSocket, csrf_token: str = "", client_id: str = "empty",
                              Authorize: AuthJWT = Depends(), db: Session = Depends(dataBase)):
    await websocket.accept()
    try:
        Authorize.jwt_required("websocket", websocket=websocket, csrf_token=csrf_token)
        userName = Authorize.get_jwt_subject()
        user: schemas.User = await stringUtils.getUserSchemaFromName(userName, db)
        xgrowKey: str = await userUtils.asyncGetXgrowKeyForCurrentUser(user)
        connection = await getConnectionManagerFrontend().connect(websocket=websocket, userName=userName)

        try:
            while True:
                command = await websocket.receive_text()
                await getConnectionManagerFrontend().sendMessageToDevice(f"command: {command} was sent...", userName)
                await getCommandManagerFrontend().commandDispatcher(command=command, xgrowKey=xgrowKey, userName=userName)



        except WebSocketDisconnect:
            getConnectionManagerFrontend().disconnect(userName=userName)
            # await websocket.close() #<<=== niepotrzebne
            # await manager.broadcast(f"Client #{Authorize.get_jwt_subject()} left the chat")
    except AuthJWTException:
        await websocket.send_text("login failed...")
        await websocket.close()


'''
                print(data)
                # FIXME: test loop
                await getConnectionManagerFrontend().sendMessageToDevice(
                    f"Connected user:{userName}, xkey: {connection.getUserName()}", userName=userName)

                count = 0
                xklist = []
                for connection in getConnectionManagerFrontend().active_connections:
                    count = count + 1
                    connection: ConnectionFrontend
                    xklist.append(connection.getUserName())
                    await getConnectionManagerFrontend().sendMessageToDevice(f"Pobierz Pot{connection.getUserName()}",
                                                                             connection.getUserName())
                await getConnectionManagerFrontend().sendMessageToDevice(
                    f'chuj {getConnectionManagerFrontend().active_connections}, count: {count}, xkeyList: {xklist}',
                    connection.getUserName())

'''