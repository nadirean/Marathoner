from modules.models.Button import Button

class BaseScreen:
    def __init__(self, screen, game_font, parent):
        self.parent = parent
        self.screen = screen
        self.game_font = game_font

    def draw_button(self, x, y, text, callback, events, color="White"):
        Button(x, y, self.game_font, text, self.screen, callback, events, color).process()

    def draw_text(self, text, center, color="White"):
        rendered_text = self.game_font.render(text, False, color)
        text_rect = rendered_text.get_rect(center=center)
        self.screen.blit(rendered_text, text_rect)