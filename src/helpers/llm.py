"""Cliente de LLM: interfaz común y cliente simulado (T2).

Design goals:
- `LLMClient`: abstracción única para el resto de la aplicación.
- `MockClient`: cliente determinista para ejecutar la app sin red ni API key.
"""

from abc import ABC, abstractmethod


class LLMClient(ABC):
    """Interfaz común para clientes de LLM.

    Los mensajes usan el formato estándar: lista de dicts con
    ``{"role": "user" | "assistant", "content": str}``.
    """

    @abstractmethod
    def get_reply(self, messages: list, system_prompt: str) -> str:
        """Devuelve la respuesta del asistente al historial dado."""
        raise NotImplementedError


class MockClient(LLMClient):
    """Cliente simulado: determinista, sin red y sin necesidad de API key.

    Responde en inglés con un prefijo que deja claro que es una simulación,
    para que el usuario puedan distinguirla de una respuesta real de Gemini.
    """

    PREFIX = "[Demo response]"

    def get_reply(self, messages: list, system_prompt: str) -> str:
        last_user_message = self._last_user_message(messages)
        return f"{self.PREFIX} You said: {last_user_message}"

    @staticmethod
    def _last_user_message(messages: list) -> str:
        for message in reversed(messages):
            if message.get("role") == "user":
                return message.get("content", "")
        raise ValueError("No hay mensajes de usuario en el historial")