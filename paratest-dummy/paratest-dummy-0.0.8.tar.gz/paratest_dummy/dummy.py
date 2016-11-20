def find(path, test_pattern, file_pattern, output_path):
    items = {'foo': 'echo foo', 'bar': 'echo bar', 'bazz': 'echo bazz'}
    for item in items.items():
        yield item
