import pyray as rl
from app.displays.base import BaseDisplay
from app.cameras import twodcamera


class TwoDGameDisplay(BaseDisplay):
    def __init__(self, game):
        super().__init__(game)
        self.square_pos = [200, 200]
        self.speed = 200
        self.delta_time = rl.get_frame_time()
        self.camera = twodcamera.Camera(self.game.width, self.game.height, self.square_pos[0], self.square_pos[1], 3)

    def render(self):
        self.camera.begin_mode()
        rl.draw_fps(10, 10)
        rl.draw_rectangle(int(self.square_pos[0]), int(self.square_pos[1]), 20, 20, rl.RED)
        self.camera.end_mode()

    def update(self):
        self.delta_time = rl.get_frame_time()
        self.camera.update_target(self.square_pos[0], self.square_pos[1], self.delta_time)
        if rl.is_key_down(rl.KeyboardKey.KEY_W):
            self.square_pos[1] -= self.speed * self.delta_time
        if rl.is_key_down(rl.KeyboardKey.KEY_S):
            self.square_pos[1] += self.speed * self.delta_time
        if rl.is_key_down(rl.KeyboardKey.KEY_A):
            self.square_pos[0] -= self.speed * self.delta_time
        if rl.is_key_down(rl.KeyboardKey.KEY_D):
            self.square_pos[0] += self.speed * self.delta_time
