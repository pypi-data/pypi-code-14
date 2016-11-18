from scss import is_color

VALID_COLORS = (
    '#',
    'rgb',
    'rgba',
    'hsl',
    'hsla',

    # CSS Level 1 colors
    'white', 'black', 'silver', 'gray', 'red', 'maroon', 'yellow', 'olive',
    'lime', 'green', 'aqua', 'teal', 'blue', 'navy', 'fuschia', 'purple',

    # The only color added in CSS Level 2 (Revision 1)
    'orange',
)

INVALID_COLOURS = (
    'suchblue',
    'muchmaroon',
    'wowfuscha',
)


def test_is_color():
    for value in VALID_COLORS:
        assert is_color(value)


def test_is_not_a_colour():
    for value in INVALID_COLOURS:
        assert not is_color(value)
