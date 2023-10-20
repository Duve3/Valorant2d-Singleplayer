import logging
import pygame.freetype
import pygame_wrapper as pgw
import pygame_wrapper.logging
import pygame_wrapper.UI
from game.game import Game
from config import Config


class DisclaimerMenu(pgw.MenuType):
    def __init__(self, screen, fpsClock, fps, bgColor: pgw.CustomColor):
        super().__init__(screen, fpsClock, fps)

        self.bgColor: pgw.CustomColor = bgColor  # background color
        self.FONT_disclaim = pgw.Font("./assets/Comfortaa.ttf", 30, (200, 200, 200))  # font for the disclaimer text
        with open("./assets/disclaimer.txt", "r") as df:
            self.text = df.read()  # opens the file with the disclaimer and reads it

        self.surf = pygame.Surface(self.screen.get_size(), flags=pygame.SRCALPHA)  # surface that allows alpha
        self.logger = pgw.logging.setupLogging(self.__class__.__name__, level=logging.DEBUG)  # logger for testing stuff

    def run(self):
        frames = 0
        fadeOut = False
        fadeIn = True
        ExitEvent = pygame.Event(pygame.USEREVENT + 1)
        timerEvent = pygame.USEREVENT + 3
        StartFadeOut = pygame.Event(pygame.USEREVENT + 2, timer=[timerEvent, 500])

        self.surf.set_alpha(0)  # set the screen to black basically
        while True:
            frames += 1  # frames counter for animations
            self.fpsClock.tick(self.fps)  # fps limiter
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                elif event.type == StartFadeOut.type:  # listen for start fade timer event
                    self.logger.debug("Received Fade Start Event")
                    pygame.time.set_timer(event.timer[0], event.timer[1],
                                          loops=0)  # creates a timer using the properties set before running

                elif event.type == timerEvent:  # listen for timer event, then start fade out
                    fadeOut = True

                elif event.type == ExitEvent.type:  # quit event for later
                    return

                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:  # userinput listen
                    self.logger.info(f"Exiting {self.__class__.__name__} early due to USERINPUT")
                    return

            if frames % 5 == 0 and fadeIn is True:
                add = self.surf.get_alpha() + 2
                if add >= 100:
                    add = 128
                    fadeIn = False
                    pygame.event.post(StartFadeOut)
                    self.logger.debug("posted event")
                self.surf.set_alpha(add)

            elif frames % 5 == 0 and fadeOut is True:
                add = self.surf.get_alpha() - 4
                if add <= 30:
                    add = 0
                    fadeOut = False
                    pygame.event.post(ExitEvent)
                    self.logger.debug("posted exitevent")

                self.surf.set_alpha(add)

            self.surf.fill(self.bgColor)

            self.FONT_disclaim.multiline_render_to(self.surf, (
                self.FONT_disclaim.get_center(self.screen, self.text.splitlines()[0]).x, 200), self.text)

            self.screen.blit(self.surf, (0, 0))

            pygame.display.flip()


class MainMenu(pgw.MenuType):
    def __init__(self, screen, fpsClock, fps, config: Config):
        super().__init__(screen, fpsClock, fps)
        self.config = config
        self.logger = pgw.logging.setupLogging(self.__class__.__name__, level=logging.DEBUG)

        self.bgColor = pgw.CustomColor(
            (30, 30, 30))  # the background color that's going to be used basically throughout this project

        self.disclaimer = DisclaimerMenu(screen, fpsClock, fps, self.bgColor)  # create a disclaimer menu for when we run it later
        self.FONT_Title = pgw.fonts.PredefinedFont("./assets/Comfortaa.ttf", 50, (200, 200, 200), "Valorant 2D - Singleplayer")  # create a font with the text already defined

        self.FONT_Button = pgw.Font("./assets/Comfortaa.ttf", 30, (200, 200, 200))  # the font for buttons
        self.BUTTON_Play = pgw.UI.Button(self.screen.get_rect().centerx - 100, 200, 200, 40, (100, 100, 100), (60, 60, 60), self.FONT_Button, "Play")  # play button

        self.game = Game(self.screen, self.fpsClock, self.fps, self.config)

    def rendering(self) -> None:
        self.screen.fill(self.bgColor)

        self.FONT_Title.multiline_render_to(self.screen, (self.FONT_Title.get_center(self.screen).x, 50))

        self.BUTTON_Play.render_to(self.screen)

    def logic(self):
        if self.BUTTON_Play.state:  # check if the button is clicked
            self.game.run()

    def run(self) -> None:
        self.disclaimer.run()
        while True:
            self.fpsClock.tick(self.fps)  # fps limit
            events = pygame.event.get()  # hook events
            self.BUTTON_Play.hook_events(events)
            for event in events:  # event loop
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            self.logic()
            self.rendering()

            pygame.display.flip()
