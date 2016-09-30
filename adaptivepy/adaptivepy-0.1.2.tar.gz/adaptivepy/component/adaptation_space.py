from adaptivepy.component.definitions import HasAdaptationSpace


def extend_adaptation_space(space, parameter, states):
    """
    Add set of states to an adaptation space for a given parameter.
    If the parameter is not already defined, add it to the space.
    Otherwise, extend the already defined space

    :param space: (out) Space to update
    :type space: dict[Parameter, set]
    :type parameter: Parameter
    :type states: set
    :return: Passed space with updated set
    """

    parameter_space = space.get(parameter, None)
    if parameter_space:
        parameter_space.update(states)
    else:
        space[parameter] = states.copy()
    return space


def union_adaptation_space(space1, space2):
    """
    :type space1: dict[Parameter, set]
    :type space2: dict[Parameter, set]
    :rtype: dict[Parameter, set]
    """
    space_copy = space1.copy()
    for k, v in space2.items():
        extend_adaptation_space(space_copy, k, v)
    return space_copy


def has_adaptation_space(component):
    return callable(getattr(
        component, HasAdaptationSpace.adaptation_space.__name__, None))


def aggregate_adaptation_space(components):
    """
    Iterate in components, request their adaptation space and aggregate them
    Assumes no space for non-adaptive components (adaptation agnostic)
    :param components: Iterable of components
    :type components: Iterable[HasAdaptationSpace | Any]
    :rtype: dict[Parameter, set]
    """
    aggregated_space = {}
    for c in components:
        if has_adaptation_space(c):
            for k, v in c.adaptation_space().items():
                extend_adaptation_space(aggregated_space, k, v)
    return aggregated_space


def filter_by_adaptation_space(components, state, exclude_agnostic=False):
    """
    Filter components which satisfy the passed monitored state
    Assumes no space for non-adaptive components (adaptation agnostic), include
    them by default
    :param components: Iterable of components
    :param state: Snapshot of the current monitored parameters values
    :type state: dict[Parameter, Any]
    :param exclude_agnostic: (Optional) True to exclude agnostic components
                             (non-adaptive), defaults to False
    :return: Subset of components as iterable which adaptation space covers the
             passed state values
    :rtype: set[Any]
    """
    filtered_components = set()
    for c in components:
        valid = True
        if has_adaptation_space(c):
            for parameter, space in c.adaptation_space().items():
                if state.get(parameter) not in space:
                    valid = False
                    break
        else:
            valid = not exclude_agnostic

        if valid:
            filtered_components.add(c)

    return filtered_components

