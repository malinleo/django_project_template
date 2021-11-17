from invoke import task


@task
def run(context, path='', params=''):
    """Run tests with arguments configured in pytest.ini."""
    context.run(f'pytest {path} {params}')
