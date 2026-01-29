import pyray as rl
from enum import Enum


class KeyboardAction(Enum):
    MOVE_UP = "move_up"
    MOVE_DOWN = "move_down"
    MOVE_LEFT = "move_left"
    MOVE_RIGHT = "move_right"
    PAUSE = "pause"


class KeyboardManager:
    def __init__(self):
        self.actions = {
            KeyboardAction.MOVE_UP: rl.KeyboardKey.KEY_W,
            KeyboardAction.MOVE_DOWN: rl.KeyboardKey.KEY_S,
            KeyboardAction.MOVE_LEFT: rl.KeyboardKey.KEY_A,
            KeyboardAction.MOVE_RIGHT: rl.KeyboardKey.KEY_D,
            KeyboardAction.PAUSE: rl.KeyboardKey.KEY_ESCAPE,
        }
        self.action_order = [
            KeyboardAction.MOVE_UP,
            KeyboardAction.MOVE_DOWN,
            KeyboardAction.MOVE_LEFT,
            KeyboardAction.MOVE_RIGHT,
            KeyboardAction.PAUSE,
        ]
        self.keys = {
            name: getattr(rl.KeyboardKey, name)
            for name in dir(rl.KeyboardKey)
            if name.startswith("KEY_")
        }
        self.key_names_by_code = {value: name.replace("KEY_", "") for name, value in self.keys.items()}
        self.last_pressed = []

    def update(self):
        # Collect pressed keys this frame for optional queries.
        self.last_pressed = []
        while True:
            key = rl.get_key_pressed()
            if key == rl.KeyboardKey.KEY_NULL:
                break
            self.last_pressed.append(key)

    def bind(self, action, key):
        self.actions[action] = key

    def get_binding(self, action):
        return self.actions.get(action)

    def get_key_name(self, key):
        return self.key_names_by_code.get(key, str(key))

    def format_binding(self, action):
        key = self.get_binding(action)
        if key is None:
            return "Unbound"
        return self.get_key_name(key)

    def is_down(self, action):
        key = self.actions.get(action)
        return rl.is_key_down(key) if key is not None else False

    def is_pressed(self, action):
        key = self.actions.get(action)
        return rl.is_key_pressed(key) if key is not None else False

    def is_key_down(self, key_name):
        key = self.keys.get(key_name)
        return rl.is_key_down(key) if key is not None else False

    def is_key_pressed(self, key_name):
        key = self.keys.get(key_name)
        return rl.is_key_pressed(key) if key is not None else False

    def is_any_key_pressed(self):
        return len(self.last_pressed) > 0
