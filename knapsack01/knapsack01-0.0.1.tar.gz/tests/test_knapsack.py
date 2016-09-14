from knapsack01.knapsack import Item
from knapsack01.knapsack import Knapsack


def test_item():
    """Test Item
    """

    i = Item('A', 10, [45, 78])
    assert i.name == 'A'
    assert i.weight == 10
    assert i.value == 62


def test_knapsack():
    """Test knapsack algorithm
    """

    k = Knapsack(10)
    items = [
        Item('A', 1, [1, 3]),
        Item('B', 2, [4, 1]),
        Item('C', 3, [4, 6]),
        Item('D', 4, [2, 6])
    ]
    k.items = items
    actual = k.pick_items('value', False)
    assert k.items == items
    assert [i.name for i in actual] == [
        'B', 'D', 'C'
    ]

    actual = k.pick_items('value', True)
    assert k.items == items
    assert [i.name for i in actual] == [
        'C', 'D', 'B'
    ]

    actual = k.pick_items('name', False)
    assert k.items == items
    assert [i.name for i in actual] == [
        'B', 'C', 'D'
    ]

    actual = k.pick_items()
    assert k.items == items
    assert [i.name for i in actual] == [
        'C', 'D', 'B'
    ]
