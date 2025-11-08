import pyray as rl
from app.displays.base import BaseDisplay
from app.ui import button
class StartDisplay(BaseDisplay):

    def __init__(self, game):
        super().__init__(game)
        self.button_to_2dgame = button.Button(200, 100, 100, 100, "click to enter 2dgame", 20, rl.WHITE, rl.GRAY, rl.GREEN, rl.RED)
        self.button_to_3dgame = button.Button(400, 100, 100, 100, "click to enter 3dgame", 20, rl.WHITE, rl.GRAY, rl.GREEN, rl.RED)

    def render(self):
        rl.draw_fps(10, 10)
        self.button_to_2dgame.draw()
        self.button_to_3dgame.draw()

    def update(self):
        self.button_to_2dgame.update()
        self.button_to_3dgame.update()
        if self.button_to_3dgame.is_clicked:
            self.game.change_display(self.game.threedgame)
        if self.button_to_2dgame.is_clicked:
            self.game.change_display(self.game.twodgame)
