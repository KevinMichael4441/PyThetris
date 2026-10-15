from textual.app import App # The main application
from textual.containers import ScrollableContainer
from textual.widgets import Button, Footer, Header, Static

# class x(y) means x is inherited from y
class TimeDisplay(Static):
    pass

# Creating a custom widget ^ and below. yield Buttons and stuff as you want
class StopWatch(Static):
    def compose(self):
        yield Button("Start")
        yield Button("Stop")
        yield Button("Reset")
        yield TimeDisplay("00:00:00.00")
    


class StopwatchApp(App):    # Function for the main application
    BINDINGS = [
            # (key, action name, description)
            ("d", "toggle_dark_mode", "To Toggle Dark Mode"),
        ]
       
     
    CSS_PATH = "stopwatch.tcss"    
    
    def compose(self):      # What  widgets  is this app composed of?   
        
        # Some widgets don't matter the order which you yield them; But yield Button("") for example
        yield Header(show_clock = True)
        yield Footer()
        
        # yield widgets inside a coontainer. You can name the container as well
        with ScrollableContainer(id = "stopwatches"):
            yield StopWatch()
            yield StopWatch()
            yield StopWatch()
        
        
    # Action methods should start with action and these are what's associated to actions.
    def action_toggle_dark_mode(self):
        self.theme = (            
                        "textual-dark" if self.theme == "textual-light" else "textual-light"
                    )
    
if __name__ == "__main__":  # Running the application on main
    StopwatchApp().run()