import invoke


@invoke.task
def release(ctx):
    """
    Publishes the project on PyPI.

    We have automatic publishing enabled on TRAVIS build, so this is not
    necessary... but I'll keep here for reference.
    """
    ctx.run("python setup.py sdist upload")


@invoke.task
def test(ctx):
    """
    Executes all the tests.
    """
    ctx.run("python setup.py pytest")


@invoke.task
def travis_setpass(ctx):
    """
    Stores the PyPI password (encrypted) in the .travis.yml file.
    """
    print("travis encrypt --add deploy.password")


