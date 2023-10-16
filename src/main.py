import pygame
import pygame_wrapper as pgw


class Game(pgw.GameType):
    """
    The 'game' class, this class is really just a wrapper for all the menu classes, as that's really all it does.
    """

    def __init__(self):
        super().__init__("Valorant2D - Singleplayer", RES=(1280, 720), fpsCap=60)
        self.menus = []

    def run(self) -> None:
        self.router(0)

    def router(self, idx) -> pgw.MenuType:  # noqa:signature ; signature will not match
        return self.menus[idx]


def main():
    g = Game()
    g.run()


if __name__ == "__main__":
    main()
