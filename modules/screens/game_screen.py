import pygame

from modules.screens.base_screen import BaseScreen

class GameScreen(BaseScreen):
    def __init__(self, screen, game_font, parent):
        super().__init__(screen, game_font, parent)

    def frame(self, screen_size, events):
        # DRAW BACKGROUND
        self.screen.blit(pygame.transform.scale(self.parent.sky_surface, screen_size), (0, 0))
        self.screen.blit(pygame.transform.scale(self.parent.ground_surface, screen_size), (0, screen_size[1] * 0.6))

        # DRAW PLAYER AND OBSTACLES
        self.parent.player.draw(self.screen)
        self.parent.player.update(self.parent.channel2)

        self.parent.obstacle_group.draw(self.screen)
        self.parent.obstacle_group.update()

        # DRAW VIGNETTE
        self.screen.blit(pygame.transform.scale(self.parent.vignette_surface, screen_size), (0, 0))

        # DRAW SCORE
        self.parent.score = self.parent.score_system.display_score(self.game_font, self.parent.start_time, self.screen)

        # CHECK FOR COLLISIONS
        self.parent.current_screen = self.parent.collision_sprite()

        # DRAW [ESC] and [X] BUTTONS
        self.draw_button(screen_size[0] - screen_size[0] // 6, screen_size[1] // 14, "[ESC]", self.parent.pause_game, events)
        self.draw_button(screen_size[0] - screen_size[0] // 14, screen_size[1] // 14, "[X]", self.parent.quit_game, events, "Red")