# This file is a part of 'gravely' software. Copyright (c) 2016 LCODE team.
# Distributed under the terms of the MIT License, see LICENSE.txt.

"""A simplified progressbar2 wrapper."""

from time import time

import progressbar


MIN_UPDATE_TIME = 0.02  # <= 50 Hz


class Progress(progressbar.ProgressBar):
    """
    A simple-to-use progressbar based on progressbar2's ProgressBar.
    Automates applying several preferred changes:
    * Specific fixed widget layout that changes on completion
    * Updatable prefix string
    * Guessing amount of samples for AdaptiveETA (aim for 1% * max_value)
    * A (hopefully) faster update limiting
    * Enforced redirect_stdout=True
    """

    def __init__(self, text=None, **kwargs):
        text = text or ''

        eta_samples = 10
        if 'max_value' in kwargs and kwargs['max_value'] > 1000:
            eta_samples = kwargs['max_value'] // 100

        super().__init__(
            widgets=[
                text,
                progressbar.Percentage(),
                ' ',
                progressbar.Bar(),
                ' ',
                progressbar.AdaptiveETA(samples=eta_samples),
            ],
            redirect_stdout=True,
            **kwargs
        )

        self._last_update_time = 0

    def update(self, value, text=None, force=False, **kwargs):
        if text is not None:
            self.widgets[0] = text

        if time() - self._last_update_time < MIN_UPDATE_TIME and not force:
            return
        self._last_update_time = time()

        super().update(value, force=force, **kwargs)

    def finish(self, text=None, **kwargs):
        if text is not None:
            self.widgets[0] = text
        del self.widgets[1]  # remove percentage

        super().update(self.max_value, force=True)
        super().finish(**kwargs)
