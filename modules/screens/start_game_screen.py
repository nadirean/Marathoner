import pygame

from modules.screens.base_screen import BaseScreen
from resource_path import resource_path

class StartGameScreen(BaseScreen):
    def __init__(self, screen, game_font, parent):
        super().__init__(screen, game_font, parent)
        self.sky_surface = pygame.image.load(resource_path('images/sky.jpg')).convert()
        self.vignette_surface = pygame.image.load(resource_path('images/vignette.png')).convert_alpha()

    def frame(self, screen_size, events, best_score):
        self.screen.blit(pygame.transform.scale(self.sky_surface, screen_size), (0, 0))
        self.screen.blit(pygame.transform.scale(self.vignette_surface, screen_size), (0, 0))

        # DRAW ELEMENTS
        self.draw_text(f"BEST SCORE: {best_score}", (screen_size[0] // 2, screen_size[1] // 1.1))

        self.draw_button(screen_size[0] // 2, screen_size[1] // 1.25, "CLICK OR PRESS 'SPACE' TO START", self.parent.start_game, events)
        self.draw_button(screen_size[0] // 2, screen_size[1] // 12, "[VISIT MY GITHUB]", self.parent.open_github, events)
        self.draw_button(screen_size[0] - screen_size[0] // 14, screen_size[1] // 14, "[X]", self.parent.quit_game, events, "Red")