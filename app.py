
"""Streamlit UI for the Cognetix Electronics support chatbot."""

import streamlit as st

from src.guard import check_scope
from src.llm import stream_response
from src.prompts import (
    FALLBACK_SENTENCE,
    build_system_prompt,
    load_policy,
)

MAX_TURN_MESSAGES = 10


st.set_page_config(
    page_title="Cognetix Support Chatbot",
    page_icon="🤖",
    layout="centered",
)

st.title("🤖 Cognetix Electronics Support")
st.caption(
    "Ask about orders, shipping, returns, refunds, warranties, "
    "payments, or support hours."
)

st.info(
    "Demo notice: This chatbot uses fictional store policies and "
    "cannot access real orders, accounts, or payment records."
)


@st.cache_data(show_spinner=False)
def get_policy() -> str:
    """Cache the read-only policy file."""
    return load_policy()


try:
    policy = get_policy()
except RuntimeError:
    st.error("The store policy could not be loaded. Check data/policy.txt.")
    st.stop()

system_prompt = build_system_prompt(policy)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous conversation messages.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input("How can we help you?"):
    # Display and store the current user message.
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    allowed, fallback = check_scope(prompt)

    with st.chat_message("assistant"):
        if not allowed:
            answer = fallback or FALLBACK_SENTENCE
            st.markdown(answer)
        else:
            # Include the system prompt separately from conversation memory.
            # Only the most recent MAX_TURN_MESSAGES are sent to the LLM.
            history = st.session_state.messages[-MAX_TURN_MESSAGES:]
            api_messages = [
                {"role": "system", "content": system_prompt},
                *history,
            ]

            answer = st.write_stream(stream_response(api_messages))

            if not answer:
                answer = FALLBACK_SENTENCE
                st.markdown(answer)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )

    # Keep at most ten messages in session memory (five complete exchanges).
    st.session_state.messages = (
        st.session_state.messages[-MAX_TURN_MESSAGES:]
    )
