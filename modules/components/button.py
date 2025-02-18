"""
A module that contains the Button class.
"""

import pygame


class Button:
    """
    A class representing a button.
    
    Attributes:
    x (int): The x-coordinate of the button.
    y (int): The y-coordinate of the button.
    font (pygame.font.Font): The font of the button.
    text (str): The text of the button.
    screen (pygame.Surface): The screen to draw the button on.
    on_click_function (function): The function to call when the button is clicked.
    events (list): A list of pygame events.
    hover_colour (str): The colour of the button when the mouse is hovering over it.
    button_text (pygame.Surface): The text of the button.
    button_rect (pygame.Rect): The rectangle of the button text.
    
    Methods:
    process: Process the button.
    """
    def __init__(self, x, y, font, text, screen, on_click_function, events, hover_colour="Gray"):
        self.x = x
        self.y = y
        self.font = font
        self.text = text
        self.screen = screen
        self.on_click_function = on_click_function
        self.events = events
        self.hover_colour = hover_colour

        self.button_text = font.render(text, True, "White")
        self.button_rect = self.button_text.get_rect(center=(x,y))

    def process(self):
        """
        Process the button.
        
        If the mouse is hovering over the button, the button's 
        colour will change to the hover colour.
        If the button is clicked, the on_click_function will be called.
        """
        if self.button_rect.collidepoint(pygame.mouse.get_pos()):
            self.button_text = self.font.render(self.text, True, self.hover_colour)
            if any(event.type == pygame.MOUSEBUTTONDOWN for event in self.events):
                self.on_click_function()

        self.screen.blit(self.button_text, self.button_rect)
