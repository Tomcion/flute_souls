import time

import pydirectinput as pd
import pyautogui as pg
import vgamepad as vg

from sendKeys import PressKey, ReleaseKey

VK_SPACE = 0x20
VK_E = 0x45
VK_R = 0x52
VK_Q = 0x51

VK_W = 0x57
VK_S = 0x53
VK_A = 0x41
VK_D = 0x44

rotateAmount = 10

JMIN = -32768
JMAX = 32767

gamepad = vg.VX360Gamepad()

def rotateRight():
    # posX, posY = mouse.get_position()
    # posX += rotateAmount
    # mouse.move(posX, posY, duration = rotateDuration)
    # pg.move(rotateAmount, 0)
    # asyncio.run(rotRightCor())
    gamepad.right_joystick(x_value=JMAX, y_value=0)
    gamepad.update()

def rotateLeft():
    # posX, posY = mouse.get_position()
    # posX -= rotateAmount
    # mouse.move(posX, posY, duration = rotateDuration)
    # pg.move(-rotateAmount, 0)
    # asyncio.run(rotLeftCor())
    gamepad.right_joystick(x_value=JMIN, y_value=0)
    gamepad.update()

def stopRotate():
    gamepad.right_joystick(x_value=0, y_value=0)
    gamepad.update()

def attack():
    # pg.click()
    # mouse.click('left')
    lockOn()
    gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
    gamepad.update()
    time.sleep(0.1)
    lockOn()
    gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
    gamepad.update()

def heal():
    gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_X)
    gamepad.update()
    time.sleep(0.1)
    gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_X)
    gamepad.update()
    # PressKey(VK_R)
    # ReleaseKey(VK_R)

def lockOn():
    gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB)
    gamepad.update()
    time.sleep(0.1)
    gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB)
    gamepad.update()
    # PressKey(VK_Q)
    # ReleaseKey(VK_Q)

def collect():
    gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
    gamepad.update()
    time.sleep(0.1)
    gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
    gamepad.update()
    # PressKey(VK_E)
    # ReleaseKey(VK_E)

def roll():
    gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
    gamepad.left_joystick(x_value=0, y_value=JMAX)
    gamepad.update()
    time.sleep(0.1)
    gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
    gamepad.left_joystick(x_value=0, y_value=0)
    gamepad.update()
    # PressKey(VK_W)
    # PressKey(VK_SPACE)
    # ReleaseKey(VK_SPACE)
    # ReleaseKey(VK_W)

def walkForward():
    # PressKey(VK_W)
    gamepad.left_joystick(x_value=0, y_value=JMAX)
    gamepad.update()

def stopWalkForward():
    # ReleaseKey(VK_W)
    gamepad.left_joystick(x_value=0, y_value=0)
    gamepad.update()