import os
from typing import Optional

import pygame

from modules.util.constants import BEST_SCORE_PATH


class ScoreSystem:
    """
    Manages game scoring functionality including display, persistence, and best score tracking.
    This class handles the current score display, saving and loading the best score,
    and ensuring the score directory exists for storing best scores.
    Attributes:
        screen_size: Tuple containing (width, height) of the game screen
        x: Horizontal position for score display
        y: Vertical position for score display
        _score_surface: Optional Pygame Surface for rendering the score
        _score_rectangle: Optional Pygame Rect for positioning the score on the screen
    """
    def __init__(self, screen_size: tuple[int, int]) -> None:
        """
        Initialize the ScoreSystem.

        Args:
            screen_size: Tuple containing (width, height) of the game screen
        """
        self._score_surface: Optional[pygame.Surface] = None
        self._score_rectangle: Optional[pygame.Rect] = None
        self.update_screen_size(screen_size)

        os.makedirs(os.path.dirname(BEST_SCORE_PATH), exist_ok=True)

    def load_best_score(self) -> int:
        """
        Load the best score from the file.

        Returns:
            The best score as an integer, or 0 if file doesn't exist or is invalid
        """
        try:
            with open(BEST_SCORE_PATH, 'r', encoding='utf-8') as file:
                score = file.read().strip()
                return int(score) if score.isdigit() else 0
        except (FileNotFoundError, ValueError, OSError):
            return 0

    def save_best_score(self, score: int) -> bool:
        """
        Save the score if it's better than the current best score.

        Args:
            score: The score to potentially save

        Returns:
            True if the score was saved (new best), False otherwise
        """
        if score <= self.load_best_score():
            return False

        try:
            with open(BEST_SCORE_PATH, 'w', encoding='utf-8') as file:
                file.write(str(score))
            return True
        except (FileNotFoundError, ValueError, OSError) as e:
            print(f"Error saving best score: {e}")
            return False

    def display_score(self, game_font: pygame.font.Font, start_time: int, screen: pygame.Surface) -> int:
        """
        Display the current score on the screen.

        Args:
            game_font: Font to use for rendering the score
            start_time: Game start time in seconds
            screen: Surface to draw the score on

        Returns:
            Current score (time elapsed in seconds)
        """
        # Calculate the current score based on elapsed time
        current_score = int(pygame.time.get_ticks() / 1000) - start_time
        score_text = f"{current_score} s"

        # Render the score
        self._score_surface = game_font.render(score_text, False, 'White')
        self._score_rectangle = self._score_surface.get_rect(center=(self.x, self.y))
        screen.blit(self._score_surface, self._score_rectangle)

        return current_score

    def update_screen_size(self, screen_size: tuple[int, int]) -> None:
        """
        Update the screen size and recalculate score position.

        Args:
            screen_size: New screen size as (width, height)
        """
        self.screen_size = screen_size
        self.x = screen_size[0] // 2
        self.y = screen_size[1] // 14

        if self._score_rectangle and self._score_surface:
            self._score_rectangle = self._score_surface.get_rect(center=(self.x, self.y))

    def reset_best_score(self) -> bool:
        """
        Reset the best score to 0.

        Returns:
            True if reset was successful, False otherwise
        """
        try:
            with open(BEST_SCORE_PATH, 'w', encoding='utf-8') as file:
                file.write('0')
            return True
        except OSError as e:
            print(f"Error resetting best score: {e}")
            return False
