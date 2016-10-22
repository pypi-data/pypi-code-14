from setuptools import setup, find_packages
from pip.req import parse_requirements


def get_requirements(filename):
    try:
        from pip.download import PipSession

        session = PipSession()
    except ImportError:
        session = None

    reqs = parse_requirements(filename, session=session)

    return [str(r.req) for r in reqs]


def get_package_meta():
    import imp

    mod_locals = {}

    execfile('tornado_retry/__about__.py', {}, mod_locals)

    ret = imp.new_module('tornado_retry.__about__')

    keys = mod_locals.get('__all__', mod_locals.keys())

    for name in keys:
        setattr(ret, name, mod_locals[name])

    return ret


meta = get_package_meta()


setup_args = dict(
    name='tornado-retry',
    version=meta.__version__,
    description=meta.__description__,
    maintainer='Nick Joyce',
    maintainer_email='nick+tornado-retry@boxdesign.co.uk',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt'),
)


if __name__ == '__main__':
    setup(**setup_args)
