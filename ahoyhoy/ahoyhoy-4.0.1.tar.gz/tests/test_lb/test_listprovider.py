from ahoyhoy.lb.providers.listprovider import ListProvider

def test_item_listprovider():
    # Arrange & Act
    lp = ListProvider(1, 2, 3)
    # Assert
    assert lp.get_list() == (1, 2, 3)

def test_string_listprovider():
    # Arrange and Act
    lp = ListProvider('a.com', 'b.com')
    # Assert
    assert lp.get_list() == ('a.com', 'b.com')
