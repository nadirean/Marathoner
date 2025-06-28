"""
A module that contains the GameOverScreen class.
"""

from typing import List, Tuple, TYPE_CHECKING

import pygame

from modules.screens.base_screen import BaseScreen
from modules.util.constants import Colors
from resource_path import resource_path

if TYPE_CHECKING:
    from modules.Game import Game


class GameOverScreen(BaseScreen):
    """
    A class that represents the game over screen.
    
    This screen displays when the game ends, showing the player's final score,
    the best score, and options to restart or navigate to other screens.
    It inherits from BaseScreen for common functionality.

    Attributes:
        blur_surface: Blurred background image for game over overlay
    """
    def __init__(
        self, 
        screen: pygame.Surface,
        game_font: pygame.font.Font,
        parent: 'Game'
    ) -> None:
        """
        Initialize the game over screen.

        Args:
            screen: Surface to draw on
            game_font: Font for rendering text
            parent: Reference to the main Game instance
        """
        super().__init__(screen, game_font, parent)

        # Load the blurred background image
        self.blur_surface = pygame.image.load(
            resource_path('images/blur.jpg')
        ).convert_alpha()

    def frame(
        self, 
        screen_size: Tuple[int, int], 
        events: List[pygame.event.Event], 
        score: int, 
        best_score: int
    ) -> None:
        """
        Render the game over screen frame.

        Args:
            screen_size: Current screen dimensions
            events: List of pygame events to process
            score: Player's final score for this game
            best_score: Current best score
        """
        # Positions
        center_x = screen_size[0] // 2
        title_y = int(screen_size[1] / 2.1)
        score_y = int(screen_size[1] / 1.7)
        best_score_y = int(screen_size[1] / 1.1)
        restart_x = screen_size[0] // 2
        restart_y = int(screen_size[1] / 1.25)
        marathoner_x = screen_size[0] // 2
        marathoner_y = screen_size[1] // 12
        quit_x = screen_size[0] - screen_size[0] // 14
        quit_y = screen_size[1] // 14

        # Draw background
        self.screen.blit(
            pygame.transform.scale(self.blur_surface, screen_size), 
            (0, 0)
        )

        # Draw title, scores and game name
        self.draw_text("GAME OVER", (center_x, title_y))
        self.draw_text(f"YOUR SCORE: {score}", (center_x, score_y), Colors.WHITE)
        self.draw_text(f"BEST SCORE: {best_score}", (center_x, best_score_y))
        self.draw_text("Marathoner", (marathoner_x, marathoner_y))

        # Draw action button
        self.draw_button(
            restart_x, 
            restart_y,
            "CLICK OR PRESS 'SPACE' TO START", 
            self.parent.start_game, 
            events
        )

        # Quit button
        self.draw_button(
            quit_x, 
            quit_y,
            "[X]", 
            self.parent.quit_game, 
            events, 
            Colors.RED
        )
