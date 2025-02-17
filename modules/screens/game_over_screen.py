"""
A module that contains the GameOverScreen class.
"""

import pygame

from modules.screens.base_screen import BaseScreen
from resource_path import resource_path


class GameOverScreen(BaseScreen):
    """
    A class that represents the game over screen. Inherits from BaseScreen.
    
    Attributes:
    blur_surface (pygame.Surface): The blurred background.
    
    Methods:
    frame: Draws the game over screen.
    """
    def __init__(self, screen, game_font, parent):
        super().__init__(screen, game_font, parent)
        self.blur_surface = pygame.image.load(resource_path('images/blur.jpg')).convert_alpha()

    def frame(self, screen_size, events, score, best_score):
        """
        Draws the game over screen.
        
        Parameters:
        screen_size (tuple): The size of the screen.
        events (list): The events to listen for.
        score (int): The player's score.
        best_score (int): The best score.
        """
        self.screen.blit(pygame.transform.scale(self.blur_surface, screen_size), (0, 0))
        self.draw_text("GAME OVER", (screen_size[0] // 2, screen_size[1] // 2.1))
        self.draw_text(f"YOUR SCORE: {score}", (screen_size[0] // 2, screen_size[1] // 1.7))
        self.draw_text(f"BEST SCORE: {best_score}", (screen_size[0] // 2, screen_size[1] // 1.1))

        self.draw_button(screen_size[0] // 2, screen_size[1] // 1.25,
                         "CLICK OR PRESS 'SPACE' TO START", self.parent.start_game, events)
        self.draw_button(screen_size[0] // 2, screen_size[1] // 12,
                         "[VISIT MY GITHUB]", self.parent.open_github, events)
        self.draw_button(screen_size[0] - screen_size[0] // 14, screen_size[1] // 14,
                         "[X]", self.parent.quit_game, events, "Red")
