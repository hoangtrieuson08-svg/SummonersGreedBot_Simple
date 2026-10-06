#!/usr/bin/env python3
"""
Tool to capture template images for the bot
Use this to take screenshots of game states
"""

import time
import sys
import os
from pathlib import Path

try:
    import win32gui
    import cv2
    import numpy as np
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("Run: pip install -r requirements.txt")
    sys.exit(1)

BLUESTACKS_WINDOW_NAME = "BlueStacks App Player"

def take_screenshot():
    """Capture BlueStacks window"""
    from PIL import ImageGrab
    
    hwnd = win32gui.FindWindow(None, BLUESTACKS_WINDOW_NAME)
    if hwnd == 0:
        print(f"Error: BlueStacks window not found!")
        return None
    
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))
    img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    return img

def main():
    print("="*60)
    print("Screenshot Tool - Capture Template Images")
    print("="*60)
    print()
    
    # Create resources directory
    resources_dir = Path("resources")
    resources_dir.mkdir(exist_ok=True)
    
    templates = [
        ("seller_buy.png", "Seller BUY button"),
        ("continue.png", "CONTINUE button"),
        ("confirm.png", "CONFIRM button"),
        ("map_main.png", "MAP selection screen"),
    ]
    
    for filename, description in templates:
        filepath = resources_dir / filename
        
        if filepath.exists():
            response = input(f"\n{description} ({filename}) already exists. Recapture? (y/n): ").lower()
            if response != 'y':
                print(f"Skipping {filename}")
                continue
        
        print(f"\nCapturing {description}...")
        print("1. Open BlueStacks and navigate to the screen showing this element")
        print(f"2. You have 5 seconds to position the window")
        print("3. Make sure the button/element is clearly visible")
        print()
        
        for i in range(5, 0, -1):
            print(f"Capturing in {i}...", end="\r")
            time.sleep(1)
        
        img = take_screenshot()
        if img is None:
            print(f"Failed to capture {filename}")
            continue
        
        cv2.imwrite(str(filepath), img)
        print(f"\nSaved: {filepath}")
        print(f"Image size: {img.shape[1]}x{img.shape[0]}")
        
        # Display the image
        cv2.imshow(f"Captured: {description}", img)
        print("Press any key to continue...")
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    print("\n" + "="*60)
    print("Template capture complete!")
    print("You can now run: python main.py")
    print("="*60)

if __name__ == "__main__":
    main()
