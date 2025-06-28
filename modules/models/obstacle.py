"""
A module that contains the Obstacle class.
"""

from random import randint
from typing import Tuple

import pygame

from resource_path import resource_path
from modules.util.constants import (
    OBSTACLE_SIZE_MULTIPLIER, 
    OBSTACLE_SPAWN_OFFSET_RATIO, 
    OBSTACLE_SPEED, STONE1_Y_RATIO, 
    STONE2_Y_RATIO)


class Obstacle(pygame.sprite.Sprite):
    """
    A class representing a game obstacle.

    This class manages obstacle sprites that the player must avoid.
    It handles loading, positioning, scaling, and movement of obstacles.

    Attributes:
        screen_size: The current screen dimensions
        obstacle_type: Type of obstacle ('stone1' or 'stone2')
        image: The scaled obstacle image surface
        mask: Collision mask for pixel-perfect collision detection
        rect: Rectangle defining obstacle position and bounds
    """
    def __init__(self, obstacle_type: str, screen_size: Tuple[int, int]) -> None:
        """
        Initialize a new obstacle.

        Args:
            obstacle_type: Type of obstacle ('stone1' or 'stone2')
            screen_size: Current screen size as (width, height)
        """
        super().__init__()
        self.screen_size = screen_size
        self.obstacle_type = obstacle_type
        self.load()

    def load(self, initial: bool = True) -> None:
        """
        Load and scale the obstacle image, set up collision mask and position.

        Args:
            initial: If True, position obstacle off-screen. If False, maintain current x position.
        """
        # Load appropriate image based on obstacle type
        image_path = self._get_image_path()
        image = pygame.image.load(resource_path(image_path)).convert_alpha()

        # Calculate position and scale
        y_position = self._calculate_y_position()
        scale_multiplier = self.screen_size[1] * OBSTACLE_SIZE_MULTIPLIER

        # Scale image relative to screen size
        scaled_width = int(image.get_width() * scale_multiplier)
        scaled_height = int(image.get_height() * scale_multiplier)
        self.image = pygame.transform.scale(image, (scaled_width, scaled_height))

        # Create collision mask for pixel-perfect collision detection
        self.mask = pygame.mask.from_surface(self.image)

        # Position obstacle
        if initial:
            x_position = self._calculate_initial_x_position()
            self.rect = self.image.get_rect(midbottom=(x_position, y_position))
        else:
            # Maintain current x position when updating (e.g., during screen resize)
            self.rect = self.image.get_rect(midbottom=(self.rect.x, y_position))

    def _get_image_path(self) -> str:
        """
        Get the image path based on obstacle type.
        
        Returns:
            Path to the obstacle image file
        """
        return 'images/stone1.png' if self.obstacle_type == 'stone1' else 'images/stone2.png'

    def _calculate_y_position(self) -> float:
        """
        Calculate the Y position based on obstacle type.
        
        Returns:
            Y coordinate for obstacle placement
        """
        if self.obstacle_type == 'stone1':
            return self.screen_size[1] * STONE1_Y_RATIO
        else:
            return self.screen_size[1] * STONE2_Y_RATIO

    def _calculate_initial_x_position(self) -> int:
        """
        Calculate initial X position off-screen for spawning.
        
        Returns:
            X coordinate for initial obstacle placement
        """
        spawn_min = self.screen_size[0]
        spawn_max = self.screen_size[0] + int(self.screen_size[0] * OBSTACLE_SPAWN_OFFSET_RATIO)
        return randint(spawn_min, spawn_max)

    def update(self) -> None:
        """
        Update obstacle position and remove if off-screen.
        
        Moves the obstacle left by a fixed speed and removes it when
        it goes completely off the left side of the screen.
        """
        self.rect.x -= OBSTACLE_SPEED
        
        # Remove obstacle when it's completely off-screen (with buffer)
        if self.rect.x <= -(self.screen_size[0] + 50):
            self.kill()

    def update_screen_size(self, screen_size: Tuple[int, int]) -> None:
        """
        Update obstacle for new screen size.
        
        This method is called when the game window is resized.
        It rescales the obstacle image and adjusts its position accordingly.
        
        Args:
            screen_size: New screen size as (width, height)
        """
        self.screen_size = screen_size
        self.load(initial=False)
