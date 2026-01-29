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
            KeyboardAction.MOVE_UP: [rl.KeyboardKey.KEY_W, rl.KeyboardKey.KEY_UP],
            KeyboardAction.MOVE_DOWN: [rl.KeyboardKey.KEY_S, rl.KeyboardKey.KEY_DOWN],
            KeyboardAction.MOVE_LEFT: [rl.KeyboardKey.KEY_A, rl.KeyboardKey.KEY_LEFT],
            KeyboardAction.MOVE_RIGHT: [rl.KeyboardKey.KEY_D, rl.KeyboardKey.KEY_RIGHT],
            KeyboardAction.PAUSE: [rl.KeyboardKey.KEY_ESCAPE],
        }
        self.keys = {
            name: getattr(rl.KeyboardKey, name)
            for name in dir(rl.KeyboardKey)
            if name.startswith("KEY_")
        }
        self.last_pressed = []

    def update(self):
        # Collect pressed keys this frame for optional queries.
        self.last_pressed = []
        while True:
            key = rl.get_key_pressed()
            if key == rl.KeyboardKey.KEY_NULL:
                break
            self.last_pressed.append(key)

    def bind(self, action, *keys):
        self.actions[action] = list(keys)

    def is_down(self, action):
        return any(rl.is_key_down(k) for k in self.actions.get(action, []))

    def is_pressed(self, action):
        return any(rl.is_key_pressed(k) for k in self.actions.get(action, []))

    def is_key_down(self, key_name):
        key = self.keys.get(key_name)
        return rl.is_key_down(key) if key is not None else False

    def is_key_pressed(self, key_name):
        key = self.keys.get(key_name)
        return rl.is_key_pressed(key) if key is not None else False

    def is_any_key_pressed(self):
        return len(self.last_pressed) > 0
