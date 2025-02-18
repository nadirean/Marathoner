"""
A module that contains the Obstacle class.
"""

from random import randint

import pygame

from resource_path import resource_path


class Obstacle(pygame.sprite.Sprite):
    """
    A class representing an obstacle.
    
    Attributes:
    screen_size (tuple): The size of the screen.
    type (str): The type of the obstacle.
    image (pygame.Surface): The image of the obstacle.
    mask (pygame.mask.Mask): The mask of the obstacle.
    rect (pygame.Rect): The rectangle of the obstacle.
    
    Methods:
    load: Load the obstacle.
    update: Update the obstacle.
    update_screen_size: Update the screen size of the obstacle.
    """
    def __init__(self, obstacle_type, screen_size):
        super().__init__()

        self.screen_size = screen_size
        self.type = obstacle_type
        self.load()

    def load(self, initial=True):
        """
        Load the obstacle.
        """
        image_path = 'images/stone1.png' if self.type == 'stone1' else 'images/stone2.png'
        image = pygame.image.load(resource_path(image_path)).convert_alpha()
        y_pos = self.screen_size[1] * (0.74 if self.type == 'stone1' else 0.49)

        multiplier = self.screen_size[1] * 0.0015

        self.image = pygame.transform.scale(image,
                                            (image.get_width() * multiplier,
                                             image.get_height() * multiplier))
        self.mask = pygame.mask.from_surface(self.image)

        if initial:
            self.rect = self.image.get_rect(midbottom=(
                randint(self.screen_size[0],
                        self.screen_size[0] + self.screen_size[0] // 4), y_pos))
        else:
            self.rect = self.image.get_rect(midbottom=(self.rect.x, y_pos))

    def update(self):
        """
        Update the obstacle.
        If the obstacle is out of the screen, it will be killed.
        """
        self.rect.x -= 10
        if self.rect.x <= - (self.screen_size[0] + 50):
            self.kill()

    def update_screen_size(self, screen_size):
        """
        Update the screen size of the obstacle.

        Parameters:
        screen_size (tuple): The size of the screen.
        """
        self.screen_size = screen_size
        self.load(False)
