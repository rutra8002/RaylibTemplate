class MenuController:
    def __init__(self, game, buttons):
        self.game = game
        self.buttons = list(buttons)
        self.focus_index = 0

    def set_buttons(self, buttons):
        self.buttons = list(buttons)
        if not self.buttons:
            self.focus_index = -1
        elif self.focus_index >= len(self.buttons):
            self.focus_index = len(self.buttons) - 1

    def update(self):
        if not self.buttons:
            self.focus_index = -1
            return
        if self.game.gamepad_enabled:
            y = getattr(self.game, "left_joystick_y", 0.0)
            if y < -self.game.gamepad_deadzone:
                self.focus_index = max(0, self.focus_index - 1)
            elif y > self.game.gamepad_deadzone:
                self.focus_index = min(len(self.buttons) - 1, self.focus_index + 1)
        else:
            self.focus_index = -1
        for i, b in enumerate(self.buttons):
            b.update(focused=(i == self.focus_index))
