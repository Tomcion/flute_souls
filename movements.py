import mouse

from sendKeys import PressKey, ReleaseKey

VK_SPACE = 0x20
VK_E = 0x45
VK_R = 0x52
VK_Q = 0x51

VK_W = 0x57
VK_S = 0x53
VK_A = 0x41
VK_D = 0x44

rotateAmount = 50

def attack():
    mouse.click('left')

def rotateRight(rotateDuration):
    posX, posY = mouse.get_position()
    posX += rotateAmount
    mouse.move(posX, posY, duration = rotateDuration)

def rotateLeft(rotateDuration):
    posX, posY = mouse.get_position()
    posX -= rotateAmount
    mouse.move(posX, posY, duration = rotateDuration)

def heal():
    PressKey(VK_R)
    ReleaseKey(VK_R)

def lockOn():
    PressKey(VK_Q)
    ReleaseKey(VK_Q)

def collect():
    PressKey(VK_E)
    ReleaseKey(VK_E)

def roll():
    PressKey(VK_W)
    PressKey(VK_SPACE)
    ReleaseKey(VK_SPACE)
    ReleaseKey(VK_W)

def walkForward():
    PressKey(VK_W)

def stopWalkForward():
    ReleaseKey(VK_W)