import logging

import begin
import sunvox

from orbitant import backend
from sf.synth.sunsynth import SunSynth


@begin.start
@begin.logging
def main(filename: 'Filename of the .sunsynth to load',
         port: 'MIDI port name'):
    sunvox.init(None, 44100, 2, 0)
    slot = sunvox.Slot()
    slot.volume(255)
    synth = SunSynth(filename, slot)
    port = backend.open_input(name=port, virtual=True)
    logging.debug('port %r', port)
    for message in port:
        logging.debug('message %r', message)
        synth.process_midi(message)
