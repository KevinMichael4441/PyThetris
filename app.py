from flask import Flask, render_template, session, request

import random

app = Flask(__name__)
app.secret_key = "moffdnanpampaugagnpavnoy8avnamnvaiuybhanpaiygbnagnaguijagbbiygagaeigb"

_BLACK = "black"
_RED = "red"
_BLUE = "blue"
_YELLOW = "yellow"
_GREEN = "green"
_ORANGE = "orange"

_COLOURS = [_RED, _BLUE, _YELLOW, _GREEN, _ORANGE]
_NUM_COLOURS = 5

@app.get("/home")
def display_home():
    return render_template(
    "home.html"
    )


@app.get("/")
@app.get("/initgrid")
def init_the_grid():
    session["count"] = 0
    session["activeBlock"] = [None,None]
    session["activeColour"] = None
    session["gameOver"] = False
    
    session["rows"] = 5
    session["cols"] = 3
    session["grid"] = [[_BLACK for i in range(session["rows"])] for i in range(session["cols"])]
   
    return render_template(
        "grid.html",
        rowcount=session["rows"],
        colcount=session["cols"],
        grid = session["grid"]
    )


@app.post("/keypress")
def which_key_pressed():
    key_pressed = request.form["keyPressed"]
    if key_pressed == "ArrowLeft":
        move_left()
    elif key_pressed == "ArrowRight":
        move_right()
    
    return render_template(
        "grid.html",
        rowcount=session["rows"],
        colcount=session["cols"],
        grid = session["grid"],
        gameover = session["gameOver"], 
        message = calculate_time()
    )



# SHOULD BE RUN EVERY SECOND
@app.post("/update_grid")
def update_grid():
    
    if (session["activeBlock"][0] == None):
        session["activeBlock"][0] = -1
        session["activeBlock"][1] = random.randint(0,session["cols"]-1)
        session["activeColour"] = _COLOURS[random.randint(0, _NUM_COLOURS-1)]
        #activeBlock[1] = 2
        
        if (session["grid"][session["activeBlock"][1]][0]) != _BLACK: 
            session["gameOver"] = True
    
    
    rowToPass = session["activeBlock"][0]
            
    #drop block one level down
    if session["activeBlock"][0] + 1 == session["rows"]: #last row
        session["activeBlock"][0] = None
    elif session["grid"][session["activeBlock"][1]][session["activeBlock"][0]+1] != _BLACK:  # there's block below
        session["activeBlock"][0] = None
    else:
        session["grid"][session["activeBlock"][1]][session["activeBlock"][0]] = _BLACK
        session["activeBlock"][0] += 1
        session["grid"][session["activeBlock"][1]][session["activeBlock"][0]] = session["activeColour"]
        
        

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

        
    if isRowFilled(session["grid"], rowToPass, session["cols"]):
        session["grid"] = clearRow(session["grid"], rowToPass, session["cols"])


    
        
  
    grid = session["grid"]
    print(grid)
    
    
    return render_template(
        "grid.html",
        rowcount=session["rows"],
        colcount=session["cols"],
        grid = session["grid"],
        gameover = session["gameOver"],
        message = calculate_time()
    )
    
    
def calculate_time():
    session["count"] = session["count"] + 1
    # Format the elapsed time - MY CODE
    minutes, seconds = divmod(session["count"], 60)
    hours, minutes = divmod(minutes, 60)
    
    #g_score = (int)(((hours * 3600) + (minutes * 60) + (seconds * 0.5)) + g_numBlocksProcessed) * g_scoreMultiplier
    
    message = f"You have played for {hours:02.0f}:{minutes:02.0f}:{seconds:05.2f}"# and recieved a score of {g_score}"
    
    return message


def move_left():
    session["count"] = session["count"] - 1
    
    if session["activeBlock"][0] == None:
        return
    if session["activeBlock"][1] - 1 >= 0:
        if session["grid"][((session["activeBlock"][1]) - 1)][session["activeBlock"][0]] == _BLACK:
            session["grid"][session["activeBlock"][1]][session["activeBlock"][0]] = _BLACK
            session["activeBlock"][1] -= 1
            session["grid"][session["activeBlock"][1]][session["activeBlock"][0]] = session["activeColour"]
    
    
def move_right():
    session["count"] = session["count"] - 1
    
    if session["activeBlock"][0] == None:
        return
    if session["activeBlock"][1] + 1 <= session["cols"] - 1:
        if session["grid"][((session["activeBlock"][1]) + 1)][session["activeBlock"][0]] == _BLACK:
            session["grid"][(session["activeBlock"][1])][(session["activeBlock"][0])] = _BLACK
            session["activeBlock"][1] += 1
            session["grid"][(session["activeBlock"][1])][(session["activeBlock"][0])] = session["activeColour"]


if __name__ == "__main__":
    app.run(debug=True)
