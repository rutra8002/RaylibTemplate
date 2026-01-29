import pyray as rl
from enum import Enum
from pathlib import Path
import re


class ModelManager:
    MODEL_EXTS = {".obj", ".gltf", ".glb", ".iqm", ".vox", ".m3d"}

    def __init__(self):
        self.assets_dir = Path(__file__).resolve().parent.parent / "assets/models"
        self.ModelId, self._id_to_path = self._build_enum()
        self.models = {}
        self._load_assets()

    def _normalize_id(self, name):
        key = re.sub(r"[^0-9A-Za-z]+", "_", name).strip("_").upper()
        if not key:
            key = "MODEL"
        if key[0].isdigit():
            key = f"M_{key}"
        return key

    def _build_enum(self):
        entries = {}
        if self.assets_dir.exists():
            for path in sorted(self.assets_dir.iterdir()):
                if path.is_file() and path.suffix in self.MODEL_EXTS:
                    key = self._normalize_id(path.stem)
                    self._add_entry(entries, key, path)

                elif path.is_dir():
                    found_model = None
                    for candidate in ["scene.gltf", "scene.glb", f"{path.name}.gltf", f"{path.name}.glb", f"{path.name}.obj"]:
                        p = path / candidate
                        if p.exists():
                            found_model = p
                            break

                    if found_model:
                        key = self._normalize_id(path.name)
                        self._add_entry(entries, key, found_model)

        if not entries:
            model_enum = Enum("ModelId", {"NONE": 0})
            return model_enum, {}

        model_enum = Enum("ModelId", {name: name for name in entries})
        id_to_path = {model_enum[name]: path for name, path in entries.items()}
        return model_enum, id_to_path

    def _add_entry(self, entries, key, path):
        base = key
        i = 2
        while key in entries:
            key = f"{base}_{i}"
            i += 1
        entries[key] = path

    def _load_assets(self):
        for model_id, path in self._id_to_path.items():
            try:
                model = rl.load_model(str(path))
                self.models[model_id] = model
            except Exception as e:
                print(f"Failed to load model {model_id} from {path}: {e}")

    def get_model(self, model_id):
        return self.models.get(model_id)

    def unload_models(self):
        for model in self.models.values():
            rl.unload_model(model)
        self.models.clear()
