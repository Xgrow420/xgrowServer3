from typing import List

from fastapi import WebSocket


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

    def getConnectionByXgrowKey(self, xgrowKey):
        if xgrowKey == self._xgrowKey:
            return self._webSocket


class ConnectionManager:

    _instance = None

    @staticmethod
    def getInstance():
        if ConnectionManager._instance is None:
            ConnectionManager()
        return ConnectionManager._instance

    def __init__(self):
        if ConnectionManager._instance is not None:
            raise Exception("ConnectionManager class is a singleton!")
        else:
            self.active_connections: List[Connection] = []
            ConnectionManager._instance = self

    async def connect(self, websocket: WebSocket, xgrowKey: str):
        connection = Connection(websocket=websocket, xgrowKey=xgrowKey)
        self.active_connections.append(connection)
        return connection

    def disconnect(self, xgrowKey):
        for connection in self.active_connections:
            if connection.getConnectionByXgrowKey(xgrowKey):
                print(f"{connection.getXgrowKey()} disconnected")
                self.active_connections.remove(connection)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def sendMessageToDevice(self, message: str, xgrowKey: str):
        for connection in self.active_connections:
            if connection.getXgrowKey() == xgrowKey:
                try:
                    await connection.getWebSocket().send_text(message)
                except RuntimeError:
                    print(f"webSocket: {connection.getWebSocket()} does not exist i will deleting it...")
                    self.active_connections.remove(connection)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.getWebSocket().send_text(message)



    # TODO: add if statment connection not found info




def getConnectionManager():
    connectionManager : ConnectionManager = ConnectionManager.getInstance()
    return connectionManager
