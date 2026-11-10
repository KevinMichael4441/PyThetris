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

_COLOURS = [_BLACK, _RED, _BLUE, _YELLOW, _GREEN, _ORANGE]

@app.get("/home")
def display_home():
    return render_template(
    "home.html"
    )


@app.get("/")
@app.get("/showgrid")
def init_the_grid():
    session["count"] = 0
    session["activeBlock"] = [None,None]
    session["activeColour"] = None
    
    session["rows"] = 10
    session["cols"] = 5
    session["grid"] = [[_BLACK for i in range(session["rows"])] for i in range(session["cols"])]
   
    return render_template(
        "grid.html",
        rowcount=session["rows"],
        colcount=session["cols"],
        grid = session["grid"]
    )


@app.post("/location/<row>/<col>/<colour>")
def process_the_click(row, col, colour):
    set_colour = "white" if colour == "black" else "black"
    session["grid"][row][col] = set_colour
    return render_template(
        "snippet.html",
        row=row,
        col=col,
        colour=set_colour,
    )




@app.post("/counting")
def maintain_count():
    session["count"] = session["count"] + 1
    return "Time is ticking: " + str(session["count"])


@app.post("/keypress")
def which_key_pressed():
    key_pressed = request.form["keyPressed"]
    if key_pressed == "ArrowLeft":
        move_left()
    elif key_pressed == "ArrowRight":
        move_right()
    return f"You Pressed {key_pressed}"



def move_left():
    if session["activeBlock"][0] == None:
        return
    if session["activeBlock"][1] - 1 >= 0:
        if session["grid"][session["activeBlock"][1] - 1][session["activeBlock"][0]] == _BLACK:
            session["grid"][session["activeBlock"][1]][session["activeBlock"][0]] = _BLACK
            session["activeBlock"][1] -= 1
            session["grid"][session["activeBlock"]][session["activeBlock"][0]] = session["activeColour"]
    #self.refresh()
    # UPDATE GRID
    
def move_right():
    if session["activeBlock"][0] == None:
        return
    if session["activeBlock"][1] + 1 <= session["cols"] - 1:
        if session["grid"][session["activeBlock"][1] + 1][session["activeBlock"][0]] == _BLACK:
            session["grid"][session["activeBlock"][1]][session["activeBlock"][0]] = _BLACK
            session["activeBlock"][1] += 1
            session["grid"][session["activeBlock"][1]][session["activeBlock"][0]] = session["activeColour"]
    #self.refresh()
    # UPDATE GRID

if __name__ == "__main__":
    app.run(debug=True)
