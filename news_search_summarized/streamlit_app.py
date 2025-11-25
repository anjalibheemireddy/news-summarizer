import streamlit as st
from nodes import create_agent  # your current nodes file

# --- Initialize agent ---
agent = create_agent()

# --- Initialize session memory ---
if "messages" not in st.session_state:
    st.session_state.messages = []

st.set_page_config(page_title="News Summarizer Chat", layout="wide")
st.title("📰 News Summarizer Chat")

# --- Display previous messages ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- User input ---
if user_input := st.chat_input("Type your question here..."):

    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # --- Invoke agent directly ---
    output = agent.invoke({"question": user_input})

    # Extract summary and sources
    summary = output.get("final_answer") or output.get("answer") or ""
    search_results = output.get("search_results", {}).get("results", [])
    if search_results:
        sources_text = "\n\nSources:\n" + "\n".join([f"- {r['title']}: {r['url']}" for r in search_results])
        response_text = summary + sources_text
    else:
        response_text = summary

    # --- Add agent response ---
    st.session_state.messages.append({"role": "assistant", "content": response_text})
    with st.chat_message("assistant"):
        st.markdown(response_text)

