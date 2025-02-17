import pygame
from modules.models.Button import Button

class SettingsScreen:
    def __init__(self, screen, game_font, parent):
        self.parent = parent
        self.screen = screen
        self.game_font = game_font

    def frame(self, screen_size, events, settings):
        # DRAW BACKGROUND
        self.screen.fill((0, 0, 0))

        # RENDERS
        music_message = "[UNMUTE MUSIC]" if not settings.music else "[MUTE MUSIC]"
        sounds_message = "[UNMUTE SOUND]" if not settings.sounds else "[MUTE SOUND]"

        settings_text = self.game_font.render("SETTINGS", False, "White")

        # RECTANGLES
        settings_text_rect = settings_text.get_rect(center=(screen_size[0] // 2, screen_size[1] // 4))

        # DRAW ELEMENTS
        self.screen.blit(settings_text, settings_text_rect)

        # BUTTONS LIST
        button_y = screen_size[1] // 2
        button_spacing = screen_size[1] // 12

        Button(screen_size[0] // 2, button_y, self.game_font, "[FULLSCREEN F11]", self.screen, self.parent.toggle_fullscreen, events).process()
        Button(screen_size[0] // 2, button_y + button_spacing, self.game_font, music_message, self.screen, self.parent.toggle_music, events).process()
        Button(screen_size[0] // 2, button_y + button_spacing * 2, self.game_font, sounds_message, self.screen, self.parent.toggle_sounds, events).process()

        # DRAW [ESC] and [X] BUTTONS
        Button(screen_size[0] - screen_size[0] // 6, screen_size[1] // 14, self.game_font, "[ESC]", self.screen, self.parent.resume_game, events).process()
        Button(screen_size[0] - screen_size[0] // 14, screen_size[1] // 14, self.game_font, "[X]", self.screen, self.parent.quit_game, events, "Red").process()