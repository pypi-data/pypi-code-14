from . import Movie

class Movie3D(Movie):

  def __init__(self, title, rank, wow_factor):
    super().__init__(title, rank)
    self._wow_factor = wow_factor

  def thumbs_up(self):
    for i in range(0, self._wow_factor):
      super().thumbs_up()

  def show_effect(self):
    print('Wow! ' * self._wow_factor)

if __name__ == '__main__':
  movie3d = Movie3D('glee', 5, 20)
  print(movie3d.get_title())
  print(movie3d.get_rank())

  movie3d.thumbs_up()

  print(movie3d.get_rank())
  print(movie3d)

  movie3d.show_effect()
