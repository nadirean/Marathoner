import os
import sys
import webbrowser
from random import choice
from typing import List, Tuple

import pygame

from modules.models.obstacle import Obstacle
from modules.models.player import Player
from modules.screens.game_over_screen import GameOverScreen
from modules.screens.pause_game_screen import PauseGameScreen
from modules.screens.start_game_screen import StartGameScreen
from modules.screens.game_screen import GameScreen
from modules.util.score_system import ScoreSystem
from modules.util.settings import Settings
from modules.util.constants import (
    SCREEN_SCALE_FACTOR,
    OBSTACLE_SPAWN_INTERVAL,
    GAME_FPS,
    GAME_OVER_COOLDOWN,
    RESIZE_COOLDOWN,
    MIN_ASPECT_RATIO,
    MAX_ASPECT_RATIO,
    MUSIC_VOLUME,
    SOUND_VOLUME,
    GITHUB_URL,
    FONT_SIZE_DIVISOR,
    SettingType
)
from resource_path import resource_path


class Game:
    """
    Main game class that manages the entire game state and loop.
    This class initializes all game components, handles events, manages game state,
    and renders the game screens.

    Attributes:
        settings: Game settings instance
        screen: Pygame display surface
        monitor_size: List containing the width and height of the monitor
        original_screen_size: Tuple of the original screen width and height
        screen_size: Tuple of the current screen width and height
        aspect_ratio: Aspect ratio of the screen
        fullscreen: Boolean indicating if the game is in fullscreen mode
        player: Group containing the player sprite
        obstacle_group: Group containing all obstacles
        obstacle_timer: Timer event for spawning obstacles
        sky_surface: Surface for the sky background
        ground_surface: Surface for the ground
        vignette_surface: Surface for the vignette overlay
        blur_surface: Surface for the blur effect
        game_over_sound: Sound effect for game over
        theme_sound: Background music sound
        channel1: Pygame mixer channel for music
        channel2: Pygame mixer channel for sound effects
        clock: Pygame clock for controlling frame rate
        game_font: Font used for rendering text
        score_system: ScoreSystem instance for managing scores
        start_time: Timestamp when the game started
        score: Current game score
        current_screen: Current screen state (0: start/game over, 1: game, 2: pause)
        pause_time: Timestamp when the game was paused
        resize_time: Timestamp when the screen was resized
        last_game_over_time: Timestamp of the last game over event
        game_active: Boolean indicating if the game is currently active
        start_game_screen: Instance of StartGameScreen
        game_over_screen: Instance of GameOverScreen
        pause_game_screen: Instance of PauseGameScreen
        game_screen: Instance of GameScreen
        _cached_best_score: Cached best score to avoid file I/O every frame
        _score_cache_dirty: Boolean indicating if the best score cache is dirty
    """
    def __init__(self) -> None:
        """Initialize the game with all required components and settings."""
        pygame.init()

        self._ensure_game_directory()
        self._initialize_settings()
        self._setup_display()
        self._initialize_game_objects()
        self._setup_audio()
        self._initialize_ui()
        self._initialize_screens()

        # Cache best score to avoid file I/O every frame
        self._cached_best_score: int = self.score_system.load_best_score()
        self._score_cache_dirty: bool = False

    def _ensure_game_directory(self) -> None:
        """Create game directory if it doesn't exist."""
        try:
            game_dir = os.path.expanduser("~") + '/Marathoner'
            os.makedirs(game_dir, exist_ok=True)
        except OSError as e:
            print(f"Warning: Could not create game directory: {e}")

    def _initialize_settings(self) -> None:
        """Initialize game settings."""
        self.settings = Settings()

    def _setup_display(self) -> None:
        """Setup display and window properties."""
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        info = pygame.display.Info()
        self.monitor_size: List[int] = [info.current_w, info.current_h]

        self.original_screen_size: Tuple[int, int] = (
            int(info.current_w / SCREEN_SCALE_FACTOR), 
            int(info.current_h / SCREEN_SCALE_FACTOR)
        )
        self.screen_size: Tuple[int, int] = self.original_screen_size
        self.aspect_ratio: float = self.screen_size[0] / self.screen_size[1]

        self.screen = pygame.display.set_mode(self.screen_size, pygame.RESIZABLE)
        pygame.display.set_caption("Marathoner")
        pygame.display.set_icon(pygame.image.load(resource_path('images/icon.ico')))

        # Fullscreen flag
        self.fullscreen: bool = False

    def _initialize_game_objects(self) -> None:
        """Initialize player, obstacles, and sprites."""
        # Player
        self.player = pygame.sprite.GroupSingle()
        self.player.add(Player(self.screen_size))

        # Obstacles
        self.obstacle_group = pygame.sprite.Group()
        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer, OBSTACLE_SPAWN_INTERVAL)

        # Game surfaces
        self.sky_surface = pygame.image.load(resource_path('images/sky.jpg')).convert()
        self.ground_surface = pygame.image.load(resource_path('images/ground.png')).convert_alpha()
        self.vignette_surface = pygame.image.load(resource_path('images/vignette.png')).convert_alpha()
        self.blur_surface = pygame.image.load(resource_path('images/blur.jpg')).convert_alpha()

    def _setup_audio(self) -> None:
        """Setup audio channels and sounds."""
        self.game_over_sound = pygame.mixer.Sound(resource_path('audio/game_over.ogg'))
        self.theme_sound = pygame.mixer.Sound(resource_path('audio/theme.ogg'))

        self.channel1 = pygame.mixer.Channel(0)  # Music channel
        self.channel2 = pygame.mixer.Channel(1)  # Sound effects channel

        self.game_over_sound.set_volume(SOUND_VOLUME)
        self.theme_sound.set_volume(SOUND_VOLUME)

        self.channel2.set_volume(SOUND_VOLUME if self.settings.sounds else 0)
        self.channel1.set_volume(MUSIC_VOLUME if self.settings.music else 0)

        self.channel1.play(self.theme_sound, loops=-1)

    def _initialize_ui(self) -> None:
        """Initialize UI components."""
        self.clock = pygame.time.Clock()
        self.game_font = pygame.font.Font(
            resource_path('font/pixeled.ttf'), 
            (self.screen_size[0] + self.screen_size[1]) // FONT_SIZE_DIVISOR
        )
        self.score_system = ScoreSystem(self.screen_size)

        # Game state variables
        self.start_time: int = 0
        self.score: int = 0
        self.current_screen: int = 0  # 0: start/game over, 1: game, 2: pause
        self.pause_time: int = 0
        self.resize_time: int = 0
        self.last_game_over_time: int = 0
        self.game_active: bool = False

    def _initialize_screens(self) -> None:
        """Initialize all game screens."""
        self.start_game_screen = StartGameScreen(self.screen, self.game_font, self)
        self.game_over_screen = GameOverScreen(self.screen, self.game_font, self)
        self.pause_game_screen = PauseGameScreen(self.screen, self.game_font, self)
        self.game_screen = GameScreen(self.screen, self.game_font, self)

    def get_best_score(self) -> int:
        """
        Get the cached best score, loading from file only when necessary.
        
        Returns:
            Current best score
        """
        if self._score_cache_dirty:
            self._cached_best_score = self.score_system.load_best_score()
            self._score_cache_dirty = False
        return self._cached_best_score

    def invalidate_score_cache(self) -> None:
        """Mark the score cache as dirty so it will be reloaded next time."""
        self._score_cache_dirty = True

    def toggle_fullscreen(self) -> None:
        """Toggle between fullscreen and windowed mode."""
        if not self.fullscreen:
            self.screen = pygame.display.set_mode(self.monitor_size, pygame.RESIZABLE)
            self.handle_resize(self.monitor_size[0], self.monitor_size[1])
            self.fullscreen = True
        else:
            self.screen = pygame.display.set_mode(
                (self.original_screen_size[0], self.original_screen_size[1]), 
                pygame.RESIZABLE
            )
            self.handle_resize(self.original_screen_size[0], self.original_screen_size[1])
            self.fullscreen = False

    def toggle_music(self) -> None:
        """Toggle background music on/off."""
        self.settings.update_settings(not self.settings.music, SettingType.MUSIC)
        self.channel1.set_volume(MUSIC_VOLUME if self.settings.music else 0)

    def toggle_sounds(self) -> None:
        """Toggle sound effects on/off."""
        self.settings.update_settings(not self.settings.sounds, SettingType.SOUNDS)
        self.channel2.set_volume(SOUND_VOLUME if self.settings.sounds else 0)

    def start_game(self) -> None:
        """Start a new game."""
        self.current_screen = 1
        self.start_time = int(pygame.time.get_ticks() / 1000)

    def pause_game(self) -> None:
        """Pause the current game."""
        self.pause_time = pygame.time.get_ticks()
        self.current_screen = 2

    def resume_game(self) -> None:
        """Resume the paused game."""
        self.current_screen = 1
        pause_duration = pygame.time.get_ticks() - self.pause_time
        self.start_time += int(pause_duration / 1000)
        self.pause_time = 0

    def abort_game(self) -> None:
        """Abort the current game and return to start screen."""
        self.current_screen = 0
        self.score = 0
        self.obstacle_group.empty()

    def quit_game(self) -> None:
        """Quit the game completely."""
        pygame.quit()
        sys.exit()

    def collision_sprite(self) -> int:
        """
        Check for collisions between player and obstacles.

        Returns:
            0 if collision detected (game over), 1 if no collision
        """
        if pygame.sprite.spritecollideany(self.player.sprite, self.obstacle_group, pygame.sprite.collide_mask):
            self.obstacle_group.empty()
            self.channel2.play(self.game_over_sound)

            # Update best score and invalidate cache if necessary
            if self.score_system.save_best_score(self.score):
                self.invalidate_score_cache()

            self.last_game_over_time = pygame.time.get_ticks()
            return 0
        return 1

    def open_github(self) -> None:
        """Open the developer's GitHub page in default browser."""
        webbrowser.open(GITHUB_URL, new=0, autoraise=True)

    def handle_resize(self, w: int, h: int) -> None:
        """
        Handle window resize events.

        Args:
            w: New window width
            h: New window height
        """
        # Pause game during resize
        if self.current_screen == 1:
            self.current_screen = 2
            self.pause_time = pygame.time.get_ticks()
            self.resize_time = pygame.time.get_ticks()

        # Maintain aspect ratio constraints
        new_aspect_ratio = w / h
        if new_aspect_ratio < MIN_ASPECT_RATIO or new_aspect_ratio > MAX_ASPECT_RATIO:
            new_width = w
            new_height = int(new_width / self.aspect_ratio)
            self.screen_size = (new_width, new_height)
        else:
            self.screen_size = (w, h)

        self._update_ui_for_resize()
        self._update_game_objects_for_resize()

    def _update_ui_for_resize(self) -> None:
        """Update UI elements after screen resize."""
        self.game_font = pygame.font.Font(
            resource_path('font/pixeled.ttf'), 
            (self.screen_size[0] + self.screen_size[1]) // FONT_SIZE_DIVISOR
        )
        self.screen = pygame.display.set_mode(self.screen_size, pygame.RESIZABLE)
        self.score_system.update_screen_size(self.screen_size)

    def _update_game_objects_for_resize(self) -> None:
        """Update game objects after screen resize."""
        self.player.sprite.update_screen_size(self.screen_size)
        for obstacle in self.obstacle_group:
            obstacle.update_screen_size(self.screen_size)

    def run(self) -> None:
        """Main game loop."""
        while True:
            # Get cached best score
            best_score = self.get_best_score()

            # Load events
            events = pygame.event.get()

            self._handle_events(events)
            self._render_current_screen(events, best_score)

            pygame.display.update()
            self.clock.tick(GAME_FPS)

    def _handle_events(self, events: List[pygame.event.Event]) -> None:
        """
        Handle all pygame events.

        Args:
            events: List of pygame events to process
        """
        for event in events:
            if event.type == pygame.QUIT:
                self.quit_game()

            elif event.type == pygame.KEYDOWN:
                self._handle_keydown_events(event)

            elif event.type == self.obstacle_timer:
                self._handle_obstacle_spawn()

            elif event.type == pygame.VIDEORESIZE:
                self.handle_resize(event.w, event.h)

    def _handle_keydown_events(self, event: pygame.event.Event) -> None:
        """
        Handle keyboard input events.

        Args:
            event: Pygame keydown event
        """
        if event.key == pygame.K_SPACE and self.current_screen == 0:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_game_over_time > GAME_OVER_COOLDOWN:
                self.start_game()

        elif event.key == pygame.K_ESCAPE:
            if self.current_screen == 1:
                self.pause_game()
            elif self.current_screen == 2:
                self.resume_game()

        elif event.key == pygame.K_F11:
            self.toggle_fullscreen()

    def _handle_obstacle_spawn(self) -> None:
        """Handle spawning new obstacles during gameplay."""
        if (self.current_screen == 1 and 
            pygame.time.get_ticks() - self.resize_time > RESIZE_COOLDOWN):
            self.resize_time = 0
            obstacle_type = choice(['stone1', 'stone1', 'stone2'])  # stone1 is more common
            self.obstacle_group.add(Obstacle(obstacle_type, self.screen_size))

    def _render_current_screen(self, events: List[pygame.event.Event], best_score: int) -> None:
        """
        Render the current game screen.

        Args:
            events: List of pygame events
            best_score: Current best score
        """
        if self.current_screen == 0:
            if self.score != 0:
                self.game_over_screen.frame(self.screen_size, events, self.score, best_score)
            else:
                self.start_game_screen.frame(self.screen_size, events, best_score)

        elif self.current_screen == 1:
            self.game_screen.frame(self.screen_size, events)

        elif self.current_screen == 2:
            self.pause_game_screen.frame(self.screen_size, events, best_score, self.settings)
