from invoke import Exit, UnexpectedExit, task

from provision import common

DEFAULT_FOLDERS = 'apps provision tasks.py'


@task
def flake8(context, path=DEFAULT_FOLDERS, params=""):
    """Start flake8 checks for pre-commit."""
    common.success("Flake8 checks")
    context.run(f'flake8 {path} {params}')


@task
def isort(context, path=DEFAULT_FOLDERS, params=""):
    """Start isort fixes for pre-commit."""
    common.success("Isort checks")
    context.run(f'isort {path} {params}')


@task
def isort_check(context, path=DEFAULT_FOLDERS, params=""):
    """Start isort checks for pre-commit."""
    common.success("Isort checks")
    context.run(f'isort -c {path} {params}')


@task
def all(context, path=DEFAULT_FOLDERS):
    """Run all linters."""
    common.success("Linters: running all linters")
    linters = (isort_check, flake8)
    failed = []
    for linter in linters:
        try:
            linter(context, path)
        except UnexpectedExit:
            failed.append(linter.__name__)
    if failed:
        common.error(
            f"Linters failed: {', '.join(map(str.capitalize, failed))}",
        )
        raise Exit(code=1)
