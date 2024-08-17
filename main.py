import ctypes
from ctypes import wintypes
import time

from sendKeys import PressKey, ReleaseKey, VK_MENU, VK_TAB

def AltTab():
    """Press Alt+Tab and hold Alt key for 2 seconds
    in order to see the overlay.
    """
    PressKey(VK_MENU)   # Alt
    PressKey(VK_TAB)    # Tab
    ReleaseKey(VK_TAB)  # Tab~
    time.sleep(2)
    ReleaseKey(VK_MENU) # Alt~

# if __name__ == "__main__":
    # AltTab()

