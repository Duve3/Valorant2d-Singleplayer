import pygame.freetype
import pygame_wrapper as pgw
from mainMenu import MainMenu
from config import Config


class Game(pgw.GameType):
    """
    The 'game' class, this class is really just a wrapper for all the menu classes, as that's really all it does.
    """

    def __init__(self, config: Config):
        super().__init__("Valorant2D - Singleplayer", RES=(1280, 720), fpsCap=60, hwflags=[pygame.HWACCEL, pygame.SRCALPHA])
        self.menus = [MainMenu(self.screen, self.fpsClock, self.fps, config)]
        self.config = config

    def run(self) -> None:
        self.router(0).run()

    def router(self, idx) -> pgw.MenuType:  # noqa:signature ; signature will not match
        return self.menus[idx]





def main():
    pygame.init()
    configuration = Config(r"C:\Users\laksh\PycharmProjects\Valorant2d-Singleplayer\src\config\config.json")
    g = Game(configuration)
    g.run()


if __name__ == "__main__":
    main()
