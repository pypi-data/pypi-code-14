# -*- coding: utf-8 -*-


def selection(elements):
    """Returns the sorted values using selection sort algorithm. Selection
    sort has O(pow(n, 2)) time complexity in all the three cases (Best,
    Average and Worst).

    Args:
        elements (list): A list of values provided by the user.

    Returns:
        list: A list of elements sorted in ascending order.

    .. versionadded:: 0.1.0

    .. versionchanged:: 0.1.1
        Added validation for checking whether every element in the list is a
        string (when strings are provided in the list).
    """
    if not isinstance(elements, list):
        raise ValueError('A list of values should be given.')

    is_str = all(isinstance(element, str) for element in elements)

    if any(isinstance(element, str) for element in elements) and not is_str:
        # When any of the element in the list is a string, we should then
        # check whether all the other elements are strings or not.
        raise ValueError("int() and str() type can't be specified at the same "
                         "time")

    for pivot in range(0, len(elements) - 1):
        # Assume that minimum value is the starting element in the list.
        minimum = pivot

        for next in range(pivot + 1, len(elements)):
            if elements[next] < elements[minimum]:
                # If pivot + 1 position element is smaller than the minimum
                # value, we swap the values.
                minimum = next

        if minimum != pivot:
            # When the minimum and pivot positions are different, we go ahead
            # and swap the pivot ad minimum position values in the given list.
            elements[pivot], elements[minimum] = (elements[minimum],
                                                  elements[pivot])

    return elements
