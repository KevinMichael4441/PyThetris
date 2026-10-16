from textual.app import App, ComposeResult # The main application
from textual.containers import ScrollableContainer
from textual.widgets import Button, Footer, Header, Static
from textual.theme import Theme
from textual.strip import Strip
from textual.widget import Widget
from rich.segment import Segment
from textual.geometry import Size, Offset, Region
from textual.scroll_view import ScrollView
from rich.style import Style
from time import monotonic
from textual.reactive import reactive

_INTERVAL = 0.3
_FRAMETIME = 0.1

g_time = 0

tetris_theme = Theme(   
    name="tetris",
    primary="#88C0D0",
    secondary="#81A1C1",
    accent="#B48EAD",
    foreground="#D8DEE9",
    background="#2E3440",
    success="#A3BE8C",
    warning="#B88CBE",
    error="#BF616A",
    #surface="#B4252",
    panel="#434C5E",
    dark=True,
    variables={   
        "block-cursor-text-style": "none",
        "footer-key-foreground": "#88C0D0",        
        "input-selection-background": "#81a1c1 35%",  
    },
)

import time
import sys
from pynput import keyboard
import random


   
_BLACK = "grey0"
_RED = "red"
_BLUE = "blue3"
_YELLOW = "yellow3"
_GREEN = "dark_green"
_ORANGE = "orange3"

_COLORS = [_RED, _BLUE, _YELLOW, _GREEN, _ORANGE]
_NUMCOLS = 5

class TetrisGrid(Widget):

    start_time = reactive(monotonic)
    time = reactive(0.0)
    total = reactive(0.0)
  
    def __init__(self, rows, columns: int) -> None:
        super().__init__()
        self.rows = rows
        self.columns = columns
        self.grid = [[_BLACK for i in range(self.rows)] for i in range(self.columns)]      # setting all block to black
        self.activeBlock = [None, None]
        self.frameTime = 0
        self.currentFrameTime = monotonic()
        
        
    def on_mount(self) -> None:
        global _INTERVAL
        # Call self.tick every _INTERVAL seconds
        self.set_interval(_INTERVAL, self.tick)
        self.tick()  # immediate first update

    def tick(self) -> None:
        global _FRAMETIME
        global g_time
        

        
        self.time = self.total + (monotonic() - self.start_time)
        
        self.previoousFrameTime = self.currentFrameTime
        self.currentFrameTime = monotonic() 
        
        
        # Set an activeBlock - block that falls
        if (self.activeBlock[0] == None):
            self.activeBlock[0] = 0
            self.activeBlock[1] = random.randint(0,self.columns-1)
            self.activeColor = _COLORS[random.randint(0, _NUMCOLS-1)]
            #activeBlock[1] = 2
            
            if (self.grid[self.activeBlock[1]][self.activeBlock[0]]) != _BLACK:
                g_time = self.time
                self.remove()
                
            
            self.grid[self.activeBlock[1]][self.activeBlock[0]] = self.activeColor
            
            
        # Updating dt (and moving block down if dt is over threshold)
        self.frameTime += (self.currentFrameTime - self.previoousFrameTime) 
        if self.frameTime > _FRAMETIME:
            #print(frameTime)
            self.frameTime = 0
            rowToPass = self.activeBlock[0]
            
            #drop block one level down
            if self.activeBlock[0] + 1 == self.rows: #last row
                self.activeBlock[0] = None
            elif self.grid[self.activeBlock[1]][self.activeBlock[0]+1] != _BLACK:  # there's block below
                self.activeBlock[0] = None
            else:
                self.grid[self.activeBlock[1]][self.activeBlock[0]] = _BLACK
                self.activeBlock[0] += 1
                self.grid[self.activeBlock[1]][self.activeBlock[0]] = self.activeColor
                
                

            def isRowFilled(t_grid, t_currentRow, t_maxCols):
                colCount = 0;
    
                for col in t_grid:
                    if col[t_currentRow] != _BLACK:
                        colCount += 1;
    
                if colCount == t_maxCols:
                    return True
                else:
                    return False   
                    
                    
            def clearRow(t_grid, t_currentRow, t_maxCols):
                for i in range(t_currentRow, -1, -1):
                    for col in range(t_maxCols):
                        if t_currentRow - 1 >= 0:
                            t_grid[col][t_currentRow] = t_grid[col][t_currentRow - 1]
            
                    t_currentRow -= 1
                
                return t_grid
            
                
            if isRowFilled(self.grid, rowToPass, self.columns):
                self.grid = clearRow(self.grid, rowToPass, self.columns)
    
        self.refresh()
        
    def move_left(self):
        if self.activeBlock[0] == None:
            return
        if self.activeBlock[1] - 1 >= 0:
            if self.grid[self.activeBlock[1] - 1][self.activeBlock[0]] == _BLACK:
                self.grid[self.activeBlock[1]][self.activeBlock[0]] = _BLACK
                self.activeBlock[1] -= 1
                self.grid[self.activeBlock[1]][self.activeBlock[0]] = self.activeColor
        self.refresh()
    
    def move_right(self):
        if self.activeBlock[0] == None:
            return
        if self.activeBlock[1] + 1 <= self.columns - 1:
            if self.grid[self.activeBlock[1] + 1][self.activeBlock[0]] == _BLACK:
                self.grid[self.activeBlock[1]][self.activeBlock[0]] = _BLACK
                self.activeBlock[1] += 1
                self.grid[self.activeBlock[1]][self.activeBlock[0]] = self.activeColor
        self.refresh()
    
    def render_line(self, y: int) -> Strip:
        """Render a line of the widget. y is relative to the top of the widget."""
        
        row_index = y // 2  # four lines per row
        cell_width = 2
        total_width = cell_width * self.columns

        
        if row_index >= self.rows:
            return Strip.blank(self.size.width)
         

        #for col in self.columns:
        #    for row in self.rows:
                
        segments = []
        for c in range(self.columns):
            value = self.grid[c][row_index]
            if value == _BLACK:
                style = Style(bgcolor = _BLACK)
            else:
                style = Style(bgcolor = value)
            segments.append(Segment(" " * cell_width, style))
            
        strip = Strip(segments, total_width)
        return strip


class Menu(Widget):
    def compose(self):
        yield Button("10x5", id="Large", variant="success", classes = "box")
        yield Button("8x4", id="Medium", variant="warning", classes = "box")
        yield Button("4x2", id="Small", variant="success", classes = "box")
        yield Button("6x7", id="Funny", variant="warning", classes = "box")
        
class End(Widget):
    def compose(self):
        global g_time
        
        minutes, seconds = divmod(time, 60)
        hours, minutes = divmod(minutes, 60)
        
        message = f"Your name in {hours:02,.0f}:{minutes:02.0f}:{seconds:05.2f}"
        
        yield Static(message)

class Tetris(App):    # Function for the main application
    BINDINGS = [
            # (key, action name, description)
            ("d", "toggle_dark_mode", "To Toggle Dark Mode"),
            ("left", "move_left", "To move left"),
            ("right", "move_right", "To move Right"),
        ]
       
     
    CSS_PATH = "tetris.tcss"    
    
    
    
    def on_mount(self) -> None:
    # Register the theme
        self.register_theme(tetris_theme)  
    # Set the app's theme
        self.theme = "tetris"
    
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        # Event handler for button pressed in menu
        button_id = event.button.id
        global gridSelected
        
        if button_id == "Large":
            _ROWS = 10
            _COLUMNS = 5
        elif button_id == "Medium":
            _ROWS = 8
            _COLUMNS = 4
        elif button_id == "Small":
            _ROWS = 4
            _COLUMNS = 2
        elif button_id == "Funny":
            _ROWS = 6
            _COLUMNS = 7
        
        gridSelected = True
        menu = self.query_one(Menu)
        menu.remove()
       
        self.mount(TetrisGrid(_ROWS, _COLUMNS)) 
        self.mount(End())
        

    
    
    def compose(self):      # What  widgets  is this app composed of?   
        
        # Some widgets don't matter the order which you yield them; But yield Button("") for example
        yield Header(show_clock = True)
        yield Footer()
        
        # yield widgets inside a coontainer. You can name the container as well
        yield Menu()
            
        
    # Action methods should start with action and these are what's associated to actions.
    def action_toggle_dark_mode(self):
        self.theme = (            
                        "textual-dark" if self.theme == "textual-light" else "textual-light"
                    )
    
    def action_move_left(self):
        try:
            grid = self.query_one(TetrisGrid)
            grid.move_left()
        except:
            pass
        
    def action_move_right(self):
        try:
            grid = self.query_one(TetrisGrid)
            grid.move_right()
        except:
            pass


if __name__ == "__main__":  # Running the application on main   
    Tetris().run()





















def clear_the_terminal():
    sys.stdout.write("\033[2J\033[H")    # ANSI escape which clears the current terminal screen.
    sys.stdout.flush()


def build_clean_grid():
    global _ROWS
    global _COLUMNS
    return [["  " for i in range(_ROWS)] for i in range(_COLUMNS)]

def display_grid(grid):
    global _ROWS
    global _COLUMNS
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




# Func to check if is filled.
def isRowFilled(t_grid, t_currentRow, t_maxCols):
    colCount = 0;
    print("CURRENT ROW: ")
    print(t_currentRow)
    
    for col in t_grid:
        if col[t_currentRow] == _BLOCK:
            colCount += 1;
    
    if colCount == t_maxCols:
        return True
    else:
        return False
        
        
        
# Searched up syntax for negative range    
# Func to clear za row
def clearRow(t_grid, t_currentRow, t_maxCols):

    for i in range(t_currentRow, -1, -1):
        for col in range(t_maxCols):
            if t_currentRow - 1 >= 0:
                t_grid[col][t_currentRow] = t_grid[col][t_currentRow - 1]
            
        t_currentRow -= 1
        
    return t_grid



def startGame():
    global key_pressed
    global _ROWS
    global _COLUMNS
    
    
    print("Z for 10x5 grid")
    print("X for 8x4 grid")
    print("C for 4x2 grid")
    
    while True:
        if key_pressed == "z":
            
            _ROWS = 10
            _COLUMNS = 5
            key_pressed = None
            return
        elif key_pressed == "x":
            _ROWS = 8
            _COLUMNS = 4
            key_pressed = None
            return
        elif key_pressed == "c":
            _ROWS = 4
            _COLUMNS = 2
            key_pressed = None
            return;
            


def game():
    # Setting up
    global key_pressed
    global _ROWS
    global _COLUMNS
   
    listener = keyboard.Listener( on_press=process_on_press )
    listener.start()

    startGame()
    
    
    grid = build_clean_grid()
    activeBlock = _EMPTYLIST
    currentFrameTime = 0
    frameTime = 0 #ms 


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
                if activeBlock[1] + 1 <= _COLUMNS - 1:
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
            rowToPass = activeBlock[0]
            
            #drop block one level down
            if activeBlock[0] + 1 == _ROWS: #last row
                activeBlock[0] = None
            elif grid[activeBlock[1]][activeBlock[0]+1] == _BLOCK:  # there's block below
                activeBlock[0] = None
            else:
                grid[activeBlock[1]][activeBlock[0]] = _BLANK
                activeBlock[0] += 1
                grid[activeBlock[1]][activeBlock[0]] = _BLOCK
                
                
                
            if isRowFilled(grid, rowToPass, _COLUMNS):
                grid = clearRow(grid, rowToPass, _COLUMNS)
                
            print(activeBlock[0], activeBlock[1])    
            clear_the_terminal()
            display_grid(grid)
            
            
    print("\n\nGAME OVER! WOMP WOMP! GO CRY!")        
     
    listener.stop()

        

        