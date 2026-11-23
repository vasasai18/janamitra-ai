"""Janamitra AI: zero-cost hackathon MVP (source-limited)."""
import os
import json
import streamlit as st
import streamlit.components.v1 as components
from core import answer_question, SOURCES

st.set_page_config(page_title="Janamitra AI | Pension Assistant", page_icon="🏛️", layout="centered")
st.title("🏛️ Janamitra AI")
st.caption("Andhra Pradesh pension information • Telugu / English • Official-source guidance")
st.info("Hackathon prototype: information only, not a government service. No application submission or eligibility approval.")

with st.sidebar:
    st.header("Settings")
    language = st.radio("Answer language", ["Telugu", "English"], horizontal=True)
    st.markdown("**Information sources**")
    st.markdown(f"[Official AP pension website]({SOURCES['scheme']})")
    st.markdown(f"[Published eligibility criteria]({SOURCES['eligibility']})")
    st.markdown(f"[2024 pension enhancement order]({SOURCES['order']})")
    st.warning("Official About page contains an older pension amount. We rely on the later 2024 order for ₹4,000.")
    st.caption("Do not enter Aadhaar, bank details, phone numbers or other private identifiers.")
    if st.button("Clear conversation"):
        st.session_state.pop("messages", None)
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

api_key = os.environ.get("GEMINI_API_KEY", "")
try:
    api_key = api_key or st.secrets.get("GEMINI_API_KEY", "")
except Exception:
    # Streamlit raises its own SecretsNotFound error when no secrets file exists.
    pass
model = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash-lite")

st.caption("🟢 Source-based FAQ mode" if not api_key else "🟢 Gemini-assisted mode with FAQ fallback")

for idx, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant":
            st.caption(("AI-assisted answer" if message.get("used_ai") else "Source-based FAQ answer") + " · Official references in sidebar · Verify current rules before applying.")
            # Browser Text-to-Speech: free, device/browser and Telugu voice dependent.
            rendered_text = json.dumps(message["content"], ensure_ascii=False).replace("</", "<\\/")
            lang_tag = "te-IN" if message.get("language", "Telugu") == "Telugu" else "en-IN"
            components.html(f"""<button type='button' onclick='speak()' style='background:#f5f5f5;border:1px solid #ddd;border-radius:8px;padding:6px 12px;cursor:pointer;'>🔊 Listen (if browser supports it)</button>
<script>function speak(){{if (!('speechSynthesis' in window)){{alert('Voice not supported by this browser');return;}}window.speechSynthesis.cancel();var u=new SpeechSynthesisUtterance({rendered_text});u.lang='{lang_tag}';window.speechSynthesis.speak(u);}}</script>""", height=42)

suggestions = ["What is the minimum age?", "How much pension per month?", "Am I eligible?", "How do I apply?"]
with st.expander("Try a sample question"):
    st.write(" • ".join(suggestions))

query = st.chat_input("Ask about Andhra Pradesh old-age pension… / Pension gurinchi adagandi")
if query:
    if len(query) > 1200:
        st.warning("Please ask a shorter question (up to 1,200 characters).")
    else:
        st.session_state.messages.append({"role": "user", "content": query})
        reply, used_ai = answer_question(query, language, api_key, model)
        st.session_state.messages.append({"role": "assistant", "content": reply, "used_ai": used_ai, "language": language})
        st.rerun()

st.divider()
st.caption("Prototype focus: AP NTR Bharosa old-age pension. Information may change; always verify current rules and application windows with government authorities.")
