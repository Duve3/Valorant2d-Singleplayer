import pygame
import pygame_wrapper as pgw

class MainMenu(pgw.MenuType):
    def __init__(self, screen, fpsClock, fps):
        super().__init__(screen, fpsClock, fps)

    def run(self) -> None:
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return


