import os
import pyautogui as gui
import cv2
import time as t
import numpy as np
import polars as pl
from polars import col as c
from typing import DefaultDict
from datetime import datetime as dt, date as d
from random import randint
import argparse as ap
import sys

if getattr(sys, 'frozen', False):
    imgpath = sys._MEIPASS + '/img/'
else:
    imgpath = 'img/'

## Button globals
button_globals = [
    'mmplay.png',
    'confirm.png',
    'challengeconfirm.png',
    'mschallenges.png',
    'afkgaming.png',
    'forest.png',
    'tier1.png',
    'darkconfirm.png',
    'lightplay.png',
    'cantconfirm.png',
    'youded.png',
    'deathbar.png',
]

img_paths = [imgpath + button_png for button_png in button_globals]

MM_PLAYBUTTON = img_paths[0]
CONFIRMBUTTON = img_paths[1]
CHALLENGECONFIRM = img_paths[2]
MS_CHALLENGES = img_paths[3]
AFKGAMING = img_paths[4]
FOREST = img_paths[5]
TIER1 = img_paths[6]
DARKCONFIRM = img_paths[7]
LIGHTPLAY = img_paths[8]
CANTCONFIRM = img_paths[9]
YOUDED = img_paths[10]
DEATHBAR = img_paths[11]

## Positioning globals
PX_X = gui.size()[0]
PX_Y = gui.size()[1]
CS_XSTART = int(71/1920 * PX_X)
CS_XEND = int(708/1920 * PX_X)
CS_YSTART = int(174/1080 * PX_Y)
CS_YEND = int(974/1080 * PX_Y)

def parse_args():
    parser = ap.ArgumentParser()
    parser.add_argument('-c', '--character', required = True, type = str, help = 'character you are playing with, select and return to main menu to run')
    parser.add_argument('-d', '--delay', default = 0, required = False, type = int, help = 'Delay timer for start in case of 1 screen')
    parser.add_argument('-rps', '--rotations-per-second', default = 1, required = False, type = float, help = 'character spin speed, character rotates at {speed} rps, default 1')
    return parser.parse_args()

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
    if not os.path.isdir('logdata'):
        os.mkdir('logdata')
    if not os.path.isfile('logdata/log.xlsx'):
        df = {
            'run_start': [],
            'run_end': [],
            'character': [],
            'rps': []
        }
        df = pl.DataFrame(df)
        df.write_excel('logdata/log.xlsx')
    df = pl.read_excel('logdata/log.xlsx', schema_overrides = {
        'run_start': pl.Datetime,
        'run_end': pl.Datetime,
        'character': pl.String,
        'rps': pl.Float64,
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
        ('w', 'e'),
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
    
def play():
    guisize = gui.size()
    region = (int(1800 / 1920 * guisize.width), int(120 / 1080 * guisize.height), int(100 / 1920 * guisize.width), int(780 / 1080 * guisize.height))
    while True:
        screenshot = np.array(gui.screenshot(region = region))
        gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
        if (gray.mean(axis = 0) == 0).all():
            print('\tDeath Detected')
            break
        spin()
    return dt.now()

def return_to_main():
    gui.hotkey('enter')
    t.sleep(3)
    gui.hotkey('enter')
    
def delay(seconds):
    for i in range(seconds):
        print(f'Waiting {seconds - i} seconds' + (20 * ' '), end = '\r')
        t.sleep(1)
    print(f'Waited {seconds} seconds')

def main():
    gui.PAUSE = 0.1
    args = parse_args()
    print(f'Using RPS of {args.rotations_per_second}')
    delay(args.delay)
    games_logged = 0
    log = load_or_create_log()
    while True:
        try:
            row = DefaultDict(list)
            launch_from_mm()
            t.sleep(6)
            row['run_start'].append(dt.now())
            print(f'Starting run {games_logged + 1} at {row['run_start'][0]}')
            # unlock inputs for a moment for spin speed to take effect
            gui.PAUSE = (1 / args.rotations_per_second) / 8
            row['run_end'].append(play())
            # lock em again
            gui.PAUSE = 0.1
            print(f'\tRun ended at {row['run_end'][0]}')
            print(f'\t\tDuration: {(row['run_end'][0] - row['run_start'][0]).seconds // 60}m, {(row['run_end'][0] - row['run_start'][0]).seconds % 60}s')
            row['character'].append(args.character)
            row['rps'].append(float(args.rotations_per_second))
            rowdf = pl.DataFrame(row)
            log = load_or_create_log()
            log = pl.concat([log, rowdf])
            log.write_excel('logdata/log.xlsx')
            games_logged += 1
            print('\tRun logged')
            t.sleep(10)
            return_to_main()
            t.sleep(10)
        except (KeyboardInterrupt, gui.FailSafeException) as e:
            gui.PAUSE = 0.1
            if e == KeyboardInterrupt:
                print('Recieved keyboard interrupt, ending play loop')
            if e == gui.FailSafeException:
                print('pyautogui detected failsafe activation, ending play loop')
            break
    if games_logged >= 1:
        tdif_df = log\
        .with_columns(
            (c('run_end') - c('run_start')).dt.total_seconds().alias('run_length_s')
        )\
        .tail(games_logged)
        av_tdif = tdif_df['run_length_s'].mean() / 60
        av_tdif_str = f'{int(av_tdif)}m, {round((av_tdif - int(av_tdif)) * 60)}s'
        print(f'__________________\nPlayed and logged {games_logged} runs with average run time of {av_tdif_str}')
    else:
        print('No runs completed or logged')

if __name__ == "__main__":
    main()
