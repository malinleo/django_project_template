from invoke import task


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
