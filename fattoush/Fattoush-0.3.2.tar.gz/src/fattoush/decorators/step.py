import contextlib
import datetime
import functools
import logging
import os.path
import sys
import time

from fattoush import world
from selenium.common.exceptions import WebDriverException

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)
HANDLER = logging.StreamHandler()
HANDLER.setLevel(logging.INFO)
LOGGER.addHandler(HANDLER)


LOGGED_IMAGE_FILENAME_TEMPLATE = (
    "{datetime:%Y%m%d_%H%M%S.%f}{parent_name} - {sentence}.png"
)


def _truncate(long_string, max_length, link_with='...'):
    if len(long_string) <= max_length:
        return long_string

    text_length = max_length - len(link_with)
    end_size = int(text_length / 4)
    start_size = text_length - end_size

    return "{start}{link}{end}".format(
        start=long_string[:start_size],
        end=long_string[-end_size:],
        link=link_with,
    )


def _create_log_filename(step, max_characters=200):
    """
    On some platforms filename length is limited to 200 characters. In
    order to work with this let's trim down a few parts to try and keep
    the file names useful.
    """

    parent = step.parent
    parent_name = getattr(parent, 'name', None)
    now = datetime.datetime.now()

    if parent_name is None:  # Must be a background
        parent_name = parent.feature.name

    mandatory_characters = len(LOGGED_IMAGE_FILENAME_TEMPLATE.format(
        datetime=now,
        parent_name='',
        sentence='',
    ))

    characters_left = max_characters - mandatory_characters

    parent_name = _truncate(parent_name, characters_left / 2)

    characters_left -= len(parent_name)

    sentence = _truncate(step.sentence, characters_left)

    return LOGGED_IMAGE_FILENAME_TEMPLATE.format(
        datetime=now,
        parent_name=parent_name,
        sentence=sentence,
    )


@contextlib.contextmanager
def _screenshot_after(step):
    """
    Ensure that a screenshot is taken after the decorated step definition
    is run.
    """
    log_dir = os.path.abspath('logs')

    if not os.path.exists(log_dir):
        os.mkdir(log_dir)

    file_path = os.path.join(log_dir, _create_log_filename(step))

    try:
        yield
    except:
        exc_type, exc_value, exc_tb = sys.exc_info()

        time.sleep(1)

        browser = world.per_scenario.get('browser')

        if browser is not None:
            try:
                taken = browser.get_screenshot_as_file(file_path)
            except WebDriverException:
                taken = False

            if taken:
                LOGGER.info(
                    "captured screen shot to {}".format(file_path)
                )
            else:
                LOGGER.exception(
                    "could not capture screen shot to {}".format(file_path)
                )

        raise exc_type, exc_value, exc_tb
    else:
        browser = world.per_scenario.get('browser')
        if browser is None:
            return

        try:
            if browser.is_sauce:
                browser.get_screenshot_as_png()
            else:
                browser.get_screenshot_as_file(file_path)
        except WebDriverException:
            pass


def screenshot(fn):
    @functools.wraps(fn)
    def _inner(step, *args, **kwargs):
        with _screenshot_after(step):
            return fn(step, *args, **kwargs)
    return _inner
