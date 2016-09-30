import contextlib
import datetime
import functools
import sys
import time

from fattoush import world
from selenium.common.exceptions import WebDriverException


@contextlib.contextmanager
def _screenshot_after(step):
    """
    Ensure that a screenshot is taken after the decorated step definition
    is run.
    """
    parent = step.parent
    parent_name = getattr(parent, 'name', None)
    if parent_name is None:  # Must be a background
        parent_name = parent.feature.name

    filename = (
        "logs/{datetime:{dfmt}_{tfmt}}{parent_name}.{step.sentence}.png"
        .format(
            step=step,
            parent_name=parent_name,
            datetime=datetime.datetime.now(),
            dfmt='%Y%m%d',
            tfmt='%H%M%S.%f',
        )
    )

    try:
        yield
    except:
        exc_type, exc_value, exc_tb = sys.exc_info()

        time.sleep(1)

        browser = world.per_scenario.get('browser')

        if browser is not None:
            try:
                browser.get_screenshot_as_file(filename)
            except Exception as ex:
                print(
                    "could not capture screen shot to {}:\n{}"
                    .format(filename, ex)
                )
            else:
                print("captured screen shot to {}".format(filename))

        raise exc_type, exc_value, exc_tb
    else:
        browser = world.per_scenario.get('browser')
        if browser is None:
            return

        try:
            if browser.is_sauce:
                browser.get_screenshot_as_png()
            else:
                browser.get_screenshot_as_file(filename)
        except WebDriverException:
            pass


def screenshot(fn):
    @functools.wraps(fn)
    def _inner(step, *args, **kwargs):
        with _screenshot_after(step):
            return fn(step, *args, **kwargs)
    return _inner
