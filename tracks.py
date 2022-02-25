""" Retrieve Spotify Saved Tracks """

import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth

"""
Description:
Retrieves Spotify saved tracks info for a user.

Auth:
Spotify developers client ID, secret and redirect URI (env).
Spotify user credentials (prompt).

Output:
Saved tracks dumped in JSON format.
"""

def main():
    scope = 'user-library-read'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    # Tracks
    tracks = []
    off = 0

    while True:
        some_tracks = sp.current_user_saved_tracks(limit=50, offset=off)
        if len(some_tracks['items']) == 0:
            break
        else:
            tracks.extend(some_tracks['items'])
            off = len(tracks)

    # Dump
    with open(f"tracks.json", 'w') as tf:
        json.dump(json.dumps(tracks), tf)

    # Report
    with open(f"tracks.log", 'w') as tl:
        for i in range(len(tracks)):
            tl.write(f"Track {i+1} - {tracks[i]['track']['album']['name']} - {tracks[i]['track']['artists'][0]['name']} - {tracks[i]['track']['name']} \n")
        tl.write(f"\n")

    # End status
    print(f"All done!")


if __name__ == '__main__':
    main()
