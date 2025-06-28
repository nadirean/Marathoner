"""
A module that contains the Player class.
"""

from typing import List, Tuple

import pygame

from resource_path import resource_path
from modules.util.constants import (
    PLAYER_SIZE_MULTIPLIER,
    PLAYER_POSITION_X_DIVISOR,
    JUMP_STRENGTH_FORMULA,
    GRAVITY_INCREASE,
    ANIMATION_SPEED,
    GROUND_OFFSET_RATIO,
    JUMP_VOLUME)


class Player(pygame.sprite.Sprite):
    """
    A class representing the game player character.

    This class manages the player sprite including animations, movement,
    physics (gravity), input handling, and collision detection.

    Attributes:
        screen_size: Current screen dimensions
        run_index: Current frame index for running animation
        jump_index: Current frame index for jumping animation
        player_run: List of running animation frame surfaces
        player_jump: List of jumping animation frame surfaces
        image: Current player image surface
        mask: Collision mask for pixel-perfect collision detection
        rect: Rectangle defining player position and bounds
        gravity: Current gravity/velocity value
        jump_sound: Sound effect played when jumping
    """

    def __init__(self, screen_size: Tuple[int, int]) -> None:
        """
        Initialize the player.

        Args:
            screen_size: Current screen size as (width, height)
        """
        super().__init__()
        self.screen_size = screen_size
        self.run_index: float = 0.0
        self.jump_index: float = 0.0
        self.gravity: int = 0

        self.player_run: List[pygame.Surface] = []
        self.player_jump: List[pygame.Surface] = []

        self.load()

    def load(self) -> None:
        """Load player sprites, sounds, and set initial position."""
        self._load_animation_frames()
        self._scale_sprites()
        self._setup_initial_state()
        self._load_audio()

    def _load_animation_frames(self) -> None:
        """Load all animation frame images from files."""
        run_frames = [
            pygame.image.load(resource_path('images/run1.png')).convert_alpha(),
            pygame.image.load(resource_path('images/run2.png')).convert_alpha(),
            pygame.image.load(resource_path('images/run3.png')).convert_alpha()
        ]

        jump_frames = [
            pygame.image.load(resource_path('images/jump1.png')).convert_alpha(),
            pygame.image.load(resource_path('images/jump2.png')).convert_alpha()
        ]

        self.player_run = run_frames
        self.player_jump = jump_frames

    def _scale_sprites(self) -> None:
        """Scale all sprite frames based on screen size."""
        scale_multiplier = self.screen_size[1] * PLAYER_SIZE_MULTIPLIER

        # Scale running frames
        self.player_run = [
            pygame.transform.scale(
                img, 
                (int(img.get_width() * scale_multiplier), 
                 int(img.get_height() * scale_multiplier))
            ) for img in self.player_run
        ]

        # Scale jumping frames
        self.player_jump = [
            pygame.transform.scale(
                img, 
                (int(img.get_width() * scale_multiplier), 
                 int(img.get_height() * scale_multiplier))
            ) for img in self.player_jump
        ]

    def _setup_initial_state(self) -> None:
        """Set up initial player position and collision detection."""
        initial_x = self.screen_size[0] // PLAYER_POSITION_X_DIVISOR
        initial_y = self.screen_size[1] - self.screen_size[1] // 2

        self.image = self.player_run[0]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(midbottom=(initial_x, initial_y))

    def _load_audio(self) -> None:
        """Load and configure jump sound effect."""
        self.jump_sound = pygame.mixer.Sound(resource_path('audio/jump.ogg'))
        self.jump_sound.set_volume(JUMP_VOLUME)

    def _get_ground_level(self) -> int:
        """
        Calculate the ground level position.

        Returns:
            Y coordinate of the ground level
        """
        return self.screen_size[1] - int(self.screen_size[1] / GROUND_OFFSET_RATIO)

    def _is_on_ground(self) -> bool:
        """
        Check if the player is on the ground.

        Returns:
            True if player is on ground level, False if airborne
        """
        return self.rect.bottom >= self._get_ground_level()

    def player_input(self, channel: pygame.mixer.Channel) -> None:
        """
        Handle player input for jumping.

        Args:
            channel: Audio channel for playing jump sound
        """
        keys = pygame.key.get_pressed()

        # Jump only if on ground and space key is pressed
        if keys[pygame.K_SPACE] and self._is_on_ground():
            # Calculate jump strength relative to screen size using formula
            jump_strength = (JUMP_STRENGTH_FORMULA[0] * self.screen_size[1] + 
                           JUMP_STRENGTH_FORMULA[1])
            self.gravity = int(jump_strength)
            channel.play(self.jump_sound)

    def apply_gravity(self) -> None:
        """Apply gravity physics to the player."""
        self.gravity += GRAVITY_INCREASE
        self.rect.y += self.gravity

        # Keep player on ground level
        ground_level = self._get_ground_level()
        if self.rect.bottom >= ground_level:
            self.rect.bottom = ground_level

    def animation_state(self) -> None:
        """Update player animation based on current state (jumping or running)."""
        if not self._is_on_ground():
            self._update_jump_animation()
        else:
            self._update_run_animation()

    def _update_jump_animation(self) -> None:
        """Update jumping animation frames."""
        self.jump_index += ANIMATION_SPEED
        if self.jump_index >= len(self.player_jump):
            self.jump_index = 0
        self.image = self.player_jump[int(self.jump_index)]

    def _update_run_animation(self) -> None:
        """Update running animation frames."""
        self.run_index += ANIMATION_SPEED
        if self.run_index >= len(self.player_run):
            self.run_index = 0
        self.image = self.player_run[int(self.run_index)]

    def update(self, channel: pygame.mixer.Channel) -> None:
        """
        Update player state including input, physics, and animation.

        Args:
            channel: Audio channel for playing sounds
        """
        self.player_input(channel)
        self.apply_gravity()
        self.animation_state()

    def update_screen_size(self, screen_size: Tuple[int, int]) -> None:
        """
        Update player for new screen size.

        This method is called when the game window is resized.
        It reloads and rescales all player sprites and repositions the player.

        Args:
            screen_size: New screen size as (width, height)
        """
        self.screen_size = screen_size
        self.load()
