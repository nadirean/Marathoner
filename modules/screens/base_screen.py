"""
A module that contains the BaseScreen class.
"""

from modules.components.button import Button


class BaseScreen:
    """
    A class that represents the base screen.
    
    Attributes:
    screen (pygame.Surface): The screen to draw on.
    game_font (pygame.font.Font): The font to use.
    parent (pygame.Surface): The parent screen.
    
    Methods:
    draw_button: Draws a button on the screen.
    draw_text: Draws text on the screen.
    """
    def __init__(self, screen, game_font, parent):
        self.parent = parent
        self.screen = screen
        self.game_font = game_font

    def draw_button(self, x, y, text, callback, events, color="White"):
        """
        Draws a button on the screen.
        
        Parameters:
        x (int): The x-coordinate of the button.
        y (int): The y-coordinate of the button.
        text (str): The text to display on the button.
        callback (function): The function to call when the button is clicked.
        events (list): The events to listen for.
        color (str): The color of the button. Default is "White".
        """
        Button(x, y, self.game_font, text, self.screen, callback, events, color).process()

    def draw_text(self, text, center, color="White"):
        """
        Draws text on the screen.
        
        Parameters:
        text (str): The text to display.
        center (tuple): The center of the text.
        color (str): The color of the text. Default is "White".
        """
        rendered_text = self.game_font.render(text, False, color)
        text_rect = rendered_text.get_rect(center=center)
        self.screen.blit(rendered_text, text_rect)
