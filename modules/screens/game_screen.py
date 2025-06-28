"""
A module that contains the GameScreen class.
"""

from typing import List, Tuple, TYPE_CHECKING

import pygame

from modules.screens.base_screen import BaseScreen
from modules.util.constants import Colors, GROUND_HEIGHT_RATIO

if TYPE_CHECKING:
    from modules.Game import Game


class GameScreen(BaseScreen):
    """
    A class that represents the main game screen during gameplay.
    
    This screen handles the active game state, displaying the player,
    obstacles, background, and UI elements during gameplay.
    """
    def __init__(
        self, 
        screen: pygame.Surface, 
        game_font: pygame.font.Font, 
        parent: 'Game'
    ) -> None:
        """
        Initialize the game screen.

        Args:
            screen: Surface to draw on
            game_font: Font for rendering text
            parent: Reference to the main Game instance
        """
        super().__init__(screen, game_font, parent)

    def frame(
        self, 
        screen_size: Tuple[int, int], 
        events: List[pygame.event.Event]
    ) -> None:
        """
        Render the main game screen frame.
        
        Args:
            screen_size: Current screen dimensions
            events: List of pygame events to process
        """
        # Positions
        ground_y = int(screen_size[1] * GROUND_HEIGHT_RATIO)
        esc_button_x = screen_size[0] - screen_size[0] // 6
        esc_button_y = screen_size[1] // 14
        quit_button_x = screen_size[0] - screen_size[0] // 14
        quit_button_y = screen_size[1] // 14

        # Draw sky background
        self.screen.blit(
            pygame.transform.scale(self.parent.sky_surface, screen_size),
            (0, 0)
        )
        # Draw ground at bottom portion of screen
        self.screen.blit(
            pygame.transform.scale(self.parent.ground_surface, screen_size),
            (0, ground_y)
        )

        # Update and draw game objects
        self.parent.player.draw(self.screen)
        self.parent.player.update(self.parent.channel2)
        self.parent.obstacle_group.draw(self.screen)
        self.parent.obstacle_group.update()

        # Draw vignette overlay
        self.screen.blit(
            pygame.transform.scale(self.parent.vignette_surface, screen_size), 
            (0, 0)
        )

        # Draw score display
        self.parent.score = self.parent.score_system.display_score(
            self.game_font, 
            self.parent.start_time, 
            self.screen
        )

        # Draw pause button (ESC)
        self.draw_button(
            esc_button_x, 
            esc_button_y,
            "[ESC]", 
            self.parent.pause_game, 
            events
        )

        # Draw quit button (X)
        self.draw_button(
            quit_button_x, 
            quit_button_y,
            "[X]", 
            self.parent.quit_game, 
            events, 
            Colors.RED
        )

        # Check for collisions
        if self.parent.collision_sprite() == 0:
            self.parent.current_screen = 0
