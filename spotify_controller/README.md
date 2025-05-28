# Spotify Controller Plugin

Control Spotify playback, search music, and manage playlists through AI agents.

## Features

- **Playback Control**: Play, pause, resume, skip tracks
- **Music Search**: Search for tracks, artists, albums, and playlists
- **Device Management**: List and transfer playback between devices
- **Volume Control**: Set volume levels
- **Playlist Access**: Get user playlists and their contents

## Setup Instructions

### 1. Create a Spotify App

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Click "Create an App"
3. Fill in the app name and description
4. Accept the terms and create the app

### 2. Configure Your App

1. In your app settings, add `http://127.0.0.1:8888/callback` as a Redirect URI
2. Copy your **Client ID** and **Client Secret**

### 3. Set Environment Variables

Add these to your `.env` file:

```bash
# Required
SPOTIFY_CLIENT_ID=your_client_id_here
SPOTIFY_CLIENT_SECRET=your_client_secret_here

# Optional (default shown)
SPOTIFY_REDIRECT_URI=http://127.0.0.1:8888/callback
```

### 4. First Time Authentication

The first time you use the plugin, it will open a browser window for Spotify authentication. After logging in and authorizing the app, you'll be redirected to a localhost URL. Copy the full URL and paste it back into the terminal when prompted.

## Available Functions

### Playback Control
- `get_current_playback()` - Get current playing track info
- `pause_playback()` - Pause current playback
- `resume_playback()` - Resume playback
- `next_track()` - Skip to next track
- `previous_track()` - Go to previous track

### Music Discovery
- `search_spotify(query, search_type, limit)` - Search for music
- `get_user_playlists(limit)` - Get user's playlists

### Device Management
- `get_available_devices()` - List available Spotify devices
- `transfer_playback(device_id, force_play)` - Transfer to different device

### Playback Actions
- `play_track(track_uri)` - Play a specific track
- `play_playlist(playlist_uri)` - Play a playlist
- `set_volume(volume_percent)` - Set volume (0-100)

## Usage Examples

```python
# Search for a song
results = await search_spotify("Bohemian Rhapsody", "track", 5)

# Play the first result
if results.get('tracks'):
    track_uri = results['tracks'][0]['uri']
    await play_track(track_uri)

# Get current playback info
current = await get_current_playback()
if current:
    print(f"Now playing: {current['track_name']} by {current['artist']}")

# Control playback
await pause_playback()
await resume_playback()
await next_track()
```

## Requirements

- Python 3.10+
- spotipy>=2.22.0
- Active Spotify Premium account (required for playback control)

## Notes

- Playback control requires Spotify Premium
- The plugin will automatically handle OAuth token refresh
- Device control works with any Spotify Connect-enabled device
- Search functionality works with free Spotify accounts 