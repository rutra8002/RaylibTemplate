import pyray as rl
from app.displays.base import BaseDisplay
from app.ui import button
class StartDisplay(BaseDisplay):

    def __init__(self, game):
        super().__init__(game)
        self.button_to_game = button.Button(100, 100, 100, 100, "click to enter 2dgame", 20, rl.WHITE, rl.GRAY, rl.GREEN, rl.RED)

    def render(self):
        rl.draw_fps(10, 10)
        self.button_to_game.draw()

    def update(self):
        self.button_to_game.update()
        if self.button_to_game.is_clicked:
            self.game.change_display(self.game.twodgame)
