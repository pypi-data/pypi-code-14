# -*- coding: utf-8 -*-
# Copyright (c) 2016 Sqreen. All Rights Reserved.
# Please refer to our terms for more information: https://www.sqreen.io/terms.html
""" Callbacks rules classes and helpers
"""
import logging

from datetime import datetime
from functools import wraps

from .callbacks import Callback
from .events import Attack, get_context_payload
from .runtime_infos import RuntimeInfos, runtime
from .runner import MetricsEvent
from .condition_evaluator import ConditionEvaluator, is_condition_empty
from .constants import LIFECYCLE_METHODS


LOGGER = logging.getLogger(__name__)


def check_condition_wrapper(rule_data, function, condition, lifecycle):
    """ Wrapper that will check lifecycle method pre-condition before
    calling it.
    If pre-conditions are true, call the lifecycle method, otherwise
    return None.
    """

    @wraps(function)
    def wrapped(*args, **kwargs):
        """ Wrapper around lifecycle method
        """

        # Copy args to work on them
        binding_args = list(args)

        # Compute return value depending on the lifecycle method we wrap
        return_value = False
        if lifecycle in ('post', 'failing'):
            # Args[1] is either the return value of the hooked point
            # or the exception
            return_value = binding_args.pop(1)

        original = binding_args.pop(0)

        binding_eval_args = {
            "binding": locals(),
            "global_binding": globals(),
            "framework": runtime.get_current_request(),
            "instance": original,
            "arguments": binding_args,
            "cbdata": rule_data,
            "return_value": return_value
        }

        # Check the pre condition
        condition_result = condition.evaluate(**binding_eval_args)

        LOGGER.debug("ConditionWrapper (%s) result for %s: %s", condition, function, condition_result)

        if condition_result in (False, None):
            return None

        # Execute the hook otherwise with the original args
        return function(*args, **kwargs)

    wrapped.__wrapped__ = function

    return wrapped


class RuleCallback(Callback):

    def __init__(self, hook_module, hook_name, rule_name, rulespack_id,
                 block, test, runner, strategy_cls=None, data=None,
                 conditions=None, callbacks=None):
        super(RuleCallback, self).__init__(hook_module, hook_name, strategy_cls)
        self.rule_name = rule_name
        self.rulespack_id = rulespack_id

        if data is None:
            data = {}
        self.data = data
        self.block = block
        self.test = test
        self.runner = runner

        if conditions is None:
            conditions = {}
        self.conditions = conditions

        self.callbacks = callbacks

        self._apply_conditions()

    @classmethod
    def from_rule_dict(cls, rule_dict, runner):
        """ Return a RuleCallback based on a rule dict
        """
        return cls(
            hook_module=rule_dict['hookpoint']['klass'],
            hook_name=rule_dict['hookpoint']['method'],
            rule_name=rule_dict['name'],
            rulespack_id=rule_dict['rulespack_id'],
            strategy_cls=rule_dict['hookpoint'].get('strategy', 'import_hook'),
            block=rule_dict['block'],
            test=rule_dict['test'],
            data=rule_dict.get('data'),
            conditions=rule_dict.get('conditions'),
            callbacks=rule_dict.get('callbacks'),
            runner=runner
        )

    def _apply_conditions(self):
        """ Wrap each lifecycle methods if the Rule define them and if we have
        conditions for them.
        """
        for lifecycle in LIFECYCLE_METHODS.values():
            conditions = self.conditions.get(lifecycle)

            if not is_condition_empty(conditions) and hasattr(self, lifecycle):
                conditions = ConditionEvaluator(conditions)

                # Wrap the lifecycle method
                lifecycle_method = getattr(self, lifecycle)
                wrapped = check_condition_wrapper(self.data, lifecycle_method,
                                                  conditions, lifecycle)
                setattr(self, lifecycle, wrapped)

    def exception_infos(self, infos={}):
        """ Returns additional infos in case of exception
        """
        return {
            'rule_name': self.rule_name,
            'rulespack_id': self.rulespack_id,
            'should_block': self.should_block()
        }

    def should_block(self):
        """ Return True if this rule should catch an attack based on block
        and test value
        """
        return ((not self.test) and self.block)

    def record_attack(self, infos=None):
        """ Record an attack
        """
        current_request = runtime.get_current_request()

        if current_request is None:
            LOGGER.warning("No request was recorded, couldn't record an attack")
            return

        current_time = RuntimeInfos()._time()['time']

        attack_payload = {
            'rule_name': self.rule_name,
            'rulespack_id': self.rulespack_id,
            'client_ip': current_request.client_ip,
            'time': current_time,
            'test': self.test,
            'block': self.block,

            'infos': infos
        }
        attack_payload.update(current_request.full_payload)
        attack_payload.update(get_context_payload())

        # Whitelisted paths
        attack_payload.update(self.whitelist_path(current_request))

        attack = Attack(attack_payload)
        self.runner.queue.put(attack)

        LOGGER.debug("Attack was pushed to the queue: %s", attack_payload)

    def whitelist_path(self, current_request):
        """ Alter the attack payload if the request patch match a whitelist path
        """
        request_path = current_request.path
        whitelist_match = self.runner.settings.paths_whitelist_match(request_path)
        if whitelist_match is not None:
            return {'block': False, 'whitelist_match': whitelist_match}

        return {}

    def record_observation(self, metric_name, key, observation, at=None):
        """ Record a metric observation, push it to runner
        observations queue
        """
        if at is None:
            at = datetime.utcnow()

        self.runner.observation_queue.put((metric_name, at, key, observation))

        # Ask the runner thread to aggregate and empty the observation queue
        if self.runner.observation_queue.half_full():
            self.runner.queue.put(MetricsEvent)

    def __repr__(self):
        return "%s(rule_name=%r)" % (self.__class__.__name__, self.rule_name)
