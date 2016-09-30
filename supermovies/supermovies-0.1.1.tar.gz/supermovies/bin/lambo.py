#!/usr/bin/env python

import os, sys

from supermovies import Movie, Movie3D, Playlist, BadMan

BIN_DIR = os.path.dirname(os.path.abspath(__file__))
default_movie_file = os.path.join(BIN_DIR, 'movies.csv')

from_file = sys.argv[1] if len(sys.argv) > 1 else default_movie_file

playlist = Playlist("Fozzie", BadMan)
playlist.load(from_file)
movie3d = Movie3D("glee", 5, 20)
playlist.add_movie(movie3d)

while(True):
  answer = input("\nHow many viewings? ('quit' to exit) ").lower()

  if(answer.isdigit()):
    playlist.play(int(answer))
  elif(answer in ('quit', 'exit')):
    playlist.print_stats()
    break
  else:
    print("Please enter a number or 'quit'")

playlist.save()