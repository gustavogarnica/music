""" Retrieve Spotify Playlists and Tracks """

import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth

"""
Description:
Retrieves Spotify playlist and track info for a user.

Auth:
Spotify developers client ID, secret and redirect URI (env).
Spotify user credentials (prompt).

Output:
Playlists and corressponding tracks dumped in JSON format.
"""

def main():
    scope = 'playlist-read-private'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    # Playlists
    playlists = []
    off = 0

    while True:
        some_playlists = sp.current_user_playlists(limit=50, offset=off)
        if len(some_playlists['items']) == 0:
            break
        else:
            playlists.extend(some_playlists['items'])
            off = len(playlists)

    # Tracks
    for i in range(len(playlists)):

        tracks = []
        off = 0

        while True:
            some_tracks = sp.playlist_tracks(playlists[i]['id'], limit=100, offset=off)
            if len(some_tracks['items']) == 0:
                break 
            else:
                tracks.extend(some_tracks['items'])
                off = len(tracks)

        playlists[i].update({"tracks_data": tracks})

    # Dump
    with open(f"playlists.json", 'w') as pf:
        json.dump(json.dumps(playlists), pf)

    # Report
    for i in range(len(playlists)):
        print(f"{i+1} - {playlists[i]['name']} (tracks: {playlists[i]['tracks']['total']})")
        playlist_tracks = playlists[i]["tracks_data"]
        for j in range(len(playlist_tracks)):
            print(f"{j}: {playlist_tracks[j]['track']['artists'][0]['name']} - {playlist_tracks[j]['track']['name']}")
        print()


if __name__ == '__main__':
    main()
