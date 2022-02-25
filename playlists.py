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
    with open(f"playlists.json", 'w') as pj:
        json.dump(json.dumps(playlists), pj)

    # Report
    with open(f"playlists.log", 'w') as pl:
        for i in range(len(playlists)):
            pl.write(f"Playlist {i+1} - {playlists[i]['name']} (tracks: {playlists[i]['tracks']['total']}) \n")
            playlist_tracks = playlists[i]["tracks_data"]
            for j in range(len(playlist_tracks)):
                pl.write(f"Track {j+1}: {playlist_tracks[j]['track']['artists'][0]['name']} - {playlist_tracks[j]['track']['name']} \n")
            pl.write(f"\n")

    # End status
    print(f"All done!")


if __name__ == '__main__':
    main()
