"""Selector de cliente LLM (T4/T7).

Decide en runtime qué cliente usar: ``GeminiClient`` si existe una API key,
``MockClient`` en caso contrario (modo demo sin credenciales).

La key se busca (en orden) en: argumento explícito → variable de entorno
``GEMINI_API_KEY`` → secret de Streamlit (``.streamlit/secrets.toml``).
"""

from __future__ import annotations

import os

from helpers.gemini_client import _ENV_KEY_VAR, GeminiClient
from helpers.llm import LLMClient, MockClient


def build_llm_client(api_key: str | None = None) -> LLMClient:
    """Devuelve ``GeminiClient`` si hay API key (arg, env o st.secrets); si no, ``MockClient``."""
    key = api_key or os.environ.get(_ENV_KEY_VAR) or _read_streamlit_secret()
    if key:
        return GeminiClient(api_key=key)
    return MockClient()


def _read_streamlit_secret() -> str | None:
    """Lee ``st.secrets["GEMINI_API_KEY"]`` sólo si se corre dentro de Streamlit.

    Fuera del runtime de Streamlit (p.ej. en los tests) ``st.secrets`` lanza
    una excepción, que se traga para no romper ni exponer nada.
    """
    try:
        import streamlit as st  # noqa: PLC0415

        return st.secrets.get(_ENV_KEY_VAR)
    except Exception:
        return None