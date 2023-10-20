import pygame
import pygame_wrapper as pgw
import pygame_wrapper.logging
from pygame_wrapper.UI import Button
import typing
from .player import Player
from .level import Level, _createCustomColor, Object
import os

from src.config import Config


class VisualLevelList:
    def __init__(self, px, py, sx, sy, color, levels: list[Level], font):
        self.x = px
        self.y = py
        self.OFFSET_y = 0

        self.logger = pgw.logging.setupLogging(self.__class__.__name__)

        self.surf = pygame.Surface((sx, sy))

        self.color = _createCustomColor(color)

        self.buttons: list[Button] = []

        self.levels = {level.name: level for level in levels}
        self.font = font
        self.recreate_buttons()
        self.maximumButtonVolume = 0
        newList = self.buttons.copy()
        newList.pop(0)
        for button in newList:
            self.maximumButtonVolume += button.h + 10  # height of button + padding

    def recreate_buttons(self):
        self.buttons = []
        for i, level in enumerate(self.levels.values()):
            self.logger.debug(f"level {level}")
            self.buttons.append(
                Button(10, ((i * 60) + 10) + self.OFFSET_y, self.surf.get_size()[0] - 20, 80, self.color.lighten(20),
                       self.color.darken(40),
                       self.font, level.name, darkLightOffset=10, textOffset=(0, -10)))

    def render(self, surf: pygame.Surface):
        self.surf.fill(self.color)
        for button in self.buttons:
            button.render_to(self.surf)
        surf.blit(self.surf, (self.x, self.y))

    def hook_events(self, events: list[pygame.Event]):
        scroll_movement = 50
        for event in events:
            if event.type == pygame.MOUSEWHEEL:
                oldy = self.OFFSET_y
                if event.y == -1:
                    self.OFFSET_y += scroll_movement
                elif event.y == 1:
                    self.OFFSET_y -= scroll_movement

                if self.OFFSET_y <= 0:
                    self.OFFSET_y = 0

                if self.OFFSET_y > self.maximumButtonVolume:
                    self.OFFSET_y = oldy

                self.recreate_buttons()

        for button in self.buttons:
            button.hook_events(events)


class LevelSelection(pgw.MenuType):
    def __init__(self, screen, fpsClock, fps, config: Config):
        super().__init__(screen, fpsClock, fps)
        self.config = config
        self.logger = pgw.logging.setupLogging(self.__class__.__name__)

        self.storyLevels = []
        storyPath = self.config.PATH_level + "\\story\\"
        self.logger.debug(storyPath)
        for level in os.listdir(storyPath):
            if not os.path.isfile(storyPath + level):
                continue

            with open(storyPath + level, "r") as lf:
                self.storyLevels.append(Level.FromRaw(lf.read()))

        self.logger.debug(self.storyLevels)

        self.ExitEvent = pygame.USEREVENT + 1

        self.visualList = VisualLevelList(20, 20, 400, self.screen.get_size()[1] - 40, (25, 25, 25), self.storyLevels,
                                          pgw.Font(self.config.PATH_asset + "\\Comfortaa.ttf", 30, (200, 200, 200)))

    def run(self) -> Level | None:
        while True:
            events = pygame.event.get()
            self.visualList.hook_events(events)
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                elif event.type == self.ExitEvent:
                    return event.value

            self.logic()
            self.rendering()

            pygame.display.flip()

    def rendering(self) -> None:
        self.screen.fill((30, 30, 30))

        self.visualList.render(self.screen)

    def logic(self) -> None:
        for button in self.visualList.buttons:
            if button.state is True:
                finalEvent = pygame.Event(pygame.USEREVENT + 1, value=self.visualList.levels[button.text])
                pygame.event.post(finalEvent)


class Game(pgw.MenuType):  # we are using menutype so that you can just run it like a menu
    def __init__(self, screen, fpsClock, fps, config: Config):
        super().__init__(screen, fpsClock, fps)
        self.config = config
        self.logger = pgw.logging.setupLogging(self.__class__.__name__)

        self.objs: list[Object] = []
        self.textures = []
        self.level = None

        self.selector = LevelSelection(screen, fpsClock, fps, config)

    def run(self) -> None:
        level = self.selector.run()
        self.level = level
        self.logger.debug(f"Objs: {self.objs}")
        while True:
            self.fpsClock.tick(self.fps)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            self.logic()
            self.rendering()

            pygame.display.flip()

    def rendering(self) -> None:
        self.level.build()(self.screen, self.textures)

    def logic(self) -> None:
        pass
