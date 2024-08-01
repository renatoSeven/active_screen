import pyautogui
import time
import random
import sys
import os
from multiprocessing import Process
from datetime import datetime

def rand_func(start,end,c_quad=0):
    # returns random quadrant(1-4) or random number of seconds
    if c_quad == 0:
        return int(random.randint(start,end))
    else:
        while True:
            rand_quad_res = random.randint(1,4)
            if rand_quad_res != c_quad:
                return rand_quad_res

def rand_quadrant(width,height,c_quad):
    # generate random coordenates on randomly generated screen quandrant
    screen_quad = {
        1:[(10,int(width/2)),(10,int(height/2))],
        2:[(int(width/2),width - 10),(10,int(height/2))],
        3:[(10,int(width/2)),(int(height/2),height - 10)],
        4:[(int(width/2),width - 10),(int(height/2),height - 10)]
    }
    w_start = screen_quad[c_quad][0][0]
    w_end = screen_quad[c_quad][0][1]
    h_start = screen_quad[c_quad][1][0]
    h_end = screen_quad[c_quad][1][1]
    return int(random.randint(w_start,w_end)),int(random.randint(h_start,h_end))

def prog_start_test(width, height):
    # run preliminary tests of screen size
    print(f'[{str(datetime.now())}]Testing screen:')
    time_sleep = .5
    pyautogui.moveTo(int(width / 2), int(height / 2), time_sleep)
    print(f'  - Center... Done')
    pyautogui.moveTo(10, 10, time_sleep)
    print(f'  - Top left... Done')
    pyautogui.moveTo(width - 10, 10, time_sleep)
    print(f'  - Top right... Done')
    pyautogui.moveTo(width - 10, height - 10, time_sleep)
    print(f'  - Bottom right... Done')
    pyautogui.moveTo(10, height - 10, time_sleep)
    print(f'  - Bottom left... Done')
    pyautogui.moveTo(int(width / 2), int(height / 2), time_sleep)
    print(f'  - Center... Done')
    print(f'[{str(datetime.now())}] Tests complete.')
    time.sleep(2)

def count_down(countdown_time):
    # generate animated countdown timer 
    for i in range(countdown_time, 0, -1):
        print(f'Sleeping... |{str('_' * (i - 1))} <{i}sec> ', end = ' \r')
        time.sleep(.99)

def move_mouse():
    # loop that performs motion/right click/escape actions
    print(f'[{str(datetime.now())}] Move mouse started')
    time.sleep(5)
    width, height = pyautogui.size()
    print(f'[{str(datetime.now())}] [screen size] w: {width}px h: {height}px')
    prog_start_test(width, height)
    try:
        # input is in minutes
        runtime = int(sys.argv[1])
        # save original value
        runtime_orig = runtime
    except:
        runtime = False
        pass
    if runtime and runtime > 0:
        runtime = int(runtime * 60) # convert to seconds
        print(f'[{str(datetime.now())}] Runtime will be {runtime_orig} minutes({runtime} seconds)')
    else:
        print(f'[{str(datetime.now())}] Runtime not defined, running indefinitely')
    curr_quad = 1
    rand_sleep_total = 0
    counter = 1
    while True:
        try:
            if runtime and rand_sleep_total > runtime:
                print(f'[{str(datetime.now())}] Runtime reached({runtime} seconds)')
                break
            # generate random quandrant selection different from current
            curr_quad = rand_func(0,0,curr_quad)
            # generate random coordenates on screen based on new quandrant
            width_res, height_res = rand_quadrant(width,height,curr_quad)
            # generate random time of mouse travel 1-3s
            rand_time_res = rand_func(1,3)
            rand_sleep_res = rand_func(20,80)
            rand_sleep_total += rand_sleep_res
            print(f'[{str(datetime.now())}] [move#{"{:03d}".format(counter)}] t:{rand_time_res} <quad{curr_quad}> w:{"{:04d}".format(width_res)} h:{"{:04d}".format(height_res)} sleep:{rand_sleep_res} total:{"{:04d}".format(rand_sleep_total)} ', end='')
            pyautogui.moveTo(width_res, height_res, rand_time_res)
            print('[Rclick] ', end='')
            pyautogui.click(button='right')
            time.sleep(.5)
            print('[esc]')
            pyautogui.press('esc')
            count_down(rand_sleep_res)
            counter += 1
        except Exception as error:
            print(f'[ERROR] {error}')
            time.sleep(60)
            pass

def kb_ctrl_send():
    # loop to notify user were the mouse cursor is
    print(f'[{str(datetime.now())}] Mouse locator started')
    while True:
        pyautogui.press('ctrl')
        time.sleep(.5)
        pyautogui.press('ctrl')
        time.sleep(5)

def proc_manager(proc_name):
    # starts proccesses based on name
    if proc_name == 'mouse1':
        move_mouse()
    else:
        kb_ctrl_send()

if __name__ == '__main__':
    try:
        print(f'[{str(datetime.now())}] Pprogram started ')
        processes = [Process(target=proc_manager, args=(task,)) for task in ['mouse1','mouse2']]
        # start all processes
        for process in processes:
            process.start()
        # wait for all processes to complete
        for process in processes:
            process.join()
    except KeyboardInterrupt:
        print(f'[{str(datetime.now())}]Interrupted')
        try:
            sys.exit(130)
        except SystemExit:
            os._exit(130)
