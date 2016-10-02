import importlib
import inspect
from brite_etl.exceptions import InvalidFrame


class FrameBuilder(object):
    """ Fetch and build a frame class

    Imports the frame class associated with passed frame, creates it with the passed dataframe,
    and returns a new instance of the class.

    Not recommended to use directly, should get frames through :class:`brite_etl.lib.FrameSet` instead.

    :param name: Name of the frame, lowercase. If prepared, prepend 'prepared.' to frame name.
    :type name: str
    :param df: Dataframe to use when building the frameclass
    :type df: Pandas.DataFrame
    :returns: The corrosponding frame class of requested frame
    :rtype: Metaclass of :class:`brite_etl.abstracts.Frame`
    """
    def __new__(self, name, df=None):
        try:
            module = importlib.import_module(
                'brite_etl.frames.{0}'.format(name)
            )

            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and name != 'Frame':
                    return obj(df)

        except Exception as e:
            raise InvalidFrame('Error when importing frame class: {0}'.format(e))
        else:
            raise InvalidFrame('Error when importing frame class.')
