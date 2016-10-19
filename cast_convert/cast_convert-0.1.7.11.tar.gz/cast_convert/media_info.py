from json import loads
from os.path import getsize
from subprocess import getoutput
from collections import namedtuple


try:
    from typing import Dict, List, Union, Tuple

except ImportError as e:
    try:
        from mypy.types import Dict, List, Union, Tuple

    except ImportError as e2:
        raise ImportError("Please install mypy via pip") from e2


from .exceptions import StreamNotFoundException
from .chromecast_compat import CAST_COMPAT
from .preferences import AUDIO_CODEC, VIDEO_CODEC, CONTAINER_TYPE, CONVERT_TO_CODEC


FFPROBE_CMD_FMT = 'ffprobe ' \
                  '-show_format ' \
                  '-show_streams ' \
                  '-loglevel quiet ' \
                  '-print_format json "%s"'

TRANSCODE_OPTS = {"audio": False,
                  "video": False,
                  "container": False}


CodecInfo = Union[bool, str]
Options = Dict[str, str]

Duration = namedtuple("Duration", "hour min sec")


def get_media_info(filename: str) -> dict:
    json = loads(getoutput(FFPROBE_CMD_FMT % filename))

    if not json:
        raise IOError("File %s cannot be read by ffprobe." % filename)

    return json


def get_codec(media_info: dict, codec_type: str) -> str:
    streams = media_info['streams']

    for stream in streams:
        if stream['codec_type'] == codec_type:
            return stream['codec_name']

    raise StreamNotFoundException("%s not found in file." % codec_type)


def get_video_codec(media_info: dict) -> str:
    return get_codec(media_info, 'video')


def get_audio_codec(media_info: dict) -> str:
    return get_codec(media_info, 'audio')


def get_container_format(media_info: dict) -> str:
    format_info = media_info['format']
    name = format_info['format_name']

    # ffprobe might return a list of types
    # let's check each one for compatibility
    for fmt in name.split(','):
        if fmt in CAST_COMPAT['container']:
            return fmt

    return name


VID_INFO_FUNCS = {
    'audio': get_audio_codec,
    'video': get_video_codec,
    'container': get_container_format
}


def duration_from_seconds(time: float) -> Duration:
    m, s = divmod(time, 60)
    h, m = divmod(m, 60)

    return Duration(h, m, s)


def get_duration(media_info: dict) -> float:
    return media_info['format']['duration']


def get_bitrate(media_info: dict) -> float:
    return media_info['format']['bitrate']


def get_size(filename: str) -> int:
    return getsize(filename)


def is_compatible(codec_type: str, codec: str):
    return codec in CAST_COMPAT[codec_type]


# def is_audio_compatible(codec: str) -> bool:
#     return codec in COMPAT_AUDIO
#
#
# def is_video_compatible(codec: str) -> bool:
#     return codec in COMPAT_VIDEO
#
#
# def is_container_compatible(container: str) -> bool:
#     return container in COMPAT_CONTAINER


def determine_transcodings(media_info: dict) -> Options:
    transcoding_info = TRANSCODE_OPTS.copy()

    for stream_type in TRANSCODE_OPTS:
        get_codec_info = VID_INFO_FUNCS[stream_type]

        try:
            codec = get_codec_info(media_info)

        except StreamNotFoundException as e:
            codec = None

        if not is_compatible(stream_type, codec):
            transcoding_info[stream_type] = CONVERT_TO_CODEC[stream_type]

    return transcoding_info


    # if not is_audio_compatible(get_audio_codec(media_info)):
    #     transcoding_info['audio'] = CONVERT_TO_CODEC['audio']
    #
    # if not is_video_compatible(get_video_codec(media_info)):
    #     transcoding_info['video'] = CONVERT_TO_CODEC['audio']
    #
    # if not is_container_compatible(get_container_format(media_info)):
    #     transcoding_info['container'] = CONVERT_TO_CODEC['audio']
    #
    # return transcoding_info


def get_transcode_info(filename: str) -> Options:
    return determine_transcodings(get_media_info(filename))


def is_video(path: str) -> bool:
    try:
        media_info = get_media_info(path)
        codec = get_video_codec(media_info)

        if codec == 'ansi':
            return False

        return bool(codec)

    except IOError as e:
        return False
