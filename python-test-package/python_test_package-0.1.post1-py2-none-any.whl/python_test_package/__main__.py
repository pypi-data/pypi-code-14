if __name__ == '__main__':
    import pkg_resources

    name = 'python-test-package'
    print '{}=={}'.format(name, pkg_resources.get_distribution(name).version)

    import pdb; pdb.set_trace()
