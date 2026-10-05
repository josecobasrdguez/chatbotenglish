# -*- coding: utf-8 -*-
# (c) José Cobas Rodríguez

import html

import streamlit as st

from helpers.chat import (
    build_options,
    build_situacion_options,
    handle_user_message,
)
from helpers.conversation import get_messages, new_state, reset_chat, set_situacion
from helpers.factory import build_llm_client

st.set_page_config(
    page_title="English Practice Chatbot",
    page_icon="💬",
    layout="wide",
)

st.markdown(
    """
    <style>
    .block-container {
        max-width: 2100px;   /* Ajusta a tu gusto */
        margin: 0 auto;      /* ← Centrado */
        padding-top: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

if "conversation" not in st.session_state:
    st.session_state.conversation = new_state()
if "client" not in st.session_state:
    st.session_state.client = build_llm_client()

state = st.session_state.conversation
client = st.session_state.client

tema_titulos, temas = build_options()
tema_titulo = st.session_state.get("tema_key")
if tema_titulo not in tema_titulos:
    tema_titulo = tema_titulos[0]

sit_titulos, sit_ids = build_situacion_options(temas[tema_titulo])
sit_titulo = st.session_state.get("sit_key")
if sit_titulo not in sit_titulos:
    sit_titulo = sit_titulos[0]

selected_situacion_id = sit_ids[sit_titulo]
if state["situacion_id"] != selected_situacion_id:
    set_situacion(state, selected_situacion_id)
    st.session_state["tema_key"] = tema_titulo
    st.session_state["sit_key"] = sit_titulo

st.markdown(
    "<h1>💬 English Practice Chatbot</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    f'<p class="situation-caption">'
    f"Tema: {html.escape(tema_titulo)} · Situación: {html.escape(sit_titulo)}"
    f"</p>",
    unsafe_allow_html=True,
)

for message in get_messages(state):
    with st.chat_message(message["role"]):
        st.write(message["content"])

col1, col2, col3 = st.columns([8, 12, 2], vertical_alignment="bottom")
with col1:
    st.selectbox("Tema", tema_titulos, key="tema_key")
with col2:
    st.selectbox("Situación", sit_titulos, key="sit_key")
with col3:
    if st.button("Nuevo chat"):
        reset_chat(state)
        st.rerun()

if user_input := st.chat_input("Write in English..."):
    handle_user_message(state, client, user_input)
    st.rerun()
