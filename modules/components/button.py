"""
A module that contains the Button class for UI interaction.
"""

from typing import List, Callable

import pygame

from modules.util.constants import Colors


class Button:
    """
    A class representing an interactive UI button.

    This class handles button rendering, hover effects, and click detection
    for the game's user interface elements.

    Attributes:
        x: X coordinate of button center
        y: Y coordinate of button center
        font: Font used to render button text
        text: Button text content
        screen: Surface to draw the button on
        on_click_function: Function to call when button is clicked
        events: List of pygame events to check for clicks
        hover_colour: Color when mouse hovers over button
        button_text: Rendered text surface
        button_rect: Rectangle defining button bounds
    """
    def __init__(
        self,
        x: int,
        y: int,
        font: pygame.font.Font,
        text: str,
        screen: pygame.Surface,
        on_click_function: Callable[[], None],
        events: List[pygame.event.Event],
        hover_colour: str
    ) -> None:
        """
        Initialize a new button.
        """
        self.x = x
        self.y = y
        self.font = font
        self.text = text
        self.screen = screen
        self.on_click_function = on_click_function
        self.events = events
        self.hover_colour = hover_colour

        # Initialize button rendering
        self.button_text = font.render(text, True, Colors.WHITE)
        self.button_rect = self.button_text.get_rect(center=(x, y))

    def process(self) -> None:
        """
        Process the button.
        
        If the mouse is hovering over the button, the button's 
        colour will change to the hover colour.
        If the button is clicked, the on_click_function will be called.
        """
        # If the mouse is hovering over the button, change its colour
        if self.button_rect.collidepoint(pygame.mouse.get_pos()):
            self.button_text = self.font.render(self.text, True, self.hover_colour)
            # If the button is clicked, call the on_click_function
            if any(event.type == pygame.MOUSEBUTTONDOWN for event in self.events):
                self.on_click_function()

        # Draw the button text on the screen
        self.screen.blit(self.button_text, self.button_rect)
