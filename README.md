![Logo](logo.png)

#

Marathoner is a simple 2D infinite runner game built with Pygame. The player controls a character who automatically runs through a side-scrolling world. The goal is to avoid obstacles by timing jumps accurately. In the game menu, you can see your best score and adjust settings.

![Game Preview](preview.gif)

## Controls
- Space: Jump and start a new game
- Escape or [ESC]: Toggle the pause menu
- Drag corners or sides: Resize the window

## Menu Settings
- Toggle fullscreen
- Toggle music
- Toggle sounds
- Reset best score

## Getting Started
- Launch the game and press Space or click to start running.
- Avoid obstacles by jumping at the right time.
- Pause the game with [ESC] to access settings or reset your best score.
- Try to beat your high score each run!

## Technology & Implementation

- **Language & Framework:** Marathoner is written in Python and uses the Pygame library for graphics, input, and sound.
- **Modular Design:** The codebase is organized into modules for game logic, UI screens, models, and utilities. This separation makes the code easier to maintain and extend.
- **Game Loop:** The main loop handles event processing, game state updates, and rendering. Screens (start, pause, game, game over) are managed as separate classes for clarity.
- **Asset Management:** Images, fonts, and sounds are loaded from dedicated folders. The `resource_path.py` utility ensures assets are found regardless of the working directory.
- **Persistence:** The best score is saved to a file in the user's home directory, allowing high scores to persist between sessions.
- **Settings:** User preferences (music, sounds, fullscreen) are stored in a config file and can be toggled in-game.
- **Testing:** The project includes a `tests/` directory with unit tests for core logic and models.

## Credits
- Background sky graphics by [gstudioimagen on Freepik](https://www.freepik.com/free-vector/wanderlust-travel-landscapes_5667591.htm#query=pixel%20sky%20background&position=11&from_view=keyword&track=ais)
- In-game font by [OmegaPC777 on Dafont](https://www.dafont.com/omegapc777.d6598)
- Player and stones graphics created via [Bing Image Creator](https://www.bing.com/create)
- Jump sound effect from [YouTube](https://www.youtube.com/watch?v=QmCfnTtM7vU)
- Game over sound effect from [YouTube](https://www.youtube.com/watch?v=bug1b0fQS8Y)
- Theme song by the author. Full version available [here](https://on.soundcloud.com/C6pCU)
