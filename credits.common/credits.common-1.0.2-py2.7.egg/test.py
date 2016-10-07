#!/usr/bin/env python
# -*- coding: utf-8 -*-
from UserDict import UserDict


class DummyRegistry(UserDict):
    def register(self, marshallable):
        self[marshallable.fqdn] = marshallable

    def unmarshall(self, payload):
        return self[payload["fqdn"]].unmarshall(self, payload)


def check_transform(cls, dependencies, kwargs, state, state_expected):
    """
    Test a Tranform is implemented correctly.

    :param cls: Your Transform class.
    :param dependencies: A list of Marshallable objects. If you've not used any in your transform, pass an empty list.
    :param kwargs: A list of keyword arguments to be passed to the constructor of your Transform.
    :param state: A mocked up state for checking verify/apply logic.
    :param state: A mocked up resultant state for checking transform.apply applied correctly.

    :type cls: credits.transform.Transform
    :type dependencies: [credits.interface.Marshallable]
    :type kwargs: dict
    :type state: dict
    :type state_expected: dict
    """
    from copy import deepcopy
    from credits.hash import SHA256HashProvider

    hash_provider = SHA256HashProvider()

    # Setup registry
    registry = DummyRegistry()
    for dependency in dependencies:
        registry.register(dependency)

    # Check registration
    registry.register(cls)

    # Construct the Transform
    transform = cls(**kwargs)

    # Get a digest.
    digest = transform.hash(hash_provider)

    # Check this has a UNIQUE fqdn.
    fqdn = transform.fqdn

    # Marshall this object into a primative map
    payload = transform.marshall()

    # Make sure the fqdn is in the payload.
    assert payload["fqdn"] == fqdn

    # Get the transform back from it's marshalled output.
    transform = registry.unmarshall(payload)

    # Check that it still digests like it did before.
    assert transform.hash(hash_provider) == digest

    # Verify against some demo state that it can apply either NOW or in the FUTURE
    result, error = transform.verify(deepcopy(state))
    if error is not None:
        raise error
    assert result is None  # All good!

    # Apply against state, check application is as expected.
    result, error = transform.apply(deepcopy(state))
    if error is not None:
        raise error
    assert result == state_expected  # All good!
