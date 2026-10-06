_ROWS = 10
_COLUMNS = 5
_INTERVAL = 0.3
_BLANK = "  "
_BLOCK = "\u2588\u2588"
_FRAMETIME = 0.1
_EMPTYLIST = [None,None]


import time
import sys
from pynput import keyboard
import random


def clear_the_terminal():
    sys.stdout.write("\033[2J\033[H")    # ANSI escape which clears the current terminal screen.
    sys.stdout.flush()


def build_clean_grid():
    return [["  " for i in range(_ROWS)] for i in range(_COLUMNS)]

def display_grid(grid):
    the_columns = tuple(range(0, _COLUMNS))
    the_rows = tuple(range(0, _ROWS))
    for r in the_rows:
        print("|", sep="", end="")
        for c in the_columns:
            print(grid[c][r], "|", sep="", end="")
        print()



key_pressed = None
def process_on_press(key):
    global key_pressed
    try:
        key_pressed = key.char
    except AttributeError:
        key_pressed = str(key)


# Everything below is purely my work


def game():
    # Setting up
    global key_pressed
    grid = build_clean_grid()
    activeBlock = _EMPTYLIST
    currentFrameTime = 0
    frameTime = 0 #ms 

    listener = keyboard.Listener( on_press=process_on_press )
    listener.start()

    display_grid(grid)
    
    while(True):
        currentFrameTime = time.time()
        
        # Set an activeBlock - block that falls
        if (activeBlock[0] == None):
            activeBlock[0] = 0
            activeBlock[1] = random.randint(0,_COLUMNS-1)
            #activeBlock[1] = 2
            
            if (grid[activeBlock[1]][activeBlock[0]]) == _BLOCK:
                break
            
            grid[activeBlock[1]][activeBlock[0]] = _BLOCK
            
            clear_the_terminal()
            display_grid(grid)

        # Checking if key pressed in every update
        if key_pressed:
            if key_pressed == "Key.left":
                if activeBlock[1] - 1 >= 0:
                    if grid[activeBlock[1] - 1][activeBlock[0]] == _BLANK:
                        grid[activeBlock[1]][activeBlock[0]] = _BLANK
                        activeBlock[1] -= 1
                        grid[activeBlock[1]][activeBlock[0]] = _BLOCK
            elif key_pressed == "Key.right":
                if activeBlock[1] + 1 <= 4:
                    if grid[activeBlock[1] + 1][activeBlock[0]] == _BLANK:
                        grid[activeBlock[1]][activeBlock[0]] = _BLANK
                        activeBlock[1] += 1
                        grid[activeBlock[1]][activeBlock[0]] = _BLOCK

            print(activeBlock[0], activeBlock[1])
            clear_the_terminal()
            display_grid(grid)
            key_pressed = None

        
        # Updating dt (and moving block down if dt is over threshold)
        frameTime += (time.time() - currentFrameTime) 
        if frameTime > _FRAMETIME:
            #print(frameTime)
            frameTime = 0
            
            #drop block one level down
            if activeBlock[0] + 1 == _ROWS: #last row
                activeBlock[0] = None
            elif grid[activeBlock[1]][activeBlock[0]+1] == _BLOCK:  # there's block below
                activeBlock[0] = None
            else:
                grid[activeBlock[1]][activeBlock[0]] = _BLANK
                activeBlock[0] += 1
                grid[activeBlock[1]][activeBlock[0]] = _BLOCK
                
                
            print(activeBlock[0], activeBlock[1])    
            clear_the_terminal()
            display_grid(grid)
            
            
    print("\n\nGAME OVER! WOMP WOMP! GO CRY!")        
     
    listener.stop()

        

        