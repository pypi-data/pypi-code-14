import logging

from spotify_tracker.spotify_client import SpotifyPlaylistClient
from . import config


logger = logging.getLogger(name='spotify_tracker')


class SpotifyFavoritesClient(SpotifyPlaylistClient):
    def __init__(self):
        self.playlist_id = config.get_config_value('favorites_playlist_id')
        self.playlist_name = config.get_config_value('favorites_playlist_name')
        return super().__init__()

    def setup_playlist_id(self):
        print("You need to add a playlist_id to your config to save "
              "song history to.")
        sp_playlists = self.sp.user_playlists(self.username)
        playlists = {p['id']: p['name'] for p in sp_playlists['items']
                     if p['owner']['id'] == self.username}
        for playlist_id, playlist_name in playlists.items():
            print('{}: {}'.format(playlist_name, playlist_id))
        playlist_id = input("Please input the playlist_id of the Playlist "
                            "you'd like to save your favorites to: ")
        playlist_name = playlists[playlist_id]
        config.save_config_value('favorites_playlist_id', playlist_id)
        config.save_config_value('favorites_playlist_name', playlist_name)

    def main(self):
        if not self.check_config():
            raise Exception("Please run setupfavorites command.")

        track_id = self.get_current_track_id()
        if not track_id:
            logger.warning('No song currently playing')
        self.add_track_to_playlist(track_id)
        logger.info('Added {} to {}'.format(
            self.get_track_name_and_artist_string(track_id),
            self.playlist_name
        ))
