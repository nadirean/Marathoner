"""
A module that contains the BaseScreen class for common screen functionality.
"""

from typing import List, Tuple, Callable, TYPE_CHECKING

import pygame

from modules.components.button import Button
from modules.util.constants import Colors

if TYPE_CHECKING:
    from modules.Game import Game


class BaseScreen:
    """
    A base class for all game screens providing common functionality.
    
    This class provides shared functionality for all game screens including
    button rendering, text rendering, and basic screen management.
    
    Attributes:
        screen: Surface to draw on
        game_font: Font for rendering text
        parent: Reference to the main Game instance
    """
    def __init__(
        self, 
        screen: pygame.Surface, 
        game_font: pygame.font.Font, 
        parent: 'Game'
    ) -> None:
        """
        Initialize the base screen.
        
        Args:
            screen: Surface to draw on
            game_font: Font for rendering text
            parent: Reference to the main Game instance
        """
        self.parent = parent
        self.screen = screen
        self.game_font = game_font

    def draw_button(
        self, 
        x: int, 
        y: int, 
        text: str, 
        callback: Callable[[], None], 
        events: List[pygame.event.Event], 
        hover_colour: str = Colors.GRAY
    ) -> None:
        """
        Draw an interactive button on the screen.

        Args:
            x: X coordinate of button center
            y: Y coordinate of button center
            text: Text to display on button
            callback: Function to call when button is clicked
            events: List of pygame events to process
            hover_colour: Button text color when hovered (default: gray)
        """
        Button(x, y, self.game_font, text, self.screen, callback, events, hover_colour).process()

    def draw_text(
        self, 
        text: str, 
        center: Tuple[int, int], 
        color: str = Colors.WHITE
    ) -> None:
        """
        Draw text on the screen at the specified position.

        Args:
            text: Text to display
            center: Center position as (x, y) coordinates
            color: Text color (default: white)
        """
        rendered_text = self.game_font.render(text, False, color)
        text_rect = rendered_text.get_rect(center=center)
        self.screen.blit(rendered_text, text_rect)
