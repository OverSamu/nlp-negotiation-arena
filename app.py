import pandas as pd
import streamlit as st
from openai import OpenAI

from agents.fair_agent import FairAgent
from agents.profit_agent import ProfitAgent
from environment.negotiation_game import NegotiationGame
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
        event = run_negotiation_step(st.session_state.game)

        st.session_state.chat.append(event)

        if st.session_state.game.is_agreement():
            st.session_state.finished = True

with col2:
    if st.button("🔄 Reset"):
        st.session_state.clear()
        st.rerun()

st.divider()

current_round = st.session_state.game.round if "game" in st.session_state else 0
st.caption(f"🕒 Round: {current_round + 1}")

st.subheader("💬 Conversation")

prompt = st.chat_input("⚖️ As a judge, you can provide feedback or suggestions to the agents.")
if prompt:
    st.session_state.chat.append({
        "agent": "Judge",
        "message": prompt,
        "shares": {}
    })
    st.session_state.game.add_judge_feedback(prompt)


for msg in st.session_state.chat:
    shares = {agent: f"{share}%" for agent, share in msg['shares'].items()}
    with st.chat_message(msg["agent"], avatar="⚖️" if msg["agent"] == "Judge" else None):
        st.markdown(f"**{msg['agent']}**")
        st.markdown(msg["message"])
        if shares:
            st.caption(f"📊 Proposes: {shares}")

if st.session_state.finished:
    st.success("✅ Agreement reached!")

df = pd.DataFrame(st.session_state.game.get_agent_proposals_in_rounds(),
                  columns=[a.name for a in st.session_state.game.agents])

st.line_chart(df, x_label="Round", y_label="Proposed Share (%)")
