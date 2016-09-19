""" Spotify Tracker - Save every song you play from OS X to a playlist

Usage:
  spotifytracker setup
  spotifytracker watch [ [-V | --verbose] | [-Q | --quiet ]]
  spotifytracker debug-refresh-token
  spotifytracker remove-old-tracks <days> [-D | --dryrun ] [ [-V | --verbose] | [-Q | --quiet ]]

Options:
  -V --verbose
  -Q --quiet
  -D --dryrun
"""
import logging

from docopt import docopt

from spotify_client import SpotifyClient


DEFAULT_LOG_LEVEL = logging.INFO


def main():
    arguments = docopt(__doc__)
    _spotify_client = SpotifyClient()

    logging.basicConfig(
        format='%(asctime)s %(levelname)s: %(message)s')

    spotify_tracker_logger = logging.getLogger(name='spotify_tracker')
    base_logger = logging.getLogger()
    if arguments['--verbose']:
        base_logger.setLevel(level=logging.DEBUG)
    elif arguments['--quiet']:
        base_logger.setLevel(level=logging.WARNING)
    else:
        spotify_tracker_logger.setLevel(level=DEFAULT_LOG_LEVEL)

    if arguments['setup']:
        _spotify_client.setup()
        return
    if arguments['watch']:
        _spotify_client.watch()
        return
    if arguments['debug-refresh-token']:
        _spotify_client.save_token()
        return
    if arguments['remove-old-tracks']:
        _spotify_client.remove_old_tracks_in_playlist(
            int(arguments['<days>']), arguments['--dryrun']
        )

if __name__ == "__main__":
    main()
