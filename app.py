import json
import os

import streamlit as st

from rag.rag_chain import generate_rag_response

from rag.session_manager import (
    create_new_session,
    save_session,
    load_session,
    get_all_sessions,
    update_session_title,
    delete_session,
    rename_session
)

# ------------ PAGE CONFIG --------------
st.set_page_config(
    page_title="RAG Chatbot",
    layout="centered"
)

# # ------------ CHAT STORAGE --------------
# CHAT_HISTORY_FILE = "chat_history.json"

# def load_chat_history():

#     if os.path.exists(CHAT_HISTORY_FILE):

#         with open(CHAT_HISTORY_FILE, "r") as file:
#             return json.load(file)

#     return []


# def save_chat_history(messages):

#     with open(CHAT_HISTORY_FILE, "w") as file:
#         json.dump(messages, file, indent=4)
        
        
#------------ SESSION STATE --------------

if "current_session" not in st.session_state:
    st.session_state.current_session = create_new_session()

if "processing" not in st.session_state:
    st.session_state.processing = False
    
if "rename_mode" not in st.session_state:

    st.session_state.rename_mode = None
    
# ----------- SIDEBAR --------------

with st.sidebar:

    st.title("💬 Conversations")

    # -------- NEW CHAT BUTTON --------

    if st.button("+ New Chat"):

        st.session_state.current_session = create_new_session()

        st.session_state.processing = False

        st.rerun()

    st.markdown("---")

    # -------- LOAD ALL SESSIONS --------

    sessions = get_all_sessions()

    for session in sessions:

        col1, col2, col3 = st.columns([5, 1, 1])

        # -------- SESSION BUTTON --------

        with col1:

            if st.button(
                session["title"],
                key=f"load_{session['session_id']}"
            ):

                loaded_session = load_session(
                    session["session_id"]
                )

                st.session_state.current_session = (
                    loaded_session
                )

                st.session_state.processing = False

                st.rerun()

        # -------- RENAME BUTTON --------

        with col2:

            if st.button(
                "✏️",
                key=f"rename_{session['session_id']}"
            ):

                st.session_state.rename_mode = (
                    session["session_id"]
                )

        # -------- DELETE BUTTON --------

        with col3:

            if st.button(
                "🗑",
                key=f"delete_{session['session_id']}"
            ):

                delete_session(session["session_id"])

                # Active session deleted
                if (
                    st.session_state.current_session[
                        "session_id"
                    ]
                    == session["session_id"]
                ):

                    st.session_state.current_session = (
                        create_new_session()
                    )

                st.rerun()

        # -------- RENAME INPUT --------

        if (
            st.session_state.rename_mode
            == session["session_id"]
        ):

            new_title = st.text_input(

                "New title",

                value=session["title"],

                key=f"text_{session['session_id']}"
            )

            if st.button(
                "Save",
                key=f"save_{session['session_id']}"
            ):

                rename_session(
                    session["session_id"],
                    new_title
                )

                # Update active session too
                if (
                    st.session_state.current_session[
                        "session_id"
                    ]
                    == session["session_id"]
                ):

                    st.session_state.current_session[
                        "title"
                    ] = new_title

                st.session_state.rename_mode = None

                st.rerun()
        
# ----------- MAIN CONTENT --------------

st.title("RAG Chatbot")
st.caption("Powered by Llama 3.1")

# ------------ DISPLAY CHAT HISTORY --------------

messages = st.session_state.current_session["messages"]

for message in messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# ------------ USER INPUT --------------

prompt = None

if not st.session_state.processing:
    prompt = st.chat_input("Type your message here...")
    
# ----------- PROCESS USER INPUT --------------

if prompt:

    st.session_state.processing = True

    st.session_state.current_session["messages"].append(
        {
            "role": "user",
            "content": prompt
        }
    )

    # Update title automatically
    st.session_state.current_session = (
        update_session_title(
            st.session_state.current_session
        )
    )

    # Save session
    save_session(
        st.session_state.current_session
    )

    st.rerun()
    
# ----------- GENERATE RESPONSE --------------

messages = st.session_state.current_session["messages"]

if (
    st.session_state.processing
    and len(messages) > 0
    and messages[-1]["role"] == "user"
):

    user_question = messages[-1]["content"]

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            bot_reply = generate_rag_response(
                user_question
            )

            st.markdown(bot_reply)

    # Save assistant response
    st.session_state.current_session["messages"].append(
        {
            "role": "assistant",
            "content": bot_reply
        }
    )

    # Save session again
    save_session(
        st.session_state.current_session
    )

    # Unlock input
    st.session_state.processing = False

    st.rerun()
    
    