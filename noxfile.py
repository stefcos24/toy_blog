import nox


@nox.session
def tests(session):
    session.install(
        "django", "pytest", "djangorestframework", "django-environ"
    )
    session.run(
        "python",
        "manage.py",
        "test",
        "--keepdb",
        external=True,
    )


@nox.session
def lint(session):
    session.run(
        "flake8",
        "domain",
        external=True,
    )
