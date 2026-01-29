import pyray as rl

from app.displays import startscreen, twodgame, threedgame
from app.input.keyboard import KeyboardManager


class Game:
    def __init__(self):
        self.width, self.height = 800, 600
        rl.init_window(self.width, self.height, "raylib template?")
        rl.set_exit_key(rl.KeyboardKey.KEY_NULL)
        self.bloom_shader = rl.load_shader("", "app/shaders/bloom.fs")
        self.base_display = startscreen.StartDisplay(self)
        self.twodgame = twodgame.TwoDGameDisplay(self)
        self.threedgame = threedgame.ThreeDGameDisplay(self)
        self.current_display = self.base_display

        self.keyboard = KeyboardManager()

        # controller
        self.gamepad_id = 0
        self.gamepad_deadzone = 0.25
        self.gamepad_enabled = False
        self.gamepad_name = ""
        self.gamepad_name_blacklist = ("touchpad")

    def update_gamepad_status(self):
        # Detect availability each frame (hot-plug support)
        available = rl.is_gamepad_available(self.gamepad_id)
        name = rl.get_gamepad_name(self.gamepad_id) if available else ""
        self.gamepad_name = name or ""
        lowered = self.gamepad_name.lower()
        is_blacklisted = any(token in lowered for token in self.gamepad_name_blacklist)
        self.gamepad_enabled = available and not is_blacklisted

    def change_display(self, display):
        self.current_display = display

    def loop(self):
        while not rl.window_should_close():
            self.update()
            self.render()

    def render(self):
        rl.begin_drawing()
        self.current_display.render()
        #debug thingy
        rl.draw_text(str(self.current_display), 10, 100, 20, rl.WHITE)
        rl.end_drawing()

    def update(self):
        self.update_gamepad_status()
        self.update_joystick()
        self.keyboard.update()
        self.current_display.update()

    def update_joystick(self):
        if self.gamepad_enabled:
            self.left_joystick_x = rl.get_gamepad_axis_movement(self.gamepad_id, rl.GamepadAxis.GAMEPAD_AXIS_LEFT_X)
            self.left_joystick_y = rl.get_gamepad_axis_movement(self.gamepad_id, rl.GamepadAxis.GAMEPAD_AXIS_LEFT_Y)
            self.right_joystick_x = rl.get_gamepad_axis_movement(self.gamepad_id, rl.GamepadAxis.GAMEPAD_AXIS_RIGHT_X)
            self.right_joystick_y = rl.get_gamepad_axis_movement(self.gamepad_id, rl.GamepadAxis.GAMEPAD_AXIS_RIGHT_Y)
            if abs(self.left_joystick_x) < self.gamepad_deadzone:
                self.left_joystick_x = 0.0
            if abs(self.left_joystick_y) < self.gamepad_deadzone:
                self.left_joystick_y = 0.0
            if abs(self.right_joystick_x) < self.gamepad_deadzone:
                self.right_joystick_x = 0.0
            if abs(self.right_joystick_y) < self.gamepad_deadzone:
                self.right_joystick_y = 0.0
