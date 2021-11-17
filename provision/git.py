from invoke import task


@task
def init_hooks(context):
    """Set up predefined hooks to the project's GIT repo."""
    context.run('cp git-hooks/* .git/hooks/')
