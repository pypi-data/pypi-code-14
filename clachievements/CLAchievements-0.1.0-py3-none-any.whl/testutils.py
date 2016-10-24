# Command Line Achievements
# Copyright 2016 Louis Paternault
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Some utilities used for tests."""

def test_unlock(func):
    """Decorator for test methods unlocking the achievement.

    To be applied to methods of :class:`~clachievements.achievements.__init__.Achievement`.

    Those methods must iterate over shell commands (as strings). Executing
    those commands must unlock the achievement. Otherwise, the
    corresponding test will fail.
    """
    func.test_lock = False
    return func

def test_lock(func):
    """Decorator for test methods keeping the achievement locked.

    To be applied to methods of :class:`~clachievements.achievements.__init__.Achievement`.

    Those methods must iterate over shell commands (as strings). Executing
    those commands must not unlock the achievement. Otherwise, the
    corresponding test will fail.
    """
    func.test_lock = True
    return func

def iter_test_methods(achievement, *, lock=True, unlock=True):
    """Iterate over test methods.

    :param Achievement achievement: The object which methods are to be iterated.
    :param boolean lock: Include methods keeping the achievement locked
        (decorated using :func:`test_lock`).
    :param boolean unlock: Include methods unlocking the achievement
        (decorated using :func:`test_unlock`).
    """
    for method_name in dir(achievement):
        method = getattr(achievement, method_name)
        try:
            lock_attr = method.test_lock
        except AttributeError:
            continue
        if lock_attr and lock:
            yield method
        if not lock_attr and unlock:
            yield method
