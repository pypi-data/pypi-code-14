from invoke import Collection, task

@task
def test(ctx, coverage=False, flags=""):
	if "--verbose" not in flags.split():
		flags += " --verbose"
	runner = "python"
	if coverage:
		runner = "coverage run --source=loggers"
	ctx.run("{0} tests/test_loggers.py {1}".format(runner, flags), pty=True)

@task
def coverage(ctx):
	ctx.run("coverage run --source=loggers tests/test_loggers.py --verbose")

ns = Collection(test, coverage)
