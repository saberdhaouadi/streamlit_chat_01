[Oimport streamlit as st
import json
import os
import time
import hashlib
from datetime import datetime

# ── Config ──────────────────────────────────────────────────────────────────
MESSAGES_FILE = "messages.json"
ROOM_PASSWORD  = "friends2024"          # ← Change this!
MAX_MESSAGES   = 200                    # keep last N messages
REFRESH_SECS   = 3                      # auto-refresh interval

USER_COLORS = [
    "#FF6B6B", "#FFD93D", "#6BCB77", "#4D96FF",
    "#FF922B", "#CC5DE8", "#20C997", "#F06595",
    "#74C0FC", "#A9E34B",
]

# ── Helpers ──────────────────────────────────────────────────────────────────

def load_messages():
    if not os.path.exists(MESSAGES_FILE):
        return []
    try:
        with open(MESSAGES_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []


def save_message(username: str, text: str):
    msgs = load_messages()
    msgs.append({
        "user": username,
        "text": text,
        "ts": datetime.now().strftime("%H:%M"),
    })
    msgs = msgs[-MAX_MESSAGES:]
    with open(MESSAGES_FILE, "w") as f:
        json.dump(msgs, f)


def color_for(username: str) -> str:
    idx = int(hashlib.md5(username.encode()).hexdigest(), 16) % len(USER_COLORS)
    return USER_COLORS[idx]


def check_password(pwd: str) -> bool:
    return pwd.strip() == ROOM_PASSWORD


# ── Page setup ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Friends Chat",
    page_icon="💬",
    layout="centered",
)

st.markdown("""
<style>
/* ── Global ── */
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background: #0d0f14;
    color: #e8eaf0;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header {visibility: hidden;}
.block-container {padding-top: 2rem; max-width: 720px;}

/* ── Login card ── */
.login-wrap {
    background: #161923;
    border: 1px solid #2a2d3a;
    border-radius: 16px;
    padding: 2.5rem 2rem;
    margin: 4rem auto;
    max-width: 380px;
    text-align: center;
    box-shadow: 0 8px 40px rgba(0,0,0,.5);
}
.login-wrap h1 {font-family:'Space Mono',monospace; font-size:1.6rem; margin-bottom:.3rem; color:#fff;}
.login-wrap p  {color:#7b8090; font-size:.9rem; margin-bottom:1.5rem;}

/* ── Header bar ── */
.chat-header {
    display:flex; align-items:center; justify-content:space-between;
    background:#161923; border:1px solid #2a2d3a; border-radius:12px;
    padding:.75rem 1.2rem; margin-bottom:1rem;
}
.chat-header-title {font-family:'Space Mono',monospace; font-size:1rem; color:#fff; font-weight:700;}
.chat-header-user  {font-size:.85rem; color:#7b8090;}
.online-dot {display:inline-block; width:8px; height:8px; border-radius:50%;
             background:#6BCB77; margin-right:6px; box-shadow:0 0 6px #6BCB77;}

/* ── Message list ── */
.msg-container {
    background:#161923; border:1px solid #2a2d3a; border-radius:12px;
    padding:1rem 1.2rem; height:420px; overflow-y:auto;
    display:flex; flex-direction:column; gap:.6rem;
    margin-bottom:.8rem;
}
.msg-row { display:flex; flex-direction:column; }
.msg-meta { font-size:.72rem; color:#555a6e; margin-bottom:.15rem; }
.msg-meta span { font-weight:600; }
.msg-bubble {
    display:inline-block; max-width:75%; padding:.5rem .9rem;
    border-radius:0 12px 12px 12px; font-size:.92rem; line-height:1.45;
    background:#1e2130; color:#dde1f0; word-break:break-word;
}
.msg-row.me { align-items:flex-end; }
.msg-row.me .msg-meta { text-align:right; }
.msg-row.me .msg-bubble {
    border-radius:12px 0 12px 12px;
    background: linear-gradient(135deg,#4D96FF22,#4D96FF44);
    border:1px solid #4D96FF55;
    color:#e8edf8;
}
.msg-date-divider {
    text-align:center; font-size:.72rem; color:#3a3f52;
    border-top:1px solid #222639; padding-top:.5rem; margin:.3rem 0;
}

/* ── Input row ── */
.stTextInput > div > div > input {
    background:#161923 !important;
    border:1px solid #2a2d3a !important;
    border-radius:10px !important;
    color:#e8eaf0 !important;
    font-family:'DM Sans',sans-serif !important;
    font-size:.95rem !important;
    padding:.55rem .9rem !important;
}
.stTextInput > div > div > input:focus {
    border-color:#4D96FF !important;
    box-shadow:0 0 0 3px #4D96FF22 !important;
}
.stButton > button {
    background: linear-gradient(135deg,#4D96FF,#6B6BFF) !important;
    color:#fff !important; border:none !important;
    border-radius:10px !important; padding:.55rem 1.4rem !important;
    font-family:'DM Sans',sans-serif !important; font-weight:600 !important;
    font-size:.9rem !important; cursor:pointer !important;
    transition:opacity .15s !important;
}
.stButton > button:hover { opacity:.85 !important; }
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "last_count" not in st.session_state:
    st.session_state.last_count = 0

# ── Login screen ──────────────────────────────────────────────────────────────
if not st.session_state.authenticated:
    st.markdown('<div class="login-wrap">', unsafe_allow_html=True)
    st.markdown('<h1>💬 Friends Chat</h1>', unsafe_allow_html=True)
    st.markdown('<p>Private room — enter your nickname & room password</p>', unsafe_allow_html=True)

    nick = st.text_input("Nickname", placeholder="e.g. Alex", key="nick_input")
    pwd  = st.text_input("Room Password", type="password", placeholder="Ask a friend for it", key="pwd_input")

    if st.button("Join Room →"):
        if not nick.strip():
            st.error("Please enter a nickname.")
        elif not check_password(pwd):
            st.error("Wrong password. Try again.")
        else:
            st.session_state.username = nick.strip()[:20]
            st.session_state.authenticated = True
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ── Chat screen ───────────────────────────────────────────────────────────────
username = st.session_state.username
my_color  = color_for(username)

# Header
st.markdown(f"""
<div class="chat-header">
  <span class="chat-header-title">💬 Friends Chat</span>
  <span class="chat-header-user">
    <span class="online-dot"></span>
    Logged in as <b style="color:{my_color}">{username}</b>
  </span>
</div>
""", unsafe_allow_html=True)

# ── Message display ───────────────────────────────────────────────────────────
messages = load_messages()

bubbles_html = '<div class="msg-container" id="msg-end">'
for m in messages:
    u    = m["user"]
    txt  = m["text"]
    ts   = m.get("ts", "")
    clr  = color_for(u)
    side = "me" if u == username else ""
    bubbles_html += f"""
    <div class="msg-row {side}">
      <div class="msg-meta"><span style="color:{clr}">{u}</span>  {ts}</div>
      <div class="msg-bubble">{txt}</div>
    </div>"""

bubbles_html += "</div>"
bubbles_html += """<script>
  var c=document.getElementById('msg-end');
  if(c) c.scrollTop=c.scrollHeight;
</script>"""
st.markdown(bubbles_html, unsafe_allow_html=True)

# ── Send message ─────────────────────────────────────────────────────────────
col1, col2 = st.columns([5, 1])
with col1:
    new_msg = st.text_input(
        "message", label_visibility="collapsed",
        placeholder="Type a message…", key="msg_input"
    )
with col2:
    send = st.button("Send")

if send and new_msg.strip():
    save_message(username, new_msg.strip())
    st.rerun()

# ── Logout ────────────────────────────────────────────────────────────────────
with st.expander("⚙️ Options"):
    if st.button("Leave room"):
        st.session_state.authenticated = False
        st.session_state.username = ""
        st.rerun()
    st.caption(f"Auto-refreshes every {REFRESH_SECS}s · Messages capped at {MAX_MESSAGES}")

# ── Auto-refresh ──────────────────────────────────────────────────────────────
time.sleep(REFRESH_SECS)
st.rerun()
