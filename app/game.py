import pyray as rl

from app.displays import startscreen, twodgame, threedgame


class Game:
    def __init__(self):
        self.width, self.height = 800, 600
        rl.init_window(self.width, self.height, "raylib template?")
        self.base_display = startscreen.StartDisplay(self)
        self.twodgame = twodgame.TwoDGameDisplay(self)
        self.threedgame = threedgame.ThreeDGameDisplay(self)
        self.current_display = self.base_display


    def change_display(self, display):
        self.current_display = display

    def loop(self):
        while not rl.window_should_close():
            self.update()
            self.render()

    def render(self):
        rl.begin_drawing()
        rl.clear_background(rl.BLACK)
        self.current_display.render()
        #debug thingy
        rl.draw_text(str(self.current_display), 10, 100, 20, rl.WHITE)
        rl.end_drawing()

    def update(self):
        self.current_display.update()

