"""Utilities for retrieving ServUO and Ultima Online update data."""

import logging
from typing import Dict

import feedparser
import requests
import streamlit as st

SERVUO_RELEASES_API = "https://api.github.com/repos/ServUO/ServUO/releases/latest"
ULTIMA_FEED_URL = "https://uo.com/feed/"


def _fetch_servuo_updates() -> Dict[str, Dict[str, Dict[str, str]]]:
    """Fetch latest ServUO release information from GitHub."""
    try:
        response = requests.get(SERVUO_RELEASES_API, timeout=10)
        response.raise_for_status()
        data = response.json()
        version = data.get("name") or data.get("tag_name", "Unknown Version")
        description = (data.get("body") or "").replace("\r\n", " ").strip()
        url = data.get("html_url", "")
        return {
            "Highlights": {
                version: {"Description": description, "Documentation": url}
            }
        }
    except Exception as exc:  # pragma: no cover - network failures
        logging.error("Error fetching ServUO updates: %s", exc)
        return {"Highlights": {}}


def _fetch_ultima_online_updates() -> Dict[str, Dict[str, Dict[str, str]]]:
    """Fetch latest Ultima Online publish information from RSS feed."""
    try:
        feed = feedparser.parse(ULTIMA_FEED_URL)
        for entry in feed.entries:
            if "publish" in entry.title.lower():
                version = entry.title
                description = getattr(entry, "summary", "").strip()
                url = entry.link
                return {
                    "Highlights": {
                        version: {"Description": description, "Documentation": url}
                    }
                }
        return {"Highlights": {}}
    except Exception as exc:  # pragma: no cover - network failures
        logging.error("Error fetching Ultima Online updates: %s", exc)
        return {"Highlights": {}}


@st.cache_data(show_spinner=False)
def load_game_updates() -> Dict[str, Dict[str, Dict[str, Dict[str, str]]]]:
    """Return latest updates for ServUO and Ultima Online."""
    return {
        "ServUO": _fetch_servuo_updates(),
        "UltimaOnline": _fetch_ultima_online_updates(),
    }
