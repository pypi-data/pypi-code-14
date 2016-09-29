# -*- coding: utf-8 -*-

""" Wraps the Sampling Algorithm Used for the Australian Senate Audit. """

from aus_senate_audit.config_reader import ConfigReader
from aus_senate_audit.sampler.sampler import generate_outputs


class SamplerWrapper(object):
    """ Wraps the algorithm used for sampling from the cast ballots of the Australian senate election. """

    def __init__(self, seed, state, sample_increment_size, data_file_path, audit_recorder, quick=False):
        """ Initializes a :class:`SamplerWrapper` object.

        :param int seed: The starting value for the random number generator.
        :param str state: The abbreviated name of the state to sample ballots from.
        :param int sample_increment_size: The number of ballots to add to the growing sample for this audit stage.
        :param str data_file_path: The path to all Australian senate election data.
        :param :class:`AuditRecorder` audit_recorder: An object for interfacing with information stored about the
            audit's progress thus far.
        :param boolean quick: A flag indicating whether the audit is manual (`quick` is False) or not manual (default:
            False).
        """
        audit_stage = audit_recorder.get_current_audit_stage()
        sample_size = audit_recorder.get_current_sample_size()

        new_audit_stage = audit_stage + 1
        new_sample_size = sample_size + sample_increment_size

        ballots = ConfigReader(data_file_path).get_all_ballots_for_state(state)
        _, sample_indices = generate_outputs(new_sample_size, False, 0, len(ballots) - 1, str(seed), sample_size)
        sample = [ballots[i] for i in sample_indices]
        audit_recorder.record_audit_info(new_audit_stage, new_sample_size)
        audit_recorder.record_selected_ballots(new_audit_stage, sample, quick)
