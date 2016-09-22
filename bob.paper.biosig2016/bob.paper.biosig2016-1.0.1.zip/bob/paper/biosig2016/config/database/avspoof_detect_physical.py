#!/usr/bin/env python

import bob.pad.db


avspoof_input_dir = "/idiap/project/lobi/AVSpoof/data/"
avspoof_input_ext = ".wav"


database = bob.pad.db.AVspoofPadDatabase(
    protocol='physical_access',
    original_directory=avspoof_input_dir,
    original_extension=avspoof_input_ext,
    training_depends_on_protocol=True,
)
