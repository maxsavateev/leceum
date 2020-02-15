import pygame

class PytView:
    def __init__(self, width = 800, height = 600, fps = 60, caption = "Окно"):

        self.width = width
        self.height = height
        self.fps = fps
        self.caption = caption

        self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF)
        pygame.display.set_caption(self.caption)
        self.icon_window = pygame.image.load("images/icon.jpg")
        pygame.display.set_icon(self.icon_window)
        self.frame = pygame.image.load("images/menu.png").convert()
        self.screen.blit(self.frame, (0, 0))
        self.background = pygame.image.load("images/background.png")
        self.screen.blit(self.background, (25, 25))
