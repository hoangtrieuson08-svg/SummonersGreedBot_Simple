#!/usr/bin/env python3
"""
Summoner's Greed Bot - Stable Version
Click directly into BlueStacks without affecting Windows mouse
"""

import time
import sys
import logging
from pathlib import Path

try:
    import win32gui
    import win32con
    import win32api
    import cv2
    import numpy as np
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("Run: pip install -r requirements.txt")
    sys.exit(1)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

BLUESTACKS_WINDOW_NAME = "BlueStacks App Player"

class BlueStacksBot:
    def __init__(self):
        self.hwnd = None
        self.find_bluestacks_window()
        logger.info("Bot initialized successfully")

    def find_bluestacks_window(self):
        """Find and verify BlueStacks window"""
        self.hwnd = win32gui.FindWindow(None, BLUESTACKS_WINDOW_NAME)
        if self.hwnd == 0:
            logger.error(f"BlueStacks window '{BLUESTACKS_WINDOW_NAME}' not found!")
            logger.info("Make sure BlueStacks is running and window is not minimized")
            sys.exit(1)
        logger.info(f"Found BlueStacks window: {self.hwnd}")

    def click_direct(self, x, y):
        """
        Click directly at (x, y) coordinates in BlueStacks
        Does NOT move Windows mouse cursor
        """
        try:
            # Get window position
            left, top, right, bottom = win32gui.GetWindowRect(self.hwnd)
            
            # Convert to absolute coordinates
            abs_x = left + x
            abs_y = top + y
            
            # Create LPARAM for WM_LBUTTONDOWN/UP
            lParam = win32api.MAKELONG(int(x), int(y))
            
            # Send click messages directly to BlueStacks child window
            # This doesn't move the mouse cursor
            win32gui.PostMessage(self.hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
            time.sleep(0.05)
            win32gui.PostMessage(self.hwnd, win32con.WM_LBUTTONUP, 0, lParam)
            
            logger.info(f"Clicked at ({x}, {y}) in BlueStacks")
            time.sleep(0.5)
        except Exception as e:
            logger.error(f"Click failed: {e}")

    def take_screenshot(self):
        """
        Capture screenshot of BlueStacks window
        """
        try:
            left, top, right, bottom = win32gui.GetWindowRect(self.hwnd)
            width = right - left
            height = bottom - top
            
            # Take screenshot using PIL
            from PIL import ImageGrab
            screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))
            img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            return img
        except Exception as e:
            logger.error(f"Screenshot failed: {e}")
            return None

    def find_image_in_screen(self, template_path, confidence=0.8):
        """
        Find a template image in the current BlueStacks screenshot
        Returns (x, y) if found, None otherwise
        """
        if not Path(template_path).exists():
            logger.warning(f"Template not found: {template_path}")
            return None
        
        try:
            screenshot = self.take_screenshot()
            if screenshot is None:
                return None
            
            template = cv2.imread(template_path, 0)  # Grayscale
            if template is None:
                logger.warning(f"Could not load template: {template_path}")
                return None
            
            # Convert screenshot to grayscale
            screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
            
            # Find template
            result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
            if max_val >= confidence:
                # Get center of matched area
                h, w = template.shape
                center_x = max_loc[0] + w // 2
                center_y = max_loc[1] + h // 2
                logger.info(f"Found '{Path(template_path).name}' at ({center_x}, {center_y}) - confidence: {max_val:.2f}")
                return (center_x, center_y)
            else:
                logger.debug(f"'{Path(template_path).name}' not found (confidence: {max_val:.2f} < {confidence})")
                return None
        except Exception as e:
            logger.error(f"Image detection failed: {e}")
            return None

    def run(self):
        """
        Main game loop
        Automatically detect scenes and click appropriate buttons
        """
        logger.info("Starting bot...")
        logger.info("Press Ctrl+C to stop")
        
        resources_dir = Path("resources")
        if not resources_dir.exists():
            logger.warning(f"Resources directory not found: {resources_dir}")
            logger.info("Please ensure you have template images in 'resources' folder")
        
        try:
            while True:
                time.sleep(1.5)  # Check every 1.5 seconds
                
                # Try to find and click various scenes
                # Order matters - check specific states first
                
                # 1. Check for Seller screen
                seller_buy = resources_dir / "seller_buy.png"
                if seller_buy.exists():
                    pos = self.find_image_in_screen(str(seller_buy), confidence=0.85)
                    if pos:
                        self.click_direct(pos[0], pos[1])
                        time.sleep(1)
                        continue
                
                # 2. Check for Continue button
                continue_btn = resources_dir / "continue.png"
                if continue_btn.exists():
                    pos = self.find_image_in_screen(str(continue_btn), confidence=0.85)
                    if pos:
                        self.click_direct(pos[0], pos[1])
                        time.sleep(1)
                        continue
                
                # 3. Check for Confirm button
                confirm_btn = resources_dir / "confirm.png"
                if confirm_btn.exists():
                    pos = self.find_image_in_screen(str(confirm_btn), confidence=0.85)
                    if pos:
                        self.click_direct(pos[0], pos[1])
                        time.sleep(1)
                        continue
                
                # 4. Check for Map selection
                map_main = resources_dir / "map_main.png"
                if map_main.exists():
                    pos = self.find_image_in_screen(str(map_main), confidence=0.85)
                    if pos:
                        self.click_direct(pos[0], pos[1])
                        time.sleep(1)
                        continue
        
        except KeyboardInterrupt:
            logger.info("\nBot stopped by user")
            sys.exit(0)
        except Exception as e:
            logger.error(f"Bot error: {e}")
            sys.exit(1)

def main():
    print("="*60)
    print("Summoner's Greed Bot - Stable Version")
    print("="*60)
    print()
    print("Requirements:")
    print("1. BlueStacks must be running")
    print("2. Game must be open in BlueStacks")
    print("3. Template images must be in 'resources' folder")
    print()
    print("How to get template images:")
    print("1. Run: python screenshot_tool.py")
    print("2. Take screenshots of each game state")
    print("3. Save them in 'resources' folder:")
    print("   - resources/seller_buy.png")
    print("   - resources/continue.png")
    print("   - resources/confirm.png")
    print("   - resources/map_main.png")
    print()
    print("="*60)
    print()
    
    bot = BlueStacksBot()
    bot.run()

if __name__ == "__main__":
    main()
