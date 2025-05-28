# =============================================================================
# START OF MODULE METADATA
# =============================================================================
_module_info = {
    "name": "Spotify Controller",
    "description": "Control Spotify playback, search music, and manage playlists",
    "author": "BatteryShark",
    "version": "1.0.0",
    "platform": "any",
    "python_requires": ">=3.10",
    "dependencies": ["spotipy"],
    "environment_variables": {
        "SPOTIFY_CLIENT_ID": {
            "description": "Spotify app client ID from developer dashboard",
            "default": "",
            "required": True
        },
        "SPOTIFY_CLIENT_SECRET": {
            "description": "Spotify app client secret from developer dashboard",
            "default": "",
            "required": True
        },
        "SPOTIFY_REDIRECT_URI": {
            "description": "Redirect URI for Spotify OAuth",
            "default": "http://127.0.0.1:8888/callback",
            "required": False
        },
        "SPOTIFY_CACHE_PATH": {
            "description": "Path to the Spotify token cache file",
            "default": ".cache",
            "required": False
        }
    }
}
# =============================================================================
# END OF MODULE METADATA
# =============================================================================

# =============================================================================
# START OF EXPORTS
# =============================================================================
from .spotify_functions import (
    get_current_playback,
    search_spotify,
    play_track,
    play_playlist,
    pause_playback,
    resume_playback,
    next_track,
    previous_track,
    set_volume,
    get_user_playlists,
    get_available_devices,
    transfer_playback
)

_module_exports = {
    "tools": [
        get_current_playback,
        search_spotify,
        play_track,
        play_playlist,
        pause_playback,
        resume_playback,
        next_track,
        previous_track,
        set_volume,
        get_user_playlists,
        get_available_devices,
        transfer_playback
    ]
}
# =============================================================================
# END OF EXPORTS
# ============================================================================= 