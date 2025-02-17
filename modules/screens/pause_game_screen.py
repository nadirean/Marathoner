import pygame

from modules.screens.base_screen import BaseScreen
from resource_path import resource_path

class PauseGameScreen(BaseScreen):
    def __init__(self, screen, game_font, parent):
        super().__init__(screen, game_font, parent)
        self.blur_surface = pygame.image.load(resource_path('images/blur.jpg')).convert_alpha()

    def frame(self, screen_size, events, best_score, settings):
        # DRAW BACKGROUND
        self.screen.blit(pygame.transform.scale(self.blur_surface, screen_size), (0, 0))

        # RENDERS
        music_message = "[UNMUTE MUSIC]" if not settings.music else "[MUTE MUSIC]"
        sounds_message = "[UNMUTE SOUND]" if not settings.sounds else "[MUTE SOUND]"

        # DRAW ELEMENTS
        self.draw_text("GAME PAUSED", (screen_size[0] // 2, screen_size[1] // 4))
        self.draw_text(f"BEST SCORE: {best_score}", (screen_size[0] // 2, screen_size[1] // 3))

        # BUTTONS LIST
        button_y = screen_size[1] // 2
        button_spacing = screen_size[1] // 12

        self.draw_button(screen_size[0] // 2, button_y, "[ABORT GAME]", self.parent.abort_game, events)
        self.draw_button(screen_size[0] // 2, button_y + button_spacing, "[FULLSCREEN F11]", self.parent.toggle_fullscreen, events)
        self.draw_button(screen_size[0] // 2, button_y + button_spacing * 2, "[RESET BEST SCORE]", self.parent.score_system.reset_best_score, events)
        self.draw_button(screen_size[0] // 2, button_y + button_spacing * 3, music_message, self.parent.toggle_music, events)
        self.draw_button(screen_size[0] // 2, button_y + button_spacing * 4, sounds_message, self.parent.toggle_sounds, events)

        # DRAW [ESC] and [X] BUTTONS
        self.draw_button(screen_size[0] - screen_size[0] // 6, screen_size[1] // 14, "[ESC]", self.parent.resume_game, events)
        self.draw_button(screen_size[0] - screen_size[0] // 14, screen_size[1] // 14, "[X]", self.parent.quit_game, events, "Red")