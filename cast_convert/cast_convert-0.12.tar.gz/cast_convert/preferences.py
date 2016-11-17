from multiprocessing import cpu_count


ENCODER_OPTIONS = {
    'mp3': '-c:a libmp3lame '
           '-q:a 3 ',
    'h264': '-c:v libx264 '
            '-preset ultrafast '
            '-crf 21 ',
    'mkv': '-f matroska '
}

COPY_OPTIONS = {
    'audio': '-c:a copy',
    'video': '-c:v copy',
    'container': ''
}

CONVERT_TO_CODEC = {
    'audio': 'mp3',
    'video': 'h264',
    'container': {'mkv', 'mp4'},
    None: None  # stream isn't found
}


DEFAULT_CONTAINER = "mkv"


NEW_FILE_FMT = '%s_castconvert.mkv'
FILESIZE_CHECK_WAIT = 1.1

CPUS = cpu_count()
THREADS = (CPUS - 1) if CPUS >= 3 else CPUS

FFMPEG_PROCESSES = 1 if CPUS >= 2 else 1  # one day
