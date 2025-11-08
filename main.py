import os
import pyautogui as gui
import cv2
import time as t
import numpy as np
import polars as pl
from typing import DefaultDict
from datetime import datetime as dt
from random import randint

## Button globals
MM_PLAYBUTTON = 'img/mmplay.png'
CONFIRMBUTTON = 'img/confirm.png'
CHALLENGECONFIRM = 'img/challengeconfirm.png'
MS_CHALLENGES = 'img/mschallenges.png'
AFKGAMING = 'img/afkgaming.png'
FOREST = 'img/forest.png'
TIER1 = 'img/tier1.png'
DARKCONFIRM = 'img/darkconfirm.png'
LIGHTPLAY = 'img/lightplay.png'
CANTCONFIRM = 'img/cantconfirm.png'
YOUDED = 'img/youded.png'
DEATHBAR = 'img/deathbar.png'

## Positioning globals
PX_X = gui.size()[0]
PX_Y = gui.size()[1]
CS_XSTART = int(71/1920 * PX_X)
CS_XEND = int(708/1920 * PX_X)
CS_YSTART = int(174/1080 * PX_Y)
CS_YEND = int(974/1080 * PX_Y)

def click_button(button):
    buttonloc = gui.locateCenterOnScreen(button, confidence = 0.85)
    gui.moveTo(*buttonloc)
    gui.click()

def randclick(x_bounds: tuple, y_bounds: tuple):
    x = randint(*x_bounds)
    y = randint(*y_bounds)
    gui.moveTo(x, y)
    gui.click()

def load_or_create_log():
    if not os.path.isfile('logdata/log.xlsx'):
        df = {
            'run_start': [],
            'run_end': [],
        }
        df = pl.DataFrame(df)
        df.write_excel('logdata/log.xlsx')
    df = pl.read_excel('logdata/log.xlsx', schema_overrides = {
        'run_start': pl.Datetime,
        'run_end': pl.Datetime
    })
    return df

def click_confirm():
    try:
        click_button(CHALLENGECONFIRM)
    except gui.ImageNotFoundException:
        try:
            click_button(CONFIRMBUTTON)
        except gui.ImageNotFoundException:
            click_button(DARKCONFIRM)
            
def click_play():
    try:
        click_button(MM_PLAYBUTTON)
    except gui.ImageNotFoundException:
        click_button(LIGHTPLAY)

def launch_from_mm():
    # click play
    click_play()
    # select random character
    click_confirm()
    # click forest
    click_button(FOREST)
    # click tier 1
    click_button(TIER1)
    # click challenges
    click_button(MS_CHALLENGES)
    # click afkgaming
    click_button(AFKGAMING)
    # click confirm
    click_confirm()
    # click confirm
    click_confirm()
    
def spin():
    dirs = [
        ('w',),
        ('w', 'd'),
        ('d',),
        ('d', 's'),
        ('s'),
        ('s', 'a'),
        ('a'),
        ('a', 'w')
    ]
    for dir in dirs[::-1]:
        gui.hotkey(*dir)
        t.sleep(0.1)
    
def play():
    region = (1800, 120, 100, 780)
    while True:
        screenshot = np.array(gui.screenshot(region = region))
        gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
        if (gray.mean(axis = 0) == 0).all():
            print('Death Detected')
            break
        spin()
        gui.hotkey('e')

def return_to_main():
    gui.hotkey('enter')
    t.sleep(3)
    gui.hotkey('enter')

def main():
    while True:
        row = DefaultDict(list)
        launch_from_mm()
        row['run_start'] = dt.now()
        t.sleep(10)
        play()
        t.sleep(10)
        row['run_end'] = dt.now()
        rowdf = pl.DataFrame(row)
        log = load_or_create_log()
        log = pl.concat([log, rowdf])
        log.write_excel('logdata/log.xlsx')
        return_to_main()
        t.sleep(10)

if __name__ == "__main__":
    main()
