# Summoner's Greed Bot - Stable Version

Automatic bot for Summoner's Greed game running in BlueStacks.

**Key Features:**
- ✅ Click directly into BlueStacks without affecting Windows mouse
- ✅ Image detection (template matching) for scene recognition
- ✅ Supports custom template images
- ✅ Runs in background
- ✅ Minimal dependencies

## Requirements

- **Windows 10/11** (uses Win32 API)
- **BlueStacks 5.x** (tested on 5.2+)
- **Python 3.8+**

## Installation

1. **Clone or download this repository**

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## Setup

### Step 1: Capture Template Images

The bot needs template images of game screens to detect them.

1. **Run the screenshot tool:**
```bash
python screenshot_tool.py
```

2. **Follow the prompts** to capture:
   - Seller BUY button
   - CONTINUE button
   - CONFIRM button
   - MAP selection screen

3. **Images will be saved in `resources/` folder**

### Step 2: Run the Bot

1. **Make sure BlueStacks is running** with the game open
2. **Run:**
```bash
python main.py
```

3. **Bot will start detecting scenes and clicking automatically**

4. **Press Ctrl+C to stop**

## How It Works

1. **Takes screenshots** of BlueStacks window every 1.5 seconds
2. **Detects scenes** using template matching (OpenCV)
3. **Clicks appropriate buttons** using Win32 API
4. **Does NOT move Windows mouse** - you can use computer normally

## Troubleshooting

### Bot doesn't find BlueStacks
- Make sure BlueStacks window is visible (not minimized)
- Check window title is exactly "BlueStacks App Player"

### Template images not detected
- Recapture templates using `screenshot_tool.py`
- Make sure buttons are clearly visible in the screenshot
- Adjust confidence threshold in `main.py` (line ~110) if needed

### Bot clicks wrong position
- This usually means template images don't match current game state
- Recapture templates
- Check screen resolution/scaling settings

## Advanced

### Adjust detection confidence
In `main.py`, change the confidence value (default 0.85):
```python
pos = self.find_image_in_screen(str(seller_buy), confidence=0.85)  # Higher = stricter
```

### Add more actions
Edit the `run()` method in `main.py` to add more game states or buttons.

## Notes

- Bot checks for game states every 1.5 seconds
- If multiple matches found, uses the first one
- Template images should be clear screenshots of the buttons
- Works even when BlueStacks window is in background

## License

Free to use and modify.
