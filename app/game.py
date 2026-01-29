import pyray as rl

from app.displays import startscreen, twodgame, threedgame
from app.input.keyboard import KeyboardManager, KeyboardAction
from app.audio_manager import AudioManager


class Game:
    def __init__(self):
        self.width, self.height = 800, 600
        rl.init_window(self.width, self.height, "raylib template?")
        rl.set_exit_key(rl.KeyboardKey.KEY_NULL)
        rl.init_audio_device()
        self.audio = AudioManager()
        self.bloom_shader = rl.load_shader("", "app/shaders/bloom.fs")
        self.base_display = startscreen.StartDisplay(self)
        self.twodgame = twodgame.TwoDGameDisplay(self)
        self.threedgame = threedgame.ThreeDGameDisplay(self)
        self.current_display = self.base_display
        self.current_display.on_enter()
        self.debug_enabled = False

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
        if self.current_display is not None:
            self.current_display.on_exit()
        self.current_display = display
        self.current_display.on_enter()

    def loop(self):
        while not rl.window_should_close():
            self.update()
            self.render()
        self.audio.shutdown()
        rl.close_window()

    def render(self):
        rl.begin_drawing()
        self.current_display.render()
        if self.debug_enabled:
            self._draw_debug_overlay()
        #debug thingy
        rl.draw_text(str(self.current_display), 10, 100, 20, rl.WHITE)
        rl.end_drawing()

    def update(self):
        self.update_gamepad_status()
        self.update_joystick()
        self.keyboard.update()
        if self.keyboard.is_pressed(KeyboardAction.DEBUG_TOGGLE):
            self.debug_enabled = not self.debug_enabled
        self.audio.update()
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

    def _format_debug_value(self, value):
        if isinstance(value, (int, float, str, bool, type(None))):
            return repr(value)
        text = repr(value)
        if len(text) > 80:
            text = f"{text[:77]}..."
        return text

    def _draw_debug_overlay(self):
        display = self.current_display
        lines = [f"Display: {display.__class__.__name__}"]
        for key in sorted(vars(display)):
            value = self._format_debug_value(getattr(display, key))
            lines.append(f"{key} = {value}")
        x, y = 10, 10
        size = 16
        for line in lines:
            rl.draw_text(line, x, y, size, rl.YELLOW)
            y += size + 4
