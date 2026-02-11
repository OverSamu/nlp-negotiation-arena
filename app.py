import streamlit as st

from agents.fair_agent import FairAgent
from agents.profit_agent import ProfitAgent
from environment.negotiation_game import NegotiationGame
from model.llama_cpp_model import LlamaCppModel
from openai import OpenAI
from model.openai_model import OpenAIModel
from ui.negotiation_runner import run_negotiation_step

st.set_page_config(page_title="Negotiation Arena", layout="centered")
st.title("🤝 Negotiation Arena")

if "chat" not in st.session_state:
    st.session_state.chat = []

if "game" not in st.session_state:
    client = OpenAI()
    model = OpenAIModel(client, temperature=0.3)

    st.session_state.agent_a = ProfitAgent("Alice", model)
    st.session_state.agent_b = FairAgent("Bob", model)

    st.session_state.game = NegotiationGame([st.session_state.agent_a, st.session_state.agent_b])
    st.session_state.finished = False

col1, col2 = st.columns(2)

with col1:
    if st.button("▶️ Next step") and not st.session_state.finished:
        event, agreement = run_negotiation_step(st.session_state.game)

        st.session_state.chat.append(event)

        if agreement:
            st.session_state.finished = True

with col2:
    if st.button("🔄 Reset"):
        st.session_state.clear()
        st.rerun()

st.divider()

rounds = len(st.session_state.game.proposals) if "game" in st.session_state and st.session_state.game.proposals is not None else 0
st.caption(f"🕒 Rounds: {rounds}")

st.subheader("💬 Conversation")

for msg in st.session_state.chat:
    shares = {agent: f"{share}%" for agent, share in msg['shares'].items()}
    with st.chat_message(msg["agent"]):
        st.markdown(f"**{msg['agent']}**")
        st.markdown(msg["message"])
        st.caption(f"📊 Proposes: {shares}")

if st.session_state.finished:
    st.success("✅ Agreement reached!")
