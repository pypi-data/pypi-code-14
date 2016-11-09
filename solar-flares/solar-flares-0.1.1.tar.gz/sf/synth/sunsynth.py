import logging

import rv.api
import sunvox


class SunSynth(object):

    def __init__(self, filename, slot):
        """
        :type slot: sunvox.Slot
        """
        logging.debug('filename=%r', filename)
        self.filename = filename
        synth = rv.api.read_sunvox_file(filename)
        self.project = rv.api.Project()
        self.project.attach_module(synth.module)
        self.module = synth.module
        synth.module >> self.project.output
        self.slot = slot
        slot.load(self.project)

    def process_midi(self, message):
        if message.type == 'note_on' and message.velocity > 0:
            note = sunvox.NOTECMD(message.note + 1)
            logging.debug('Note on: %r', note)
            logging.debug('Velocity: %r', message.velocity)
            self.slot.send_event(
                track_num=1,
                note=note,
                vel=message.velocity,
                module=self.module,
                ctl=0,
                ctl_val=0,
            )
        elif message.type == 'note_off' or \
                (message.type == 'note_on' and message.velocity == 0):
            note = sunvox.NOTECMD(message.note)
            self.slot.send_event(
                track_num=1,
                note=sunvox.NOTECMD.NOTE_OFF,
                vel=0,
                module=self.module,
                ctl=0,
                ctl_val=0,
            )
