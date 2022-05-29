from pydantic import BaseModel


class schemasUtils():

    @staticmethod
    def filterUnableToSave(dictionary: dict):
        newDict = dictionary.copy()

        for key, value in dictionary.items():
            if isinstance(value, dict):
                del newDict[f'{key}']
        return newDict
