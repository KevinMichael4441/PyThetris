from flask import Flask, render_template, session, request

import random

app = Flask(__name__)
app.secret_key = "moffdnanpampaugagnpavnoy8avnamnvaiuybhanpaiygbnagnaguijagbbiygagaeigb"



@app.get("/")
@app.get("/home")
def display_home():
    return render_template(
    "home.html"
    )


@app.post("/initgame/<row>/<col>")
def get_row_col(row, col):
    session["s_row"] = row
    session["s_col"] = col
    return f"{session["s_row"]} by {session["s_col"]}"


@app.get("/showgrid")
def display_the_grid():
    session["count"] = 0
    return render_template(
        "grid.html",
        rowcount=8,
        colcount=4,
        colour="white",
    )


@app.post("/location/<row>/<col>/<colour>")
def process_the_click(row, col, colour):
    set_colour = "white" if colour == "black" else "black"
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
    return f"You pressed: {key_pressed}."


if __name__ == "__main__":
    app.run(debug=True)
