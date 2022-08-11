from app.websocket.repository.connectionManagerXgrow import getConnectionManagerXgrow
from app.websocket.repository.connectionManagerFrontend import getConnectionManagerFrontend


class CommandManagerFrontend():

    _instance = None

    @staticmethod
    def getInstance():
        if CommandManagerFrontend._instance is None:
            CommandManagerFrontend()
        return CommandManagerFrontend._instance

    def __init__(self):
        if CommandManagerFrontend._instance is not None:
            raise Exception("CommandManagerFrontend class is a singleton!")
        else:
            self.task = ""
            CommandManagerFrontend._instance = self

    ''''''
    async def commandDispatcher(self, command: str, xgrowKey: str, userName: str):
        #FIXME: check if it work correctly
        #if self.task != "":
        #    if await getConnectionManagerXgrow().sendMessageToDevice(message=self.task, xgrowKey=xgrowKey):
        #        self.task = ""

        if not await getConnectionManagerXgrow().sendMessageToDevice(message=command, xgrowKey=xgrowKey):
            #self.task = command
            await getConnectionManagerFrontend().sendMessageToDevice("ERROR", userName=userName)



def getCommandManagerFrontend():
    commandManagerFrontend: CommandManagerFrontend = CommandManagerFrontend.getInstance()
    return commandManagerFrontend
