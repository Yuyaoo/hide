import pyautogui as auto
import pyperclip
import re

def hotkeyCtrl(c):
    auto.keyDown('ctrl')
    auto.keyDown(c)
    auto.keyUp(c)
    auto.keyUp('ctrl')

def getCurrentUrl():
    auto.click(300, 70)
    hotkeyCtrl('a')
    hotkeyCtrl('c')
    return pyperclip.paste()

def nextTab():
    hotkeyCtrl('tab')

def closeTab():
    hotkeyCtrl('w')

auto.PAUSE = 0.01

chromeWindow = auto.getWindowsWithTitle('Google Chrome')[0]

chromeWindow.maximize()
chromeWindow.activate()

# go to next tab
# click -> ctrl A -> copy -> verify
# close and loop or end

blacklist = ["reddit.com", "facebook.com", "youtube.com"]

originalUrl = getCurrentUrl()
closed = False

while True:
    if not closed:
        nextTab()
    closed = False
    theUrl = getCurrentUrl()
    for site in blacklist:
        if site in theUrl:
            closeTab()
            closed = True
            break
    if theUrl == originalUrl:
        break
