from __future__ import division, absolute_import, print_function
from brite_etl.decorators import get_frames
import os
import pandas as pd


def export_excel(frames=None, full=False, path=None, file_name='brite_etl_export.xlsx'):
    print('doing the excel thing')
    file_path = os.path.join(path, file_name)

    writer = pd.ExcelWriter(file_path, engine='xlsxwriter')

    if (type(frames).__name__ is 'DataFrame'):
        frames.to_excel(writer, index=False)
    elif(type(frames).__name__ is 'FrameSet'):
        _frames = frames.frames
        for name, frame in _frames.iteritems():
            if name == 'prepared':
                _frames = _frames.get('prepared')
                for name, frame in _frames.iteritems():
                    frame.df.to_excel(writer, sheet_name=frame.config.get('display_name'), index=False)
            else:
                frame.df.to_excel(writer, sheet_name=frame.config.get('display_name'), index=False)

    print('added them in')

    writer.save()
    return
