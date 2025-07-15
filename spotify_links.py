import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Spotify Developer credentials
CLIENT_ID = '56aaa66cc1ea40c79de8ee09ad387dcf'
CLIENT_SECRET = '731b143def204a999e1c4a326ecb0d41'

# The playlist ID from the URL
PLAYLIST_ID = '7q1sJnepIBWPhECLW2lS2O'

def get_playlist_tracks(client_id, client_secret, playlist_id):
    auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(auth_manager=auth_manager)
    
    results = sp.playlist_items(playlist_id=playlist_id, additional_types=['track'])
    tracks = results['items']
    
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    
    return tracks

def print_track_urls(tracks):
    for item in tracks:
        track = item.get('track')
        if track:
            name = track.get('name').lower()
            url = track.get('external_urls', {}).get('spotify')
            print(f'"{name}": "{url}",')

if __name__ == "__main__":
    tracks = get_playlist_tracks(CLIENT_ID, CLIENT_SECRET, PLAYLIST_ID)
    print_track_urls(tracks)
