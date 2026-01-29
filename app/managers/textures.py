import pyray as rl
from enum import Enum
from pathlib import Path
import re


class TextureManager:
    TEXTURE_EXTS = {".png", ".jpg", ".jpeg", ".tga", ".bmp", ".gif", ".pic", ".psd"}

    def __init__(self):
        self.assets_dir = Path(__file__).resolve().parent.parent / "assets/textures"
        self.TextureId, self._id_to_path = self._build_enum()
        self.textures = {}
        self._load_assets()

    def _normalize_id(self, name):
        key = re.sub(r"[^0-9A-Za-z]+", "_", name).strip("_").upper()
        if not key:
            key = "TEXTURE"
        if key[0].isdigit():
            key = f"T_{key}"
        return key

    def _build_enum(self):
        entries = {}
        if self.assets_dir.exists():
            for path in sorted(self.assets_dir.iterdir()):
                if not path.is_file():
                    continue
                if path.suffix.lower() not in self.TEXTURE_EXTS:
                    continue
                key = self._normalize_id(path.stem)
                self._add_entry(entries, key, path)

        if not entries:
            texture_enum = Enum("TextureId", {"NONE": 0})
            return texture_enum, {}

        texture_enum = Enum("TextureId", {name: name for name in entries})
        id_to_path = {texture_enum[name]: path for name, path in entries.items()}
        return texture_enum, id_to_path

    def _add_entry(self, entries, key, path):
        base = key
        i = 2
        while key in entries:
            key = f"{base}_{i}"
            i += 1
        entries[key] = path

    def _load_assets(self):
        for texture_id, path in self._id_to_path.items():
            try:
                texture = rl.load_texture(str(path))
                self.textures[texture_id] = texture
            except Exception as e:
                print(f"Failed to load texture {texture_id}: {e}")

    def get_texture(self, texture_id):
        return self.textures.get(texture_id)

    def unload_textures(self):
        for texture in self.textures.values():
            rl.unload_texture(texture)
        self.textures.clear()
