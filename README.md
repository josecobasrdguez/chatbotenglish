# English Practice Chatbot (Gemini + Streamlit)

Chatbot de Streamlit para practicar inglés hablado/escrito con Google Gemini.
Elige un **Tema** y una **Situación** en el menú; cada situación
inyecta un prompt de sistema específico que fija el rol del asistente, cómo
iniciar el diálogo, cuándo pausar esperando tu respuesta, el cierre con
expresiones de despedida y la regla de desvío de tema.

## Estructura

```
app.py                     # IU de Streamlit (capa visual mínima)
requirements.txt           # Dependencias de despliegue
src/helpers/
  scenarios.py             # Catálogo de 6 temas y 22 situaciones (T1)
  llm.py                   # Interfaz LLMClient + MockClient (T2)
  gemini_client.py         # Cliente de Google Gemini (T3)
  factory.py               # Selector de cliente según API key (T4)
  conversation.py          # Estado de conversación (T5)
  chat.py                  # Lógica pura reutilizable por la UI (T6)
tests/                     # Pruebas unitarias (pytest)
```

## Requisitos

- Python ≥ 3.11 (proyecto gestionado con [uv](https://docs.astral.sh/uv/))
- (Opcional) Clave de API de Google Gemini