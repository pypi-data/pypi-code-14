import unittest

from supermovies import Movie

class TestMovie(unittest.TestCase):

  def setUp(self):
    self.movie = Movie("goonies", 10)
    self.initial_rank = 10

  def test_movie_has_a_capitalized_title(self):
    self.assertEqual(self.movie.get_title(), 'Goonies')

  def test_movie_has_an_initial_rank(self):
    self.assertEqual(self.movie.get_rank(), 10)

  def test_movie_has_a_string_representation(self):
    self.assertEqual(str(self.movie), "Goonies has a rank of 10 (Hit)")

  def test_movie_rank_is_increased_by_one_if_thumbs_up_is_called(self):
    self.movie.thumbs_up()
    self.assertEqual(self.movie.get_rank(), self.initial_rank + 1)

  def test_movie_rank_is_decreased_by_one_if_thumbs_down_is_called(self):
    self.movie.thumbs_down()
    self.assertEqual(self.movie.get_rank(), self.initial_rank - 1)

class TestMovieCreatedWithADefaultRank(unittest.TestCase):

  def setUp(self):
    self.movie = Movie("goonies")

  def test_movie_has_a_rank_of_zero(self):
    self.assertEqual(self.movie.get_rank(), 0)

class TestMovieWithARankOfAtLeastTen(unittest.TestCase):

  def setUp(self):
    self.movie = Movie("goonies", 10)

  def test_movie_is_a_hit(self):
    self.assertTrue(self.movie.is_a_hit())

  def test_movie_has_a_status_of_hit(self):
    self.assertEqual(self.movie.status, 'Hit')

class TestMovieWithARankOfLessThanTen(unittest.TestCase):

  def setUp(self):
    self.movie = Movie("goonies", 9)

  def test_movie_is_a_hit(self):
    self.assertFalse(self.movie.is_a_hit())

  def test_movie_has_a_status_of_hit(self):
    self.assertEqual(self.movie.status, 'Flop')

if __name__ == '__main__':
  unittest.main()