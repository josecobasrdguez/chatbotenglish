"""Gestión de estado de conversación (T5).

Helpers puros que operan sobre un dict de estado (p.ej. uno guardado en
``st.session_state``) sin depender de Streamlit, para poder probarlos en
aislamiento. El estado incluye el historial de turnos, la situación
seleccionada y el prompt de sistema asociado.
"""

from __future__ import annotations

from helpers.scenarios import get_situacion

_VALID_ROLES = ("user", "assistant")


def new_state() -> dict:
    """Estado inicial razonable: sin situación, sin prompt, sin historial."""
    return {
        "situacion_id": None,
        "system_prompt": None,
        "messages": [],
    }


def set_situacion(state: dict, situacion_id: str) -> dict:
    """Selecciona una situación e inicia un chat nuevo con su prompt.

    Si la situación no existe, lanza ``KeyError``. Al cambiar de situación
    se limpia el historial (nuevo chat).
    """
    situacion = get_situacion(situacion_id)
    state["situacion_id"] = situacion["id"]
    state["system_prompt"] = situacion["prompt"]
    state["messages"] = []
    return state


def append_turn(state: dict, role: str, content: str) -> dict:
    """Añade un turno respetando el orden del historial."""
    if role not in _VALID_ROLES:
        raise ValueError(f"Rol inválido: {role}")
    state["messages"].append({"role": role, "content": content})
    return state


def reset_chat(state: dict) -> dict:
    """Limpia el historial conservando la selección de situación."""
    state["messages"] = []
    return state


def get_messages(state: dict) -> list:
    """Devuelve el historial de mensajes para el cliente LLM."""
    return state["messages"]


def get_system_prompt(state: dict) -> str | None:
    """Devuelve el prompt de sistema de la situación actual (o None)."""
    return state["system_prompt"]