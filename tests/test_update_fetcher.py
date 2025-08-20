"""Tests for update_fetcher module."""

import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from update_fetcher import _fetch_servuo_updates, _fetch_ultima_online_updates


def test_fetch_servuo_updates_structure():
    data = _fetch_servuo_updates()
    assert "Highlights" in data
    assert isinstance(data["Highlights"], dict)


def test_fetch_ultima_online_updates_structure():
    data = _fetch_ultima_online_updates()
    assert "Highlights" in data
    assert isinstance(data["Highlights"], dict)
