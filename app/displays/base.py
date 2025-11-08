import pyray as rl
class BaseDisplay:
    def __init__(self, game):
        self.game = game

    def __str__(self):
        return self.__class__.__name__

    def render(self):
        rl.draw_fps(10, 10)

    def update(self):
        pass
