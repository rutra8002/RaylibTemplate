import pyray as rl

class BaseDisplay:
    def __init__(self, game):
        self.game = game

    def __str__(self):
        return self.__class__.__name__

    def on_enter(self):
        # Default behavior: pause music when entering non-game displays.
        if hasattr(self.game, "audio"):
            self.game.audio.pause_music()

    def on_exit(self):
        pass

    def render(self):
        rl.clear_background(rl.BLACK)

    def update(self):
        pass
