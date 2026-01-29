import os
import json
from config import BASE_DIR

MUSIC_DIR = os.path.join(BASE_DIR, "music")
MUSIC_FILE = os.path.join(MUSIC_DIR, "track.mp3")
CACHE_FILE = os.path.join(BASE_DIR, "beat_cache.json")


def analyze_music():
    """Analyse la musique et retourne BPM + beat times"""
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return float(data["tempo"]), data["beat_times_ms"]
    
    import librosa
    
    y, sr = librosa.load(MUSIC_FILE, mono=True)
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)[0:2]
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)
    beat_times_ms = (beat_times * 1000).astype(int).tolist()
    
    data = {"tempo": float(tempo), "beat_times_ms": beat_times_ms}
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f)
    
    return float(tempo), beat_times_ms
