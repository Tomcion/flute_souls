import vgamepad as vg
import time

gamepad = vg.VX360Gamepad()

while True:
    print("press")
    gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
    gamepad.update()
    time.sleep(0.5)
    print("release")
    gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
    gamepad.update()
    time.sleep(0.5)
