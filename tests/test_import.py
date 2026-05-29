"""Smoke test: the package imports and exposes a version."""

from __future__ import annotations


def test_package_imports() -> None:
    import motive_engine

    assert motive_engine.__version__


def test_version_is_string() -> None:
    from motive_engine import __version__

    assert isinstance(__version__, str)
    assert __version__.count(".") >= 1


def test_cli_app_imports() -> None:
    """Smoke test: the Typer app loads (and therefore so do schemas + utils)."""
    from motive_engine.cli import app

    assert app is not None
