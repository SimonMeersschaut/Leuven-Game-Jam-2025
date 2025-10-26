import pygame

_current_path = None
_default_volume = 0.5

def _ensure_init():
    if not pygame.mixer.get_init():
        pygame.mixer.init()  # uses pygame.init() defaults; adjust if needed

def _play_loop(path: str, fade_ms: int = 800, volume: float = _default_volume):
    global _current_path
    _ensure_init()
    if _current_path == path and pygame.mixer.music.get_busy():
        return
    pygame.mixer.music.load(path)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(-1, fade_ms=fade_ms)  # -1 = loop forever
    _current_path = path

def stop(fade_ms: int = 400):
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.fadeout(fade_ms)

def play_menu_music(fade_ms: int = 800, volume: float = _default_volume):
    _play_loop('resources/music/clair_de_lune.mp3', fade_ms, volume)

def play_game_music(fade_ms: int = 800, volume: float = _default_volume):
    _play_loop('resources/music/vivaldi_four_seasons_4.mp3', fade_ms, volume)

def set_volume(volume: float):
    pygame.mixer.music.set_volume(max(0.0, min(1.0, volume)))