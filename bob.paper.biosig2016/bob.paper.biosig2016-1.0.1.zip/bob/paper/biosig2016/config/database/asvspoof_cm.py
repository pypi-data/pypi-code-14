#!/usr/bin/env python

import bob.pad.db


# directory where the wave files are stored
asvspoof_input_dir = "/idiap/resource/database/ASVspoof/"
asvspoof_input_ext = ".wav"


database = bob.pad.db.ASVspoofPadDatabase(
    protocol='CM',
    original_directory=asvspoof_input_dir,
    original_extension=asvspoof_input_ext,
    training_depends_on_protocol=True,
)

