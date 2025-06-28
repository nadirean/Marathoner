"""
A module containing constants used throughout the game.
"""

import os
from enum import Enum
from typing import Final
from pathlib import Path

# Game constants
GAME_FPS: Final[int] = 60
OBSTACLE_SPAWN_INTERVAL: Final[int] = 1500  # milliseconds
OBSTACLE_SPEED: Final[int] = 10
GRAVITY_INCREASE: Final[int] = 1
ANIMATION_SPEED: Final[float] = 0.1

# Screen constants
DEFAULT_ASPECT_RATIO: Final[float] = 16/9
MIN_ASPECT_RATIO: Final[float] = 1.6
MAX_ASPECT_RATIO: Final[float] = 1.9
SCREEN_SCALE_FACTOR: Final[float] = 1.5

# Audio constants
MUSIC_VOLUME: Final[float] = 0.5
SOUND_VOLUME: Final[float] = 1.0
JUMP_VOLUME: Final[float] = 0.5

# UI constants
FONT_SIZE_DIVISOR: Final[int] = 70
LARGE_FONT_SIZE_DIVISOR: Final[int] = 50
SCORE_POSITION_Y_DIVISOR: Final[int] = 14
PLAYER_POSITION_X_DIVISOR: Final[int] = 10
GROUND_HEIGHT_RATIO: Final[float] = 0.6

# Player constants
JUMP_STRENGTH_FORMULA: Final[tuple[float, float]] = (-0.01403, -5.978)  # mx + b for gravity calculation
GROUND_OFFSET_RATIO: Final[float] = 3.5
PLAYER_SIZE_MULTIPLIER: Final[float] = 0.0015

# Obstacle constants
STONE1_Y_RATIO: Final[float] = 0.74
STONE2_Y_RATIO: Final[float] = 0.49
OBSTACLE_SIZE_MULTIPLIER: Final[float] = 0.0015
OBSTACLE_SPAWN_OFFSET_RATIO: Final[float] = 0.25

# Game timing constants
GAME_OVER_COOLDOWN: Final[int] = 500  # milliseconds
RESIZE_COOLDOWN: Final[int] = 1000  # milliseconds

# File paths and URLs
GITHUB_URL: Final[str] = "https://github.com/f4rys"
SETTINGS_PATH: Final[Path] = Path.home() / 'Marathoner' / 'settings.ini'
BEST_SCORE_PATH: Final[str] = os.path.join(os.path.expanduser("~"), 'Marathoner', 'best_score.txt')


# Colors
class Colors:
    """Color constants for the game."""
    WHITE: Final[str] = "White"
    RED: Final[str] = "Red"
    GRAY: Final[str] = "Gray"


# Settings
class SettingType(Enum):
    """Enumeration for different types of settings."""
    MUSIC = "Music"
    SOUNDS = "Sounds"


# Default settings configuration
DEFAULT_SETTINGS: Final[dict[str, dict[str, int]]] = {
    'GENERAL': {
        SettingType.MUSIC.value: 1,
        SettingType.SOUNDS.value: 1
    }
}
