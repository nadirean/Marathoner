"""
A module that contains the StartGameScreen class.
"""
import pygame

from modules.screens.base_screen import BaseScreen
from resource_path import resource_path


class StartGameScreen(BaseScreen):
    """
    A class that represents the start game screen. Inherits from BaseScreen.
    
    Attributes:
    sky_surface (pygame.Surface): The sky background.
    vignette_surface (pygame.Surface): The vignette overlay.
    
    Methods:
    frame: Draws the start game screen.
    """
    def __init__(self, screen, game_font, parent):
        super().__init__(screen, game_font, parent)
        self.sky_surface = pygame.image.load(
            resource_path('images/sky.jpg')).convert()
        self.vignette_surface = pygame.image.load(
            resource_path('images/vignette.png')).convert_alpha()

    def frame(self, screen_size, events, best_score):
        """
        Draws the start game screen.
        
        Parameters:
        screen_size (tuple): The size of the screen.
        events (list): The events to listen for.
        best_score (int): The best score.
        """
        self.screen.blit(pygame.transform.scale(self.sky_surface, screen_size), (0, 0))
        self.screen.blit(pygame.transform.scale(self.vignette_surface, screen_size), (0, 0))

        self.draw_text(f"BEST SCORE: {best_score}", (screen_size[0] // 2, screen_size[1] // 1.1))
        self.draw_button(screen_size[0] // 2, screen_size[1] // 1.25,
                         "CLICK OR PRESS 'SPACE' TO START", self.parent.start_game, events)
        self.draw_button(screen_size[0] // 2, screen_size[1] // 12,
                         "[VISIT MY GITHUB]", self.parent.open_github, events)
        self.draw_button(screen_size[0] - screen_size[0] // 14, screen_size[1] // 14,
                         "[X]", self.parent.quit_game, events, "Red")
