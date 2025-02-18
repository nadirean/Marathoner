import pygame

from resource_path import resource_path

class ErrorPopup:
    def __init__(self, screen, screen_size):
        self.screen_size = screen_size
        self.screen = screen

    def display_error(self, message):
        font_large = pygame.font.Font(resource_path('font/pixeled.ttf'), (self.screen_size[0] + self.screen_size[1]) // 50)
        font_small = pygame.font.Font(resource_path('font/pixeled.ttf'), (self.screen_size[0] + self.screen_size[1]) // 70)
        self.blur_surface = pygame.image.load(resource_path('images/blur.jpg')).convert_alpha()

        # Render the "ERROR" message
        error_surface_large = font_large.render("ERROR", True, 'Red')
        error_rect_large = error_surface_large.get_rect(center=(self.screen_size[0] // 2, self.screen_size[1] // 2.5))

        # Render the error message
        error_surface_small = font_small.render(message, True, 'White')
        error_rect_small = error_surface_small.get_rect(center=(self.screen_size[0] // 2, self.screen_size[1] // 2))

        # Render the "Press SPACE to continue" message
        continue_surface = font_small.render("Press SPACE to continue", True, 'White')
        continue_rect = continue_surface.get_rect(center=(self.screen_size[0] // 2, self.screen_size[1] // 1.1))

        # Blit the "ERROR" message onto the blur surface
        self.blur_surface.blit(error_surface_large, error_rect_large)

        # Blit the error message onto the blur surface
        self.blur_surface.blit(error_surface_small, error_rect_small)

        # Blit the "Press SPACE to continue" message onto the blur surface
        self.blur_surface.blit(continue_surface, continue_rect)

        # Blit the base surface onto the main screen
        self.screen.blit(pygame.transform.scale(self.blur_surface, self.screen_size), (0, 0))
        pygame.display.update()

        # Wait for SPACE key press to continue
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    waiting = False