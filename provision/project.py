import os

from invoke import task

from provision import common, django, docker, git, tests


def copylocal(context, force_update=True):
    """Copy local settings from template.

    Args:
        force_update(bool): rewrite file if exists or not
    """
    local_settings = "config/settings/local.py"
    local_template = "config/settings/local.template.py"

    if force_update or not os.path.isfile(local_settings):
        context.run(" ".join(["cp", local_template, local_settings]))


@task
def compile_deps(context):
    """Compile dependencies files."""
    envs = [
        'development',
        'production',
    ]
    for env in envs:
        context.run(
            f'pip-compile ./requirements/{env}.in '
            f'-o ./requirements/{env}.txt '
            '-v'
        )


@task
def install_tools(context):
    """Install tools needed to install requirements."""
    context.run("pip install -U pip pip-tools setuptools wheel")


@task
def install_requirements(context, env='development'):
    """Install requirements."""
    context.run(f'pip install -r requirements/{env}.txt')


@task
def init(context, clean=False):
    """Prepare env for working with project."""
    common.success("Setting up git config")
    git.hooks(context)
    git.gitmessage(context)
    common.success("Initial assembly of all dependencies")
    install_tools(context)
    if clean:
        docker.clear(context)
    copylocal(context)
    install_requirements(context)
    django.migrate(context)
    django.set_default_site(context)
    tests.run(context)
    django.createsuperuser(context)
    common.success("Everything is done, happy coding!")
