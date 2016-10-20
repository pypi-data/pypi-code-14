from .database import PadVoiceFile
from .asvspoof import ASVspoofPadDatabase
from .avspoof import AVspoofPadDatabase
from .replay import ReplayPadDatabase
from .replaymobile import ReplayMobilePadDatabase
from .voicepa import VoicePAPadDatabase

# to fix sphinx warnings of not able to find classes, when path is shortened
PadVoiceFile.__module__ = "bob.pad.voice.database"
ASVspoofPadDatabase.__module__ = "bob.pad.voice.database"
AVspoofPadDatabase.__module__ = "bob.pad.voice.database"
ReplayPadDatabase.__module__ = "bob.pad.voice.database"
ReplayMobilePadDatabase.__module__ = "bob.pad.voice.database"
VoicePAPadDatabase.__module__ = "bob.pad.voice.database"

# gets sphinx autodoc done right - don't remove it
__all__ = [_ for _ in dir() if not _.startswith('_')]
