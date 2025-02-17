from modules.screens.base_screen import BaseScreen

class SettingsScreen(BaseScreen):
    def __init__(self, screen, game_font, parent):
        super().__init__(screen, game_font, parent)

    def frame(self, screen_size, events, settings):
        # DRAW BACKGROUND
        self.screen.fill((0, 0, 0))

        # RENDERS
        music_message = "[UNMUTE MUSIC]" if not settings.music else "[MUTE MUSIC]"
        sounds_message = "[UNMUTE SOUND]" if not settings.sounds else "[MUTE SOUND]"

        # DRAW ELEMENTS
        self.draw_text("SETTINGS", (screen_size[0] // 2, screen_size[1] // 4))

        # BUTTONS LIST
        button_y = screen_size[1] // 2
        button_spacing = screen_size[1] // 12

        self.draw_button(screen_size[0] // 2, button_y, "[FULLSCREEN F11]", self.parent.toggle_fullscreen, events)
        self.draw_button(screen_size[0] // 2, button_y + button_spacing, music_message, self.parent.toggle_music, events)
        self.draw_button(screen_size[0] // 2, button_y + button_spacing * 2, sounds_message, self.parent.toggle_sounds, events)

        # DRAW [ESC] and [X] BUTTONS
        self.draw_button(screen_size[0] - screen_size[0] // 6, screen_size[1] // 14, "[ESC]", self.parent.resume_game, events)
        self.draw_button(screen_size[0] - screen_size[0] // 14, screen_size[1] // 14, "[X]", self.parent.quit_game, events, "Red")