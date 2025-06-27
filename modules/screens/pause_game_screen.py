"""
A module that contains the PauseGameScreen class.
"""

from typing import List, Tuple, TYPE_CHECKING

import pygame

from modules.screens.base_screen import BaseScreen
from modules.util.constants import Colors
from resource_path import resource_path

if TYPE_CHECKING:
    from modules.Game import Game
    from modules.util.settings import Settings


class PauseGameScreen(BaseScreen):
    """
    A class that represents the pause game screen.
    
    This screen displays the pause menu with options for resuming,
    changing settings, resetting scores, and other game controls.
    It inherits from BaseScreen for common functionality.
    
    Attributes:
        blur_surface: Blurred background image for pause overlay
    """
    def __init__(
        self, 
        screen: pygame.Surface, 
        game_font: pygame.font.Font, 
        parent: 'Game'
    ) -> None:
        """
        Initialize the pause game screen.
        
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
        best_score: int, 
        settings: 'Settings'
    ) -> None:
        """
        Render the pause game screen frame.
        
        Args:
            screen_size: Current screen dimensions
            events: List of pygame events to process
            best_score: Current best score to display
            settings: Game settings object for toggle states
        """
        # Draw background
        self.screen.blit(
            pygame.transform.scale(self.blur_surface, screen_size), 
            (0, 0)
        )

        # Positions
        center_x = screen_size[0] // 2
        title_y = screen_size[1] // 4
        score_y = screen_size[1] // 3
        base_y = screen_size[1] // 2
        button_spacing = screen_size[1] // 12
        resume_x = screen_size[0] - screen_size[0] // 6
        resume_y = screen_size[1] // 14
        quit_x = screen_size[0] - screen_size[0] // 14
        quit_y = screen_size[1] // 14

        # Prepare menu buttons with toggle states
        music_text = "[UNMUTE MUSIC]" if not settings.music else "[MUTE MUSIC]"
        sounds_text = "[UNMUTE SOUND]" if not settings.sounds else "[MUTE SOUND]"
        menu_buttons = [
            ("[ABORT GAME]", self.parent.abort_game),
            ("[FULLSCREEN F11]", self.parent.toggle_fullscreen),
            ("[RESET BEST SCORE]", self.parent.score_system.reset_best_score),
            (music_text, self.parent.toggle_music),
            (sounds_text, self.parent.toggle_sounds)
        ]

        # Draw the title and best score
        self.draw_text("GAME PAUSED", (center_x, title_y))
        self.draw_text(f"BEST SCORE: {best_score}", (center_x, score_y))

        # Draw each button in the menu
        for i, (text, callback) in enumerate(menu_buttons):
            button_y = base_y + (button_spacing * i)
            self.draw_button(center_x, button_y, text, callback, events)

        # Resume button (ESC)
        self.draw_button(
            resume_x, 
            resume_y,
            "[ESC]", 
            self.parent.resume_game, 
            events,
        )

        # Quit button (X)
        self.draw_button(
            quit_x, 
            quit_y,
            "[X]", 
            self.parent.quit_game, 
            events, 
            Colors.RED
        )
