from app.websocket.repository.connectionManagerXgrow import getConnectionManagerXgrow
from app.websocket.repository.connectionManagerFrontend import getConnectionManagerFrontend


class CommandManager():

    _instance = None

    @staticmethod
    def getInstance():
        if CommandManager._instance is None:
            CommandManager()
        return CommandManager._instance

    def __init__(self):
        if CommandManager._instance is not None:
            raise Exception("CommandManagerFrontend class is a singleton!")
        else:
            self.task = {}
            CommandManager._instance = self


    async def sendCommandToXgrow(self, command: str, xgrowKey: str, userName: str):
        if not await getConnectionManagerXgrow().sendMessageToDevice(message=command, xgrowKey=xgrowKey):
            await getConnectionManagerFrontend().sendMessageToDevice("[Server] Connection ERROR", userName=userName)
            return False


    async def sendCommandToFrontend(self, command: str, xgrowKey: str, userName: str):
        if not await getConnectionManagerFrontend().sendMessageToDevice(message=command, userName=userName):
            await getConnectionManagerXgrow().sendMessageToDevice(f"[Server] Connection ERROR {userName} not found", xgrowKey=xgrowKey)
            return False

def getCommandManager():
    commandManagerFrontend: CommandManager = CommandManager.getInstance()
    return commandManagerFrontend
