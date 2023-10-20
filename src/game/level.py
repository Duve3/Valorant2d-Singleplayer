import pygame
import pygame_wrapper as pgw
from pygame_wrapper import CustomColor
import json


def _createCustomColor(color):
    """
    not intended for use outside of this, can change at any time
    """
    if isinstance(color, pygame.Color):
        color = CustomColor([color.r, color.g, color.b], color.a)
    elif isinstance(color, tuple) or isinstance(color, list):
        color = CustomColor([color[0], color[1], color[2]], color[3]) if len(color) == 4 else CustomColor(color)
    elif isinstance(color, str):
        color = CustomColor(color)

    return color


# objs

class Object:
    def __init__(self, px, py, sx, sy, cls, textureID: int = 0, color=None):
        self.x = px
        self.y = py
        self.size_x = sx
        self.size_y = sy
        self.textureID = textureID
        self.color = None
        self.cls = cls

        if textureID == 0 and color is not None:
            self.color: CustomColor = _createCustomColor(color)
        elif textureID == 0:
            raise NotImplementedError("Failed to find a color with textureID of 0!")

    def ToJSON(self):
        obj = {
                    "_type": self.cls.__class__.__name__.lower(),
                    "x": self.x,
                    "y": self.y,
                    "sizex": self.size_x,
                    "sizey": self.size_y,
                    "textureID": self.textureID,
                    "color": self.color.color if self.color is not None else None
                }
        return obj

    def render(self, surf, textures: list): ...

    @staticmethod
    def FromJSON(raw):
        if not isinstance(raw, dict):  # basically if its is a dictionary already, we do not need to convert it
            data = json.loads(raw)
        else:
            data = raw

        if data["_type"] == "tile":
            return Tile(data["x"], data["y"], data["sizex"], data["sizey"], data["textureID"], data["color"])


class Tile(Object):
    def __init__(self, px, py, sx, sy, textureID: int = 0, color=None):
        super().__init__(px, py, sx, sy, self, textureID, color)

    def render(self, surf: pygame.Surface, textures: list):
        if self.textureID != 0:
            surf.blit(pygame.transform.smoothscale(textures[self.textureID], (self.size_x, self.size_y)),
                      (self.x, self.y))

        else:
            pygame.draw.rect(surf, self.color, pygame.FRect(self.x, self.y, self.size_x, self.size_y))


class Level:
    def __init__(self, name, version, backgroundColor, objList: list[Object]):
        self.objs = objList
        self.name = name
        self.ver = version
        self.bgcolor = _createCustomColor(backgroundColor)

    def convertToRaw(self):
        rawObjs = []
        for obj in self.objs:
            rawObjs.append(obj.ToJSON())

        logger.debug(rawObjs)

        return json.dumps({"LEVEL_NAME": self.name,
                           "LEVEL_VERSION": self.ver,
                           "LEVEL_BACKGROUND": {
                               "COLOR": True,
                               "VALUE": self.bgcolor.color
                           },
                           "OBJECTS": rawObjs})

    def build(self):
        # prolly create an actual builder func to turn everything into smaller/bigger objs to efficient
        return self.__render__

    def __render__(self, surf, textures):
        surf.fill(self.bgcolor)
        for obj in self.objs:
            obj.render(surf, textures)

    @staticmethod
    def FromRaw(raw):
        data = json.loads(raw)
        if data["LEVEL_VERSION"] == 0:
            objs = []
            for o in data["OBJECTS"]:
                objs.append(Object.FromJSON(o))
            if data["LEVEL_BACKGROUND"]["COLOR"] is True:
                color = data["LEVEL_BACKGROUND"]["VALUE"]
            else:
                color = (255, 255, 255)
            return Level(data["LEVEL_NAME"], data["LEVEL_VERSION"], color, objs)


if __name__ == "__main__":
    import pygame_wrapper.logging
    import pygame_wrapper as pgw

    logger = pgw.logging.setupLogging("Testing_LEVEL")

    t = Tile(15, 10, 50, 100, 0, (255, 255, 255))

    t2 = Tile(100, 100, 50, 20, 0, (255, 0, 0))

    tut = Level("Tutorial", 0, (200, 200, 200), [t, t2])

    with open(r"C:\Users\laksh\PycharmProjects\Valorant2d-Singleplayer\src\game\levels\story\tut.json", "w") as tf:
        tf.write(tut.convertToRaw())

    level = Level.FromRaw(tut.convertToRaw())
    print(level.objs)
