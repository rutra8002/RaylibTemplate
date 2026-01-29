import pyray as rl
from enum import Enum
from pathlib import Path
import re


class ShaderManager:
    SHADER_EXTS = {".fs", ".vs"}

    def __init__(self):
        self.assets_dir = Path(__file__).resolve().parent.parent / "assets/shaders"
        self.ShaderId, self._id_to_paths = self._build_enum()
        self.shaders = {}
        self._load_assets()

    def _normalize_id(self, name):
        key = re.sub(r"[^0-9A-Za-z]+", "_", name).strip("_").upper()
        if not key:
            key = "SHADER"
        if key[0].isdigit():
            key = f"S_{key}"
        return key

    def _build_enum(self):
        entries = {} # name -> {vs: path, fs: path}
        if self.assets_dir.exists():
            for path in sorted(self.assets_dir.iterdir()):
                if not path.is_file():
                    continue
                if path.suffix not in self.SHADER_EXTS:
                    continue

                name = path.stem
                if name not in entries:
                    entries[name] = {"vs": None, "fs": None}

                if path.suffix == ".vs":
                    entries[name]["vs"] = str(path)
                elif path.suffix == ".fs":
                    entries[name]["fs"] = str(path)

        final_entries = {}
        processed_ids = set()

        for name, paths in entries.items():
            key = self._normalize_id(name)
            base = key
            i = 2
            while key in processed_ids:
                key = f"{base}_{i}"
                i += 1
            processed_ids.add(key)
            final_entries[key] = paths

        if not final_entries:
            shader_enum = Enum("ShaderId", {"NONE": 0})
            return shader_enum, {}

        shader_enum = Enum("ShaderId", {name: name for name in final_entries})
        id_to_paths = {shader_enum[name]: paths for name, paths in final_entries.items()}
        return shader_enum, id_to_paths

    def _load_assets(self):
        for shader_id, paths in self._id_to_paths.items():
            vs = paths["vs"]
            fs = paths["fs"]


            vs_arg = vs if vs else ""
            fs_arg = fs if fs else ""

            try:
                shader = rl.load_shader(vs_arg, fs_arg)
                self.shaders[shader_id] = shader
            except Exception as e:
                print(f"Failed to load shader {shader_id}: {e}")

    def get_shader(self, shader_id):
        return self.shaders.get(shader_id)

    def unload_shaders(self):
        for shader in self.shaders.values():
            rl.unload_shader(shader)
        self.shaders.clear()
