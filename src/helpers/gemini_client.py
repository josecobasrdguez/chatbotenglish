"""Cliente LLM para Google Gemini (T3).

Lee la API key de la variable de entorno ``GEMINI_API_KEY``.
Si no existe, no crashea pero el cliente queda sin clave.
Nunca expone la clave en logs ni en el contenido de los mensajes.
"""

from __future__ import annotations

import os
from typing import Any

from google import genai
from google.genai import types as genai_types

from helpers.llm import LLMClient

_ENV_KEY_VAR = "GEMINI_API_KEY"
_DEFAULT_MODEL = "gemini-3.6-flash"
_API_ERROR_MESSAGE = (
    "Sorry, there was a problem connecting to the AI. Please try again."
)


class GeminiClient(LLMClient):
    """Cliente que llama a la API de Google Gemini."""

    def __init__(self, api_key: str | None = None) -> None:
        self._api_key = api_key or os.environ.get(_ENV_KEY_VAR)
        self._client: genai.Client | None = (
            genai.Client(api_key=self._api_key) if self._api_key else None
        )

    @property
    def has_key(self) -> bool:
        return self._api_key is not None

    def get_reply(self, messages: list, system_prompt: str) -> str:
        if not self._client:
            raise ValueError("GEMINI_API_KEY no está configurada")
        contents = self._convert_messages(messages)
        try:
            response = self._client.models.generate_content(
                model=_DEFAULT_MODEL,
                contents=contents,
                config=genai_types.GenerateContentConfig(
                    system_instruction=system_prompt,
                ),
            )
            text = response.text
            if not text:
                return _API_ERROR_MESSAGE
            return text
        except Exception:
            return _API_ERROR_MESSAGE

    @staticmethod
    def _convert_messages(messages: list) -> list[dict[str, Any]]:
        contents: list[dict[str, Any]] = []
        for msg in messages:
            role = "model" if msg.get("role") == "assistant" else msg.get("role", "user")
            contents.append(
                {"role": role, "parts": [{"text": msg.get("content", "")}]}
            )
        return contents