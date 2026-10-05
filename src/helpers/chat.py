"""Lógica de conversación reutilizable por la UI (T6).

Funciones puras extraídas de la capa visual para poder probarlas:
construcción de opciones de Tema→Situación y procesamiento del input
del usuario (turnos + llamada al cliente LLM).
"""

from __future__ import annotations

from helpers.conversation import append_turn, get_messages, get_system_prompt
from helpers.llm import LLMClient
from helpers.scenarios import TEMAS


def build_options() -> tuple[list[str], dict[str, dict]]:
    """Devuelve (títulos de temas, dict {título del tema: tema})."""
    temas = {t["titulo"]: t for t in TEMAS}
    return list(temas.keys()), temas


def build_situacion_options(tema: dict) -> tuple[list[str], dict[str, str]]:
    """Devuelve (títulos de situaciones, dict {título: id de situación})."""
    opciones = {s["titulo"]: s["id"] for s in tema["situaciones"]}
    return list(opciones.keys()), opciones


def handle_user_message(state: dict, client: LLMClient, user_input: str) -> str:
    """Procesa el input del usuario: guarda el turno, pide respuesta y la guarda."""
    append_turn(state, "user", user_input)
    reply = client.get_reply(get_messages(state), get_system_prompt(state) or "")
    append_turn(state, "assistant", reply)
    return reply