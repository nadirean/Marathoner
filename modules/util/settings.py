"""
A module containing the Settings class for game configuration management.
"""

import os
from typing import TYPE_CHECKING
import configparser

from modules.util.constants import SettingType, DEFAULT_SETTINGS, SETTINGS_PATH
from modules.components.error_popup import ErrorPopup

if TYPE_CHECKING:
    import pygame


class Settings:
    """
    A class responsible for handling game settings persistence and management.

    This class manages loading, saving, and updating game settings including
    music and sound preferences. Settings are stored in an INI file in the
    user's home directory.

    Attributes:
        music: Whether background music is enabled
        sounds: Whether sound effects are enabled
        config: ConfigParser instance for INI file management
    """
    def __init__(self, screen_size: tuple = None, screen: 'pygame.Surface' = None, ) -> None:
        """Initialize settings with default values and load from file if available."""
        self.config = configparser.ConfigParser()

        # Set default values
        self.music: bool = bool(DEFAULT_SETTINGS['GENERAL'][SettingType.MUSIC.value])
        self.sounds: bool = bool(DEFAULT_SETTINGS['GENERAL'][SettingType.SOUNDS.value])

        # If screen is provided, use it for error popups
        self.screen = screen
        self.screen_size = screen_size

        os.makedirs(os.path.dirname(SETTINGS_PATH), exist_ok=True)
        self._load_settings()

    def _load_settings(self) -> None:
        """Load settings from file, creating default file if none exists."""
        if not SETTINGS_PATH.exists():
            self._create_default_settings()
        else:
            try:
                self.config.read(SETTINGS_PATH)
                self._update_attributes_from_config()
            except (configparser.Error, ValueError) as e:
                if self.screen:
                    ErrorPopup(self.screen, self.screen_size).display_error(f"Could not load settings file: {e}")
                self._create_default_settings()

    def _update_attributes_from_config(self) -> None:
        """Update instance attributes from loaded configuration."""
        try:
            for setting in SettingType:
                setting_value = self.config.getboolean("GENERAL", setting.value)
                setattr(self, setting.value.lower(), setting_value)
        except (configparser.NoSectionError, configparser.NoOptionError, ValueError) as e:
            if self.screen:
                ErrorPopup(self.screen, self.screen_size).display_error(f"Invalid settings format: {e}")
            self._create_default_settings()

    def _create_default_settings(self) -> None:
        """Create settings file with default values."""
        try:
            # Clear any existing configuration
            self.config.clear()

            # Add default settings
            for section, settings in DEFAULT_SETTINGS.items():
                self.config[section] = {key: str(value) for key, value in settings.items()}

            # Write to file
            with open(SETTINGS_PATH, 'w', encoding='utf-8') as f:
                self.config.write(f)

        except OSError as e:
            if self.screen:
                ErrorPopup(self.screen, self.screen_size).display_error(f"Error creating settings file: {e}")

    def update_settings(self, state: bool, setting: SettingType) -> bool:
        """
        Update a game setting and save to file.

        Args:
            state: New state of the setting (True/False)
            setting: The setting type to update

        Returns:
            True if successfully updated and saved, False otherwise
        """
        try:
            # Update instance attribute
            setattr(self, setting.value.lower(), state)

            # Update configuration
            if not self.config.has_section("GENERAL"):
                self.config.add_section("GENERAL")

            self.config.set("GENERAL", setting.value, "1" if state else "0")

            # Save to file
            with open(SETTINGS_PATH, 'w', encoding='utf-8') as f:
                self.config.write(f)

            return True

        except OSError as e:
            if self.screen:
                ErrorPopup(self.screen, self.screen_size).display_error(f"Error saving settings: {e}")
            return False
