![Logo](logo.png)

#

Marathoner is a 2D infinite runner built with Python and Pygame. The player automatically runs through a side-scrolling world, jumping to avoid stone obstacles. Score equals time survived; best score persists between sessions.

![Game Preview](preview.gif)

## Controls
- **Space**: Jump / start a new game
- **Escape**: Toggle the pause menu
- **Drag corners/sides**: Resize the window (aspect ratio constrained between 1.6:1 and 1.9:1)

## Menu Settings
- Toggle fullscreen
- Toggle music and sounds
- Reset best score

## Architecture

```
marathoner/
├── main.py                  # Entry point
├── resource_path.py         # PyInstaller-aware asset path resolver
├── modules/
│   ├── Game.py              # Core game loop, state machine, event dispatch
│   ├── models/
│   │   ├── player.py        # Player sprite: physics, animation, input
│   │   └── obstacle.py      # Obstacle spawning, movement, scaling
│   ├── screens/
│   │   ├── base_screen.py   # Abstract base with draw_text/draw_button
│   │   ├── start_game_screen.py
│   │   ├── game_screen.py
│   │   ├── pause_game_screen.py
│   │   └── game_over_screen.py
│   ├── components/
│   │   ├── button.py        # Interactive UI button with hover/click
│   │   └── error_popup.py   # Modal error dialog with cached resources
│   └── util/
│       ├── constants.py     # Game tuning values, enums, file paths
│       ├── settings.py      # INI-based settings persistence
│       └── score_system.py  # Score rendering, best score I/O
└── tests/                   # 30 unit tests (unittest)
```

## Technical Details

- **State machine**: `Game.py` manages four states (start, playing, paused, game over) via an integer `current_screen`. Each state delegates rendering to its corresponding screen class.
- **Pixel-perfect collision**: Uses `pygame.mask` for sprite-level hit detection between the player and obstacles.
- **Adaptive scaling**: All sprites and UI elements resize proportionally to the window size. Jump strength and gravity are computed from a linear formula (`mx + b`) to stay consistent across resolutions.
- **Aspect ratio lock**: Window resize is clamped to a 1.6:1–1.9:1 range, recalculating both dimensions to prevent distortion.
- **Persistence**: Best score (`~/Marathoner/best_score.txt`) and settings (`~/Marathoner/settings.ini`) are stored in the user's home directory with error handling for missing/corrupt files.
- **Asset loading**: `resource_path.py` resolves paths for both development and PyInstaller bundles.
- **Error resilience**: `ErrorPopup` provides a modal fallback when settings or score files fail to load, with cached resources to avoid repeated file I/O.

## Getting Started

```bash
uv run main.py
```

Requires Python 3.13+ and `pygame>=2.6.1`.

## Credits
- Background sky graphics by [gstudioimagen on Freepik](https://www.freepik.com/free-vector/wanderlust-travel-landscapes_5667591.htm#query=pixel%20sky%20background&position=11&from_view=keyword&track=ais)
- In-game font by [OmegaPC777 on Dafont](https://www.dafont.com/omegapc777.d6598)
- Player and stones graphics created via [Bing Image Creator](https://www.bing.com/create)
- Jump sound effect from [YouTube](https://www.youtube.com/watch?v=QmCfnTtM7vU)
- Game over sound effect from [YouTube](https://www.youtube.com/watch?v=bug1b0fQS8Y)
- Theme song by the author. Full version available [here](https://on.soundcloud.com/C6pCU)
