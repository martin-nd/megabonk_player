# Download the packaged .exe on the right!

### Download the zip and unzip it - follow the included readme.txt

# Megabonk Player Automation Script

Automates gameplay for the “Megabonk” game by performing repeated runs, detecting deaths, and logging results automatically.

## Overview

This script uses **PyAutoGUI** and **OpenCV** to automate character selection, gameplay loops, and data logging. It performs runs until a death is detected, logs session information, and repeats indefinitely until interrupted.

---

## Usage

```bash
megabonk_player.exe -c <character> [-d <delay>] [-rps <rotations_per_second>]
```

### Arguments

| Argument | Short | Type | Default | Description |
|-----------|--------|------|----------|--------------|
| `--character` | `-c` | `str` | *(required)* | Character name to use. Must be selected and at the main menu before starting. |
| `--delay` | `-d` | `int` | `0` | Start delay (seconds) before running, useful for single-screen setups. |
| `--rotations-per-second` | `-rps` | `float` | `1.0` | Character spin rate during gameplay. |

Example:
```bash
megabonk_player.exe -c "fox" -d 5 -rps 2.5
```

---

## Features

- **Automated GUI Interaction**  
  Clicks through menus and challenges using template images.

- **Death Detection**  
  Uses OpenCV to monitor a defined screen region and detect when the “death bar” appears.

- **Auto-Logging**  
  Records run start time, end time, character, and spin rate in `logdata/log.xlsx`.

- **Average Run Summary**  
  Displays total runs and average duration after exit.

---

## Output

After each session, a log file is created or updated at:
```
logdata/log.xlsx
```

The log contains:
| Column | Description |
|---------|-------------|
| `run_start` | Timestamp when run began |
| `run_end` | Timestamp when run ended |
| `character` | Character used |
| `rps` | Rotations per second |

---

## Exit Conditions

The loop ends when:
- The user presses **Ctrl+C** (KeyboardInterrupt)
- PyAutoGUI’s **failsafe** (moving the mouse to a screen corner) is triggered

---

## Requirements

- Python 3.10+
- Packages:
  ```bash
  pip install pyautogui opencv-python-headless numpy polars
  ```
- Image assets located in `img/` directory.

---

## Notes

- When bundled with **PyInstaller**, image assets are loaded from the temporary `_MEIPASS` path.  
- Ensure the game is visible and not minimized.  
- Game must be running in full screen on primary display.
