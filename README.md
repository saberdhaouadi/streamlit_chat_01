# 💬 Friends Chat — Private Streamlit App

A lightweight private chat room for ~10 friends, runs entirely on your machine (or a free cloud host).

---

## 🚀 Quick Start (Local)

```bash
# 1. Install dependency
pip install streamlit

# 2. Run the app
streamlit run chat_app.py
```

Open http://localhost:8501 in your browser. Share the URL (and password) with friends on the same network.

---

## 🔐 Changing the Password

Open `chat_app.py` and find line:

```python
ROOM_PASSWORD = "friends2024"   # ← Change this!
```

Replace `friends2024` with any password you like, then restart the app.

---

## ☁️ Deploy for Free (so friends outside your network can join)

### Option A — Streamlit Community Cloud (easiest, free)

1. Push the two files (`chat_app.py`, `requirements.txt`) to a **private** GitHub repo.
2. Go to https://share.streamlit.io → "New app" → pick your repo.
3. Deploy. You get a public URL like `https://yourapp.streamlit.app`.
4. Share the URL + password with your friends.

> ⚠️ Keep the GitHub repo **private** so strangers can't read your source (and password).

### Option B — Run on a VPS / home server

```bash
pip install streamlit
streamlit run chat_app.py --server.port 8501 --server.address 0.0.0.0
```

Open port 8501 on your firewall and share your public IP.

---

## ⚙️ Customisation

| Setting | Location | Default |
|---|---|---|
| Room password | `ROOM_PASSWORD` variable | `friends2024` |
| Auto-refresh rate | `REFRESH_SECS` variable | `3` seconds |
| Max stored messages | `MAX_MESSAGES` variable | `200` |

---

## 🗂️ Files

```
chat_app.py       ← the entire app (single file)
requirements.txt  ← pip dependency (streamlit only)
messages.json     ← created automatically, stores chat history
```

---

## 🔒 Privacy Notes

- Messages are stored **locally** in `messages.json` — no third-party servers.
- The room is protected by a shared password.
- For extra security on a public deployment, consider adding HTTPS via a reverse proxy (nginx + Let's Encrypt).
