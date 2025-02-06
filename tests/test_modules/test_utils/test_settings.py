import os
import unittest

from modules.util.settings import Settings, SETTINGS_PATH
from modules.util.setting_type import SettingType


class TestSettings(unittest.TestCase):
    """
    Test the Settings class.
    """
    def setUp(self):
        """
        Set up the test environment by removing the settings 
        file if it exists and initializing the Settings object.
        """
        try:
            os.remove(SETTINGS_PATH)
        except FileNotFoundError:
            pass

        self.settings = Settings()

    def test_default_settings(self):
        """
        Test that the default settings are correctly 
        set to True for both music and sounds.
        """
        self.assertTrue(self.settings.music)
        self.assertTrue(self.settings.sounds)

    def test_update_settings(self):
        """
        Test that updating the settings correctly changes 
        the values and writes them to the settings file.
        """
        self.settings.update_settings(False, SettingType.MUSIC)
        self.settings.update_settings(True, SettingType.SOUNDS)

        self.settings.config.read(SETTINGS_PATH)
        self.assertFalse(self.settings.music)
        self.assertTrue(self.settings.sounds)
        self.assertEqual(self.settings.config.get("GENERAL", SettingType.MUSIC.value), "0")
        self.assertEqual(self.settings.config.get("GENERAL", SettingType.SOUNDS.value), "1")

    def test_no_settings_file(self):
        """
        Test that the settings are correctly 
        initialized when the settings file does not exist.
        """
        os.remove(SETTINGS_PATH)

        self.settings = Settings()
        self.assertTrue(self.settings.music)
        self.assertTrue(self.settings.sounds)
        self.assertTrue(os.path.exists(SETTINGS_PATH))

    def test_create_default_settings(self):
        """
        Test that the default settings are 
        correctly created in the settings file.
        """
        self.settings._create_default_settings()
        self.settings.config.read(SETTINGS_PATH)
        self.assertEqual(self.settings.config.get("GENERAL", SettingType.MUSIC.value), "1")
        self.assertEqual(self.settings.config.get("GENERAL", SettingType.SOUNDS.value), "1")

    def test_load_settings(self):
        """Test that the settings are 
        correctly loaded from the settings file.
        """
        self.settings.update_settings(False, SettingType.MUSIC)
        self.settings.update_settings(False, SettingType.SOUNDS)
        self.settings._load_settings()
        self.assertFalse(self.settings.music)
        self.assertFalse(self.settings.sounds)
