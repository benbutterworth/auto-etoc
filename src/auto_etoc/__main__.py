from sys import stdout

from . import cli


def CLI():
    if not stdout.isatty():
        stdout.reconfigure(encoding="utf-8")  # to catch weird letters
    cli.app()
