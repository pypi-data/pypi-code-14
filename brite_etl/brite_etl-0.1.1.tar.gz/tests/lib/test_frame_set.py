import random


class TestFrameSet:

    def test_blank_frame_set(self, frame_set_blanks):
        _set = frame_set_blanks()

        assert type(_set).__name__ is 'FrameSet'
        assert type(random.choice(list(_set.frames.values())).df).__name__ is 'DataFrame'

    def test_blank_prepared_frame_set(self, frame_set_blanks):
        _set = frame_set_blanks(include_prepared=True)

        assert type(_set).__name__ is 'FrameSet'
        assert type(random.choice(list(_set.frames.get('prepared').values())).df).__name__ is 'DataFrame'

    def test_get_frame(self, frame_set):
        _set = frame_set
        acc = _set.frames.get('account_history', empty_frame=True)

        assert acc.__class__.__name__ is 'AccountHistory'
        assert acc.config.get('name') is 'account_history'
