import nox
from pathlib import Path

nox.options.sessions = []


@nox.session(python=False)
def dev(session) -> None:
    session.run("poetry", "install", "--no-root", "--with=dev", external=True)


@nox.session
def vendoring(session) -> None:
    session.install("vendoring")

    session.run("vendoring", "sync", "-v")
