from adaptivepy.component.adaptation_space import has_adaptation_space


def choose_most_restricted(components, parameters):
    """
    Strategy to choose the most restricted component, that is the one with
    smallest adaptation space
    :param components: Components to choose from
    :type components: Iterable[Any]
    :param parameters: Parameters on which the choice is based
    :type parameters: Iterable[Parameter]
    :return: Chosen component considered to be the most restricted based on
             their correspondence to passed parameters
    """
    max_index = 0
    most_restricted = None
    unrestricted = None
    for c in components:
        if has_adaptation_space(c):
            space = c.adaptation_space()
            overlapping_parameters = \
                set(space.keys()).intersection(set(parameters))

            index = sum(len(p.possible_values()) / len(space[p]) for p in
                        overlapping_parameters)

            if index > max_index:
                most_restricted = c
                max_index = index
        else:
            unrestricted = c if not unrestricted else unrestricted

    return most_restricted or unrestricted
