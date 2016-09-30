from . import Movie
from . import Reviewer, WaldorfAndStatler
from . import SnackBar

class Playlist:
  def __init__(self, name, reviewer = WaldorfAndStatler):
    self.__name = name
    self.__movies = []
    self.set_reviewer(reviewer)

  def load(self, from_file='movies.csv'):
    with open(from_file) as file:
      for line in file:
        movie = Movie.from_csv(line)
        self.__movies.append(movie)

  def save(self, to_file='movie_rankings.csv'):
    with open(to_file, 'w') as file:
      for movie in sorted(self.__movies):
        file.write(movie.to_csv() + '\n')

  def set_reviewer(self, reviewer):
    if not issubclass(reviewer, Reviewer):
      raise TypeError("You must pass a Reviewer class")
    else:
      self.__reviewer = reviewer

  def add_movie(self, movie):
    self.__movies.append(movie)

  def play(self, viewings):
    print("%s's playlist:" % self.__name)
    print(sorted(self.__movies))

    snacks = SnackBar.SNACKS
    print("There are {} available in the snack bar.".format(len(snacks)))

    for snack in snacks:
      print("{} has {} carbs".format(snack.name, snack.carbs))

    for count in range(0, viewings):
      print("\nViewings: %d" % (count+1))
      for movie in self.__movies:
        self.__reviewer.review(movie)
        snack = SnackBar.random()
        movie.ate_snack(snack)
        print(movie)

  def total_carbs_consumed(self):
    result = 0
    for movie in self.__movies:
      result += movie.carbs_consumed()

    return result

  def print_stats(self):
    print("\n%s's Stats:" % self.__name)

    print("{} total carbs consumed".format(self.total_carbs_consumed()))

    for movie in sorted(self.__movies):
      print("\n{}'s snacks total:".format(movie.get_title()))
      for snack in movie.snacks():
        print("{} total {} carbs".format(snack.carbs, snack.name))

      print("{} grand total carbs".format(movie.carbs_consumed()))

    hits  = [movie for movie in self.__movies if movie.is_a_hit()]
    flops = [movie for movie in self.__movies if movie not in hits]

    print("\nHits:")
    for hit in hits:
      print(hit)

    print("\nFlops:")
    for flop in flops:
      print(flop)