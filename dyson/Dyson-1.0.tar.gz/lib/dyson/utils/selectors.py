from six import string_types

ALL_SELECTORS = frozenset(['id', 'name', 'xpath', 'link', 'partiallink', 'tag', 'class', 'css'])

def translate_selector(selector, webdriver):
    """
    Translate the selector into the selenium method to call
    :param selector:
    :param webdriver:
    :return:
    """
    if isinstance(selector, string_types):
        s = selector.split("=", maxsplit=1)
        selector = dict({s[0]: s[1]})  # specifying just a string.  css=something

    if 'id' in selector:
        return getattr(webdriver, 'find_element_by_id'), selector['id']
    elif 'name' in selector:
        return getattr(webdriver, 'find_element_by_name'), selector['name']
    elif 'xpath' in selector:
        return getattr(webdriver, 'find_element_by_xpath'), selector['xpath']
    elif 'link' in selector:
        return getattr(webdriver, 'find_element_by_link_text'), selector['link']
    elif 'partiallink' in selector:
        return getattr(webdriver, 'find_element_by_partial_link_text'), selector['partiallink']
    elif 'tag' in selector:
        return getattr(webdriver, 'find_element_by_tag_name'), selector['tag']
    elif 'class' in selector:
        return getattr(webdriver, 'find_element_by_class_name'), selector['class']
    elif 'css' in selector:
        return getattr(webdriver, 'find_element_by_css_selector'), selector['css']

    return None, None


def is_selector(string: str):
    """
    Check to see if this specific string is a selector
    :param string: the string to check
    :return:
    """
    try:
        sel = string.split("=", maxsplit=1)[0]
        return sel in ALL_SELECTORS
    except:
        return False


def has_selector(string: str):
    """
    Check to see if this specific string contains a selector
    :param string: the string to check
    :return:
    """

    try:
        sel = string.split("=")
        for possible in sel:
            if possible in ALL_SELECTORS:
                return True
        return False
    except:
        return False
