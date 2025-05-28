#!/usr/bin/env python3
"""
Example script showing how to use manual authentication with SpotifyController.

This approach doesn't require running a local server for the OAuth callback.
"""

import os
from controller import SpotifyController
from dotenv import load_dotenv

load_dotenv()

def main():
    # Get credentials from environment variables
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    
    if not client_id or not client_secret:
        print("Please set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET environment variables")
        return
    
    # Initialize controller with manual auth enabled
    # Using the proper IPv4 loopback address as required by Spotify
    controller = SpotifyController(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri="http://127.0.0.1:8888/callback",  # Using IPv4 loopback instead of localhost
        manual_auth=True
    )
    
    # Step 1: Get the authorization URL
    auth_url = controller.get_auth_url()
    print("🎵 Spotify Manual Authentication")
    print("=" * 40)
    print("IMPORTANT: First update your Spotify app settings!")
    print("1. Go to: https://developer.spotify.com/dashboard")
    print("2. Click on your app → Edit Settings")
    print("3. In 'Redirect URIs', add: http://127.0.0.1:8888/callback")
    print("4. Save the settings")
    print()
    print("Then follow these steps:")
    print("5. Copy and paste this URL into your browser:")
    print(f"   {auth_url}")
    print()
    print("6. After you authorize the app, you'll see an error page that says")
    print("   'This site can't be reached' or similar.")
    print()
    print("7. DON'T WORRY! Look at the URL in your browser's address bar.")
    print("   It should look like:")
    print("   http://127.0.0.1:8888/callback?code=AQA...")
    print()
    print("8. Copy ONLY the part after 'code=' (the long string)")
    print("   Example: If the URL is:")
    print("   http://127.0.0.1:8888/callback?code=AQA1234567890abcdef")
    print("   Then copy: AQA1234567890abcdef")
    print()
    
    # Step 3: Get the authorization code from user
    auth_code = input("📋 Paste the authorization code here: ").strip()
    
    # Remove any extra parts if user copied too much
    if "code=" in auth_code:
        auth_code = auth_code.split("code=")[1].split("&")[0]
    
    # Step 4: Complete authentication
    print("\n🔐 Authenticating...")
    if controller.authenticate_with_code(auth_code):
        print("✅ Authentication successful!")
        
        # Now you can use the controller
        print("\n🧪 Testing API calls...")
        
        # Get current playback
        current = controller.get_current_playback()
        if current:
            print(f"🎵 Currently playing: {current['track_name']} by {current['artist']}")
            if current['device']:
                print(f"📱 Device: {current['device']}")
        else:
            print("⏸️  Nothing currently playing")
        
        # Get available devices
        devices = controller.get_available_devices()
        print(f"\n📱 Available devices ({len(devices)}):")
        if devices:
            for device in devices:
                status = "🟢 Active" if device['is_active'] else "⚪ Inactive"
                volume = f" (Volume: {device['volume_percent']}%)" if device['volume_percent'] is not None else ""
                print(f"   {status} {device['name']} ({device['type']}){volume}")
        else:
            print("   No devices found. Make sure Spotify is open on at least one device.")
    
    else:
        print("❌ Authentication failed! Please check your authorization code and try again.")

if __name__ == "__main__":
    main() 