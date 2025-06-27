"""
A module that provides a utility function to get the absolute path of resources.
"""

import os
import sys
from pathlib import Path


def resource_path(relative_path: str) -> str:
    """
    Get absolute path to resource, works for dev and for PyInstaller.
    
    This function handles the difference between development (where resources
    are relative to the script) and PyInstaller builds (where resources are
    in a temporary folder).
    
    Args:
        relative_path: Path relative to the application root
        
    Returns:
        Absolute path to the resource file
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = getattr(sys, '_MEIPASS', Path(__file__).parent.absolute())
        return os.path.join(base_path, relative_path)
    except Exception:
        # Fallback to current directory if anything goes wrong
        return os.path.join(Path.cwd(), relative_path)
