import pyautogui as p

UP = "W"
DOWN = "S"
LEFT = "A"
RIGHT = "D"
TURN = "H"
START = "G"

def press(key, num):
    for i in xrange(num):
        p.keyDown(key)
        p.keyUp(key)

def move_right(num):
    press(RIGHT, num)

def move_left(num):
    press(LEFT, num)

def move_up(num):
    press(UP, num)

def move_down(num):
    press(DOWN, num)

def move_turn(num):
    press(TURN, num)

def press_start():
    press(START, 1)
