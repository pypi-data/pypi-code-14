__all__ = [
    'execute_tag_chain'
]


def execute_tag_chain(tag_chain, data_container):
    if not tag_chain:
        return None

    data = data_container
    for element in tag_chain:
        data = element.execute(data)
    return data
