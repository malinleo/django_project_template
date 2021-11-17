from invoke import task

DEFAULT_FOLDERS = 'apps provision tasks.py'


@task
def flake8(context, path=DEFAULT_FOLDERS, params=""):
    """Start flake8 checks for pre-commit."""
    context.run(f'flake8 {path} {params}')


@task
def isort(context, path=DEFAULT_FOLDERS, params=""):
    """Start isort checks for pre-commit."""
    context.run(f'isort {path} {params}')
