from invoke import Exit, UnexpectedExit, task

from provision import common, django, linters


@task
def hooks(context):
    """Set up predefined hooks to the project's GIT repo."""
    context.run('cp .git-hooks/* .git/hooks/')


@task
def pre_push(context):
    """Perform pre push check."""
    common.success("Perform pre-push check")
    code_style_passed = _run_check(
        context=context,
        checker=linters.all,
        error_msg="Code style checks failed!",
    )
    migrations_passed = _run_check(
        context=context,
        checker=django.check_new_migrations,
        error_msg="New migrations were added!\nPlease commit them!",
    )
    if not all((
        migrations_passed,
        code_style_passed,
    )):
        common.error("Push aborted due to errors\nPLS fix them first!")
        raise Exit(code=1)
    common.success("Wonderful JOB! Thank You!")


def _run_check(context, checker, error_msg: str, *args, **kwargs):
    try:
        checker(context, *args, **kwargs)
    except (UnexpectedExit, Exit):
        common.warn(error_msg)
        return False
    return True


def gitmessage(context):
    """Set default .gitmessage."""
    common.success("Deploy git commit message template")
    context.run("echo '[commit]' >> .git/config")
    context.run("echo '  template = .gitmessage' >> .git/config")
