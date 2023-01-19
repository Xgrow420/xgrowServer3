from typing import List

from fastapi import WebSocket


class ConnectionFrontend:
    def __init__(self, websocket: WebSocket, userName=None):
        self._webSocket: WebSocket = websocket
        self._userName: str = userName


    def getWebSocket(self):
        return self._webSocket

    def setWebSocket(self, websocket: WebSocket):
        self._webSocket = websocket

    def getUserName(self):
        return self._userName

    def setUserName(self, userName: str):
        self._userName = userName

    def getConnectionByWebSocket(self, websocket: WebSocket):
        if websocket == self._webSocket:
            return websocket

    def getConnectionByUserName(self, userName):
        if userName == self._userName:
            return self._webSocket


class ConnectionManagerFrontend:

    _instance = None

    @staticmethod
    def getInstance():
        if ConnectionManagerFrontend._instance is None:
            ConnectionManagerFrontend()
        return ConnectionManagerFrontend._instance

    def __init__(self):
        if ConnectionManagerFrontend._instance is not None:
            raise Exception("ConnectionManager class is a singleton!")
        else:
            self.active_connections: List[ConnectionFrontend] = []
            ConnectionManagerFrontend._instance = self

    async def connect(self, websocket: WebSocket, userName: str):
        for connect in self.active_connections:
            if connect.getUserName() == userName:
                await connect.getWebSocket().send_text(f"[Server] New webSocket connection was raised for: {userName}")
                await connect.getWebSocket().close(1000, f"[!] New webSocket connection was raised for: {userName}")
                if connect in self.active_connections:
                    self.active_connections.remove(connect)

        connection = ConnectionFrontend(websocket=websocket, userName=userName)
        self.active_connections.append(connection)
        return connection

    async def disconnect(self, userName):
        for connection in self.active_connections:
            if connection.getConnectionByUserName(userName):
                #await connection.getWebSocket().close(1000, "connection close")
                print(f"{connection.getUserName()} disconnected")
                self.active_connections.remove(connection)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def sendMessageToDevice(self, message: str, userName: str):
        for connection in self.active_connections:
            if connection.getUserName() == userName:
                try:
                    await connection.getWebSocket().send_text(message)
                    return True
                except RuntimeError:
                    print(f"webSocket: {connection.getWebSocket()} does not exist i will deleting it...")
                    self.active_connections.remove(connection)
                    return False

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.getWebSocket().send_text(message)



    # TODO: add if statment connection not found info




def getConnectionManagerFrontend():
    connectionManager : ConnectionManagerFrontend = ConnectionManagerFrontend.getInstance()
    return connectionManager
