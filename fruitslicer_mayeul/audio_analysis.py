# audio_analysis.py

import os
import json

from config import MUSIC_FILE, BASE_DIR

CACHE_FILE = os.path.join(BASE_DIR, "beat_cache.json")

def analyze_music():
    """
    Retourne :
    - bpm (float)
    - beat_times_ms : liste d'instants (ms) où les beats se produisent
    Utilise un cache pour éviter de recalculer à chaque partie.
    """
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return float(data["tempo"]), data["beat_times_ms"]

    import librosa  # import tardif pour ne pas ralentir le lancement global

    y, sr = librosa.load(MUSIC_FILE, mono=True)
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)[0:2]
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)
    beat_times_ms = (beat_times * 1000).astype(int).tolist()

    data = {"tempo": float(tempo), "beat_times_ms": beat_times_ms}
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f)

    return float(tempo), beat_times_ms
