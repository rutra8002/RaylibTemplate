import pyray as rl
from raylib.colors import WHITE

from app.displays import base

class Game:
    def __init__(self):
        width, height = 800, 600
        rl.init_window(width, height, "raylib template?")
        self.base_display = base.BaseDisplay(self)
        self.current_display = self.base_display


    def loop(self):
        while not rl.window_should_close():
            self.current_display.update()
            self.render()

    def render(self):
        rl.begin_drawing()
        rl.clear_background(rl.BLACK)
        self.current_display.render()
        #debug thingy
        rl.draw_text(str(self.current_display), 10, 100, 20, WHITE)
        rl.end_drawing()

    def update(self):
        self.current_display.update()

