"""
A module that contains the StartGameScreen class.
"""

from typing import List, Tuple, TYPE_CHECKING

import pygame

from modules.screens.base_screen import BaseScreen
from modules.util.constants import Colors
from resource_path import resource_path

if TYPE_CHECKING:
    from modules.Game import Game


class StartGameScreen(BaseScreen):
    """
    A class that represents the start game screen.
    
    This screen displays the main menu with the best score, start button,
    and other navigation options. It inherits from BaseScreen for common functionality.
    
    Attributes:
        sky_surface: Background sky image
        vignette_surface: Vignette overlay for visual effect
    """
    def __init__(
        self, 
        screen: pygame.Surface, 
        game_font: pygame.font.Font, 
        parent: 'Game'
    ) -> None:
        """
        Initialize the start game screen.
        
        Args:
            screen: Surface to draw on
            game_font: Font for rendering text
            parent: Reference to the main Game instance
        """
        super().__init__(screen, game_font, parent)

        # Load background images
        self.sky_surface = pygame.image.load(
            resource_path('images/sky.jpg')).convert()
        self.vignette_surface = pygame.image.load(
            resource_path('images/vignette.png')).convert_alpha()

    def frame(
        self, 
        screen_size: Tuple[int, int], 
        events: List[pygame.event.Event], 
        best_score: int
    ) -> None:
        """
        Render the start game screen frame.
        
        Args:
            screen_size: Current screen dimensions
            events: List of pygame events to process
            best_score: Current best score to display
        """
        # Positions
        center_x = screen_size[0] // 2
        score_y = int(screen_size[1] / 1.1)
        action_button_y = int(screen_size[1] / 1.25)
        marathoner_y = screen_size[1] // 12
        quit_button_x = screen_size[0] - screen_size[0] // 14
        quit_button_y = screen_size[1] // 14

        # Draw background layers
        self.screen.blit(pygame.transform.scale(self.sky_surface, screen_size), (0, 0))
        self.screen.blit(pygame.transform.scale(self.vignette_surface, screen_size), (0, 0))

        # Draw best score text and game name
        self.draw_text(f"BEST SCORE: {best_score}", (center_x, score_y))
        self.draw_text("Marathoner", (center_x, marathoner_y))

        # Draw action button
        self.draw_button(
            center_x, 
            action_button_y,
            "CLICK OR PRESS 'SPACE' TO START", 
            self.parent.start_game, 
            events
        )

        # Draw quit button
        self.draw_button(
            quit_button_x, 
            quit_button_y,
            "[X]", 
            self.parent.quit_game, 
            events, 
            Colors.RED
        )
