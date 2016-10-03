from __future__ import division, absolute_import, print_function

import os
import pandas as pd


def export_excel(frames, path, file_name='brite_etl_export.xlsx'):
    """Export frames/frameset as an .xlsx doc

    Each frame (1 if passed a frame, multiple if passed a frameset) will put placed on it's
    own sheet, titled using the frames display name.
    :param frames: Frame/Frameset to export
    :param path: path to place exported file in
    :param file_name: name of file (MUST include 'xlsx'!), defaults to 'brite_etl_export.xlsx'
    :type file_name: str, optional
    """
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

    writer.save()
    return
