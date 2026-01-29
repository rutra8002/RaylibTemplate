import pyray as rl
from enum import IntEnum, auto
from pathlib import Path
import re


class AudioManager:
    MUSIC_EXTS = {".mp3", ".ogg", ".flac", ".xm", ".mod"}
    SFX_EXTS = {".wav", ".ogg"}

    def __init__(self, master_volume=1.0, music_volume=1.0, sfx_volume=1.0):
        self.master_volume = self._clamp(master_volume)
        self.music_volume = self._clamp(music_volume)
        self.sfx_volume = self._clamp(sfx_volume)
        self.current_music = None
        self.current_music_id = None
        self.current_music_path = None
        self.audio_dir = Path(__file__).resolve().parent.parent / "assets/audio"
        self.AudioId, self._id_to_path = self._build_audio_enum()
        self._path_to_id = {str(path): audio_id for audio_id, path in self._id_to_path.items()}
        self.music = {}
        self.sounds = {}
        self._apply_master_volume()
        self._load_assets()

    def _apply_master_volume(self):
        rl.set_master_volume(self.master_volume)

    def _clamp(self, value):
        return max(0.0, min(1.0, float(value)))

    def _normalize_id(self, name):
        key = re.sub(r"[^0-9A-Za-z]+", "_", name).strip("_").upper()
        if not key:
            key = "AUDIO"
        if key[0].isdigit():
            key = f"A_{key}"
        return key

    def _build_audio_enum(self):
        entries = {}
        if self.audio_dir.exists():
            for path in sorted(self.audio_dir.iterdir()):
                if not path.is_file():
                    continue
                key = self._normalize_id(path.stem)
                base = key
                i = 2
                while key in entries:
                    key = f"{base}_{i}"
                    i += 1
                entries[key] = path

        if not entries:
            audio_enum = IntEnum("AudioId", {"NONE": auto()})
            return audio_enum, {}

        members = {"NONE": auto(), **{name: auto() for name in entries}}
        audio_enum = IntEnum("AudioId", members)
        id_to_path = {audio_enum[name]: path for name, path in entries.items()}
        return audio_enum, id_to_path

    def _load_assets(self):
        for audio_id, path in self._id_to_path.items():
            ext = path.suffix.lower()
            if ext in self.MUSIC_EXTS:
                music = rl.load_music_stream(str(path))
                rl.set_music_volume(music, self.music_volume)
                self.music[audio_id] = music
            elif ext in self.SFX_EXTS:
                sound = rl.load_sound(str(path))
                self.sounds[audio_id] = sound

    def set_master_volume(self, value):
        self.master_volume = self._clamp(value)
        self._apply_master_volume()

    def set_music_volume(self, value):
        self.music_volume = self._clamp(value)
        if self.current_music is not None:
            rl.set_music_volume(self.current_music, self.music_volume)

    def set_sfx_volume(self, value):
        self.sfx_volume = self._clamp(value)

    def play_music_id(self, audio_id, looping=True):
        if audio_id not in self.music:
            return
        if self.current_music_id != audio_id:
            if self.current_music is not None:
                rl.stop_music_stream(self.current_music)
            self.current_music = self.music[audio_id]
            self.current_music_id = audio_id
            if hasattr(self.current_music, "looping"):
                self.current_music.looping = looping
            rl.set_music_volume(self.current_music, self.music_volume)
        if not rl.is_music_stream_playing(self.current_music):
            rl.play_music_stream(self.current_music)

    def play_music(self, path, looping=True):
        audio_id = self._path_to_id.get(path)
        if audio_id is not None:
            self.play_music_id(audio_id, looping=looping)
            return
        self.load_music(path, looping=looping)
        if self.current_music is not None and not rl.is_music_stream_playing(self.current_music):
            rl.play_music_stream(self.current_music)

    def stop_music(self):
        if self.current_music is not None:
            rl.stop_music_stream(self.current_music)

    def pause_music(self):
        if self.current_music is not None:
            rl.pause_music_stream(self.current_music)

    def resume_music(self):
        if self.current_music is not None:
            rl.resume_music_stream(self.current_music)

    def update(self):
        if self.current_music is not None:
            rl.update_music_stream(self.current_music)

    def play_sound(self, sound, volume=1.0):
        rl.set_sound_volume(sound, self._clamp(volume) * self.sfx_volume)
        rl.play_sound(sound)

    def play_sound_id(self, audio_id, volume=1.0):
        sound = self.sounds.get(audio_id)
        if sound is None:
            return
        rl.set_sound_volume(sound, self._clamp(volume) * self.sfx_volume)
        rl.play_sound(sound)

    def shutdown(self):
        if self.current_music is not None:
            rl.stop_music_stream(self.current_music)
        for music in self.music.values():
            rl.unload_music_stream(music)
        for sound in self.sounds.values():
            rl.unload_sound(sound)
        self.music.clear()
        self.sounds.clear()
        self.current_music = None
        self.current_music_id = None
        self.current_music_path = None
        rl.close_audio_device()
