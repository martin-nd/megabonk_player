# Download the packaged .exe to the right under 'releases'

### Download the zip and unzip it - follow the included readme.txt

## Requirements
- Game must be:
  - Running in full screen
  - Running in native display resolution
- Screen scaling must be at 100%
- Only works on Windows


# Megabonk afk gaming challenge script

Automates attempts at the afk gaming challenge on forest tier 1

---

## Usage

```powershell
.\megabonk_player.exe -c <character> [-d <delay>] [-rps <rotations_per_second>]
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

## Requirements to run source code

- `uv` package manager recommended
- Python 3.12
- commands:

```bash
 uv venv
 uv sync
```

