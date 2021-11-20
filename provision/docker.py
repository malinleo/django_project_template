from invoke import task

from provision import common


@task
def clear(context):
    """Stop and remove all containers defined in docker-compose.

    Also remove images.

    """
    common.success("Clearing docker-compose")
    context.run("docker-compose rm -f")
    context.run("docker-compose down -v --rmi all --remove-orphans")
