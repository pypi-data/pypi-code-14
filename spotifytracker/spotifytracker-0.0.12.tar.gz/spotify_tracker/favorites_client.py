import logging

from spotify_tracker.spotify_client import SpotifyPlaylistClient
from . import config


logger = logging.getLogger(name='spotify_tracker')


class SpotifyFavoritesClient(SpotifyPlaylistClient):
    def __init__(self):
        self.playlist_id = config.get_config_value('favorites_playlist_id')
        return super().__init__()

    def setup_playlist_id(self):
        print("You need to add a playlist_id to your config to save "
              "song history to.")
        sp_playlists = self.sp.user_playlists(self.username)
        playlists = [p for p in sp_playlists['items']
                     if p['owner']['id'] == self.username]
        for playlist in playlists:
            print('{}: {}'.format(playlist['name'], playlist['id']))
        playlist_id = input("Please input the playlist_id of the Playlist "
                            "you'd like to save your favorites to: ")
        config.save_config_value('favorites_playlist_id', playlist_id)

    def main(self):
        if not self.check_config():
            raise Exception("Please run setupfavorites command.")

        track_id = self.get_current_track_id()
        if not track_id:
            logger.warning('No song currently playing')
        logger.info('Currently listening to {}'.format(
            self.get_track_name_and_artist_string(track_id)
        ))
        self.add_track_to_playlist(track_id)
