"""
A module containing the Settings class.
"""

import configparser
import os

from modules.util.setting_type import SettingType

DEFAULT_SETTINGS = {
    'GENERAL': { SettingType.MUSIC.value: 1, SettingType.SOUNDS.value: 1 }
}

SETTINGS_PATH = os.path.join(os.path.expanduser("~"), 'Marathoner', 'settings.ini')


class Settings:
    """
    A class responsible for handling the game settings.
    
    Attributes:
    music (bool): Whether the music is enabled.
    sounds (bool): Whether the sounds are enabled.
    config (configparser.ConfigParser): The configuration parser.
    
    Methods:
    update_settings: Update the game settings.
    """
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.music = bool(DEFAULT_SETTINGS['GENERAL'][SettingType.MUSIC.value])
        self.sounds = bool(DEFAULT_SETTINGS['GENERAL'][SettingType.SOUNDS.value])

        self._load_settings()

    def _load_settings(self):
        # Create the settings file if it doesn't exist
        if not os.path.exists(SETTINGS_PATH):
            self._create_default_settings()
        # Otherwise, read the settings from the file and update the attributes
        else:
            self.config.read(SETTINGS_PATH)
            for setting in SettingType:
                setattr(self, setting.value.lower(),
                        self.config.getboolean("GENERAL", setting.value))

    def _create_default_settings(self):
        # Create the settings file with the default settings
        for section, settings in DEFAULT_SETTINGS.items():
            self.config[section] = {key: str(value) for key, value in settings.items()}

        with open(SETTINGS_PATH, 'w', encoding='utf-8') as f:
            self.config.write(f)

    def update_settings(self, state: bool, setting: SettingType):
        """
        Update the game settings.

        Parameters:
        state (bool): the new state of the setting.
        setting (SettingType): the setting to update.
        """
        setattr(self, setting.value.lower(), state)
        self.config.set("GENERAL", setting.value, "1" if state else "0")

        with open(SETTINGS_PATH, 'w', encoding='utf-8') as f:
            self.config.write(f)
