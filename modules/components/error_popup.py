"""
A module that contains the ErrorPopup class for displaying error messages.
"""

from typing import Tuple, Optional

import pygame

from modules.util.constants import Colors, LARGE_FONT_SIZE_DIVISOR, FONT_SIZE_DIVISOR
from resource_path import resource_path


class ErrorPopup:
    """
    A class for displaying error popups with cached resources for performance.

    This class manages error message display with proper resource caching
    to avoid reloading fonts and images every time an error is shown.

    Attributes:
        screen_size: Current screen dimensions
        screen: Surface to draw the popup on
        _large_font: Cached large font for error title
        _small_font: Cached small font for error message
        _blur_surface: Cached blur background surface
    """
    def __init__(self, screen: pygame.Surface, screen_size: Tuple[int, int]) -> None:
        """
        Initialize the error popup with cached resources.

        Args:
            screen: Surface to draw the popup on
            screen_size: Current screen size as (width, height)
        """
        self.screen_size = screen_size
        self.screen = screen

        # Cache fonts and surfaces for performance
        self._large_font: Optional[pygame.font.Font] = None
        self._small_font: Optional[pygame.font.Font] = None
        self._blur_surface: Optional[pygame.Surface] = None

        self._initialize_resources()

    def _initialize_resources(self) -> None:
        """Initialize and cache fonts and background surface."""
        try:
            font_size_large = (self.screen_size[0] + self.screen_size[1]) // LARGE_FONT_SIZE_DIVISOR
            font_size_small = (self.screen_size[0] + self.screen_size[1]) // FONT_SIZE_DIVISOR

            self._large_font = pygame.font.Font(resource_path('font/pixeled.ttf'), font_size_large)
            self._small_font = pygame.font.Font(resource_path('font/pixeled.ttf'), font_size_small)
            self._blur_surface = pygame.image.load(resource_path('images/blur.jpg')).convert_alpha()

        except (pygame.error, FileNotFoundError) as e:
            print(f"Warning: Could not load error popup resources: {e}")
            # Use default font as fallback
            self._large_font = pygame.font.Font(None, 36)
            self._small_font = pygame.font.Font(None, 24)

    def update_screen_size(self, screen_size: Tuple[int, int]) -> None:
        """
        Update popup for new screen size.

        Args:
            screen_size: New screen size as (width, height)
        """
        self.screen_size = screen_size
        self._initialize_resources()

    def display_error(self, message: str) -> None:
        """
        Display an error message popup and wait for user input.

        Args:
            message: Error message to display
        """
        if not self._large_font or not self._small_font:
            print(f"Error: {message}")  # Fallback to console output
            return

        # Create a copy of blur surface to avoid modifying the original
        popup_surface = self._blur_surface.copy() if self._blur_surface else pygame.Surface(self.screen_size)

        # Render text surfaces
        error_title = self._large_font.render("ERROR", True, Colors.RED)
        error_message = self._small_font.render(message, True, Colors.WHITE)
        continue_message = self._small_font.render("Press SPACE to continue", True, Colors.WHITE)

        # Calculate positions
        title_rect = error_title.get_rect(center=(
            self.screen_size[0] // 2, 
            self.screen_size[1] // 2.5
        ))
        message_rect = error_message.get_rect(center=(
            self.screen_size[0] // 2, 
            self.screen_size[1] // 2
        ))
        continue_rect = continue_message.get_rect(center=(
            self.screen_size[0] // 2, 
            int(self.screen_size[1] // 1.1)
        ))

        # Blit text onto popup surface
        popup_surface.blit(error_title, title_rect)
        popup_surface.blit(error_message, message_rect)
        popup_surface.blit(continue_message, continue_rect)

        # Display popup
        self.screen.blit(pygame.transform.scale(popup_surface, self.screen_size), (0, 0))
        pygame.display.update()

        # Wait for user input
        self._wait_for_space_key()

    def _wait_for_space_key(self) -> None:
        """Wait for the user to press the SPACE key to dismiss the popup."""
        waiting = True
        clock = pygame.time.Clock()

        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    waiting = False

            # Limit CPU usage while waiting
            clock.tick(30)
