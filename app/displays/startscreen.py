import pyray as rl
from app.displays.base import BaseDisplay
from app.displays.settings import SettingsDisplay
from app.ui import button
from app.ui import menu
class StartDisplay(BaseDisplay):

    def __init__(self, game):
        super().__init__(game)
        self.button_to_2dgame = button.Button(self.game, 200, 80, 140, 80, "2D Game", 20, rl.WHITE, rl.GRAY, rl.GREEN, rl.RED)
        self.button_to_3dgame = button.Button(self.game, 200, 190, 140, 80, "3D Game", 20, rl.WHITE, rl.GRAY, rl.GREEN, rl.RED)
        self.button_to_settings = button.Button(self.game, 200, 300, 140, 80, "Settings", 20, rl.WHITE, rl.GRAY, rl.GREEN, rl.RED)
        self.buttons = [self.button_to_2dgame, self.button_to_3dgame, self.button_to_settings]
        self.menu = menu.MenuController(self.game, self.buttons)

    def render(self):
        super().render()
        rl.draw_fps(10, 10)
        for b in self.buttons:
            b.draw()

    def update(self):
        self.menu.update()
        if self.button_to_3dgame.is_clicked:
            self.game.change_display(self.game.threedgame)
        if self.button_to_2dgame.is_clicked:
            self.game.change_display(self.game.twodgame)
        if self.button_to_settings.is_clicked:
            self.game.change_display(SettingsDisplay(self.game, self))
