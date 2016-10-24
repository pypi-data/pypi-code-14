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

"""Tools to notify unlocking of achievements"""

def notify_gi(achievement):
    """Notify user, using `gi` module."""
    try:
        import pgi
        pgi.install_as_gi()
    except ImportError:
        pass

    try:
        import gi
        gi.require_version('Notify', '0.7')
        from gi.repository import Notify
    except ImportError:
        # Silently ignore: we must not clobber user output
        return

    try:
        Notify.init("CLAchievements")
        Notify.Notification.new(
            "Achievement unlocked: {}".format(achievement.title),
            body=achievement.description(),
            icon=achievement.fullicon,
            ).show()
    except: # pylint: disable=bare-except
        # It may fail if no DBUS session is found, or because of timeout. User
        # must not see it.
        pass

def notify(achievement):
    """Portable function to notify unlocking achievements."""

    # Feel free to submit a pull request to make this portable
    notify_gi(achievement)
