COLOUR_NAMES = [
    # CSS Level 1 colors
    'white', 'black', 'silver', 'gray', 'red', 'maroon', 'yellow', 'olive',
    'lime', 'green', 'aqua', 'teal', 'blue', 'navy', 'fuschia', 'purple',

    # The only color added in CSS Level 2 (Revision 1)
    'orange',

    # TODO: add CSS Level 3 colors, sometimes called a SVG or X11 color
]


def _startswith_one_of(v, l):
    for item in l:
        if v.startswith(item):
            return True
    return False
