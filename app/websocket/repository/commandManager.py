from app import settings
from app.utils.currentUserUtils import userUtils
from app.utils.stringUtils import asyncGetUserSchemaFromName
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
            self.inspectedXgrowKey = {} #{"Admin": "inspectedKey"}
            self.inspectedUser = {} #{"Admin": "insepctedUser"}

            CommandManager._instance = self


    async def sendCommandToXgrow(self, command: str, xgrowKey: str, userName: str):
        self.adminCommandListener(command, xgrowKey, userName)

        if userName in self.inspectedXgrowKey:
            inspectedXgrowKey = self.inspectedXgrowKey[userName]
            await getConnectionManagerXgrow().sendMessageToDevice(message=command, xgrowKey=inspectedXgrowKey)
            return True

        if not await getConnectionManagerXgrow().sendMessageToDevice(message=command, xgrowKey=xgrowKey):
            await getConnectionManagerFrontend().sendMessageToDevice("[Server] Connection ERROR", userName=userName)
            return False



    async def sendCommandToFrontend(self, command: str, xgrowKey: str, userName: str):

        for admin, inspectedUser in self.inspectedUser.items():
            if inspectedUser == userName:
                await getConnectionManagerFrontend().sendMessageToDevice(message=command, userName=admin)

        if not await getConnectionManagerFrontend().sendMessageToDevice(message=command, userName=userName):
            await getConnectionManagerXgrow().sendMessageToDevice(f"[Server] Connection ERROR {userName} not found", xgrowKey=xgrowKey)
            return False

    def adminCommandListener(self, command: str, adminXgrowKey: str, adminName: str):
        if adminName == "Xgrow":
            if command.startswith("connect "):
                command_parts = command.split()
                if len(command_parts) >= 3:
                    inspectedUser = command_parts[1]
                    inspectedXgrowKey = command_parts[2]

                    if adminName in self.inspectedXgrowKey:
                        self.inspectedXgrowKey[adminName] = inspectedXgrowKey
                    else:
                        self.inspectedXgrowKey[adminName] = inspectedXgrowKey

                    if adminName in self.inspectedUser:
                        self.inspectedUser[adminName] = inspectedUser
                    else:
                        self.inspectedUser[adminName] = inspectedUser
            #     else:
            #         print("Błąd: Komenda 'connect' musi zawierać użytkownika i klucz.")
            # else:
            #     print("Błąd: Nieprawidłowa komenda.")


        return False

def getCommandManager():
    commandManagerFrontend: CommandManager = CommandManager.getInstance()
    return commandManagerFrontend

