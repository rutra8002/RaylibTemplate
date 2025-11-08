import pyray as rl
from app.displays.base import BaseDisplay
from app.cameras import threedcamera


class ThreeDGameDisplay(BaseDisplay):
    def __init__(self, game):
        super().__init__(game)
        self.cube_pos = [0.0, 1.0, 0.0]
        self.speed = 10
        self.camera = threedcamera.Camera(
            self.cube_pos[0], self.cube_pos[1], self.cube_pos[2],
            (0, 6, 8),
            3.0,
            60.0
        )

    def update(self):
        dt = rl.get_frame_time()
        if rl.is_key_down(rl.KeyboardKey.KEY_W):
            self.cube_pos[2] -= self.speed * dt
        if rl.is_key_down(rl.KeyboardKey.KEY_S):
            self.cube_pos[2] += self.speed * dt
        if rl.is_key_down(rl.KeyboardKey.KEY_A):
            self.cube_pos[0] -= self.speed * dt
        if rl.is_key_down(rl.KeyboardKey.KEY_D):
            self.cube_pos[0] += self.speed * dt
        self.camera.update_target(self.cube_pos[0], self.cube_pos[1], self.cube_pos[2], dt)

    def render(self):
        self.camera.begin_mode()
        rl.draw_grid(40, 1.0)
        pos = rl.Vector3(self.cube_pos[0], self.cube_pos[1], self.cube_pos[2])
        rl.draw_cube(pos, 1.0, 1.0, 1.0, rl.RED)
        rl.draw_cube_wires(pos, 1.0, 1.0, 1.0, rl.BLACK)
        self.camera.end_mode()

        rl.draw_fps(10, 10)
