import pyray as rl


class Slider:
    def __init__(
        self,
        game,
        x,
        y,
        width,
        height,
        min_value=0.0,
        max_value=1.0,
        value=1.0,
        step=0.05,
        track_color=rl.DARKGRAY,
        fill_color=rl.GREEN,
        knob_color=rl.WHITE,
        focused_color=rl.YELLOW,
    ):
        self.game = game
        self.rect = rl.Rectangle(x, y, width, height)
        self.min_value = float(min_value)
        self.max_value = float(max_value)
        self.step = float(step)
        self.value = self._clamp(value)
        self.track_color = track_color
        self.fill_color = fill_color
        self.knob_color = knob_color
        self.focused_color = focused_color
        self.is_focused = False
        self.is_dragging = False

    def _clamp(self, value):
        return max(self.min_value, min(self.max_value, float(value)))

    def _set_from_mouse(self, mouse_x):
        if self.rect.width <= 0:
            return
        pct = (mouse_x - self.rect.x) / self.rect.width
        value = self.min_value + pct * (self.max_value - self.min_value)
        self.value = self._clamp(value)

    def update(self, focused=False):
        self.is_focused = focused
        mouse_pos = rl.get_mouse_position()
        hovered = rl.check_collision_point_rec(mouse_pos, self.rect)

        if rl.is_mouse_button_pressed(rl.MouseButton.MOUSE_BUTTON_LEFT) and hovered:
            self.is_dragging = True

        if self.is_dragging:
            if rl.is_mouse_button_down(rl.MouseButton.MOUSE_BUTTON_LEFT):
                self._set_from_mouse(mouse_pos.x)
            else:
                self.is_dragging = False

        if self.is_focused and self.game.gamepad_enabled:
            if rl.is_gamepad_button_pressed(
                self.game.gamepad_id, rl.GamepadButton.GAMEPAD_BUTTON_LEFT_FACE_LEFT
            ):
                self.value = self._clamp(self.value - self.step)
            if rl.is_gamepad_button_pressed(
                self.game.gamepad_id, rl.GamepadButton.GAMEPAD_BUTTON_LEFT_FACE_RIGHT
            ):
                self.value = self._clamp(self.value + self.step)

    def draw(self):
        rl.draw_rectangle_rec(self.rect, self.track_color)

        pct = 0.0
        if self.max_value != self.min_value:
            pct = (self.value - self.min_value) / (self.max_value - self.min_value)
        filled_width = int(self.rect.width * max(0.0, min(1.0, pct)))
        if filled_width > 0:
            rl.draw_rectangle(
                int(self.rect.x),
                int(self.rect.y),
                filled_width,
                int(self.rect.height),
                self.fill_color,
            )

        knob_x = self.rect.x + filled_width
        knob_y = self.rect.y + self.rect.height / 2
        radius = max(6, int(self.rect.height / 2) + 2)
        knob_col = self.focused_color if self.is_focused else self.knob_color
        rl.draw_circle(int(knob_x), int(knob_y), radius, knob_col)
