import json


class Config:
    def __init__(self, configPath):
        with open(configPath, "r") as cf:
            self.raw = cf.read()

        self.json = json.loads(self.raw)

        self.PATH_asset = self.json["PATH_ASSET"]
        self.PATH_config = self.json["PATH_CONFIG"]
        self.PATH_level = self.json["PATH_LEVEL"]

    def writeConfig(self, **kwargs):
        print(kwargs)
