from invoke import Collection

from provision import django, git, linters, project, tests

ns = Collection(
    git,
    django,
    linters,
    project,
    tests,
)
