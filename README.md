<div align="center">

# ⚡ OpenClaw
### *AI that actually feels simple.*

**The normie-friendly AI chat app — built with Python + Django + Groq**

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Django](https://img.shields.io/badge/Django-4.2-092E20?style=flat-square&logo=django&logoColor=white)](https://djangoproject.com)
[![Groq](https://img.shields.io/badge/Powered%20by-Groq-F55036?style=flat-square&logoColor=white)](https://groq.com)
[![License](https://img.shields.io/badge/License-MIT-22c55e?style=flat-square)](LICENSE)
[![Deploy](https://img.shields.io/badge/Deploy-Railway-0B0D0E?style=flat-square&logo=railway&logoColor=white)](https://railway.app)

<br/>

> 💡 *"Making OpenClaw normie-friendly is the biggest opportunity in the world today."*
> — OpenClaw Challenge Brief

<br/>

[🚀 Live Demo](https://your-url.railway.app) &nbsp;•&nbsp; [📹 Demo Video](#) &nbsp;•&nbsp; [🐛 Report Bug](https://github.com/CoderParva/openclaw/issues)

</div>

---

## 🌟 What is OpenClaw?

OpenClaw is what happens when you take a powerful AI tool and make it **actually usable by everyone** — not just developers.

Inspired by what ChatGPT did to GPT-3, OpenClaw wraps the raw experience in a **beautiful, intuitive interface** that anyone can use in seconds. No terminal. No API docs. No confusion.

Just open, paste your key, and chat. ⚡

---

## ✨ Features

| Feature | Description |
|---|---|
| 🧠 **4 AI Models** | Llama 3 70B, Llama 3 8B, Mixtral 8x7B, Gemma 2 9B — all free |
| 💬 **Multiple Chats** | Create, switch, pin, rename and delete conversations |
| 🎨 **6 Custom Themes** | Purple, Cyan, Green, Amber, Red, Pink — saved across sessions |
| 🔊 **Text-to-Speech** | Read any AI response aloud with one click |
| ⬇ **Export Chats** | Download any conversation as a `.txt` file |
| 📌 **Pin Messages** | Pin important messages and entire chats |
| 🔄 **Regenerate** | Retry the last AI response instantly |
| ⚡ **Real Streaming** | Server-side streaming via Django + Groq API |
| 🔒 **Private** | API key stored in session — nothing sent to third parties |
| 📱 **Responsive** | Works perfectly on desktop, tablet, and mobile |
| 🌐 **Landing Page** | Beautiful animated landing page with scroll transitions |
| 🐍 **Django Backend** | Real database, REST API, production-ready architecture |

---

## 🛠 Tech Stack

```
Frontend   →  HTML5 · CSS3 · Vanilla JavaScript
Backend    →  Python 3.11 · Django 4.2
AI         →  Groq API (Llama 3 · Mixtral · Gemma 2)
Streaming  →  Django StreamingHttpResponse + Server-Sent Events
Database   →  SQLite (development)
Deploy     →  Railway · Gunicorn · Whitenoise
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- A free Groq API key from [console.groq.com](https://console.groq.com) — no credit card needed

### Local Setup

```bash
# 1. Clone the repo
git clone https://github.com/CoderParva/openclaw.git
cd openclaw

# 2. Create a virtual environment
python -m venv venv

# 3. Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run migrations
python manage.py migrate

# 6. Start the server
python manage.py runserver
```

Open **http://127.0.0.1:8000**, paste your Groq API key, and start chatting! 🎉

---

## 🌐 API Endpoints

```
GET     /api/chats/                →  List all chats
POST    /api/chats/create/         →  Create a new chat
GET     /api/chats/<id>/           →  Get chat with all messages
PATCH   /api/chats/<id>/           →  Rename or pin a chat
DELETE  /api/chats/<id>/           →  Delete a chat
POST    /api/chats/<id>/stream/    →  Stream AI response (SSE)
GET     /api/chats/<id>/export/    →  Export chat as .txt file
POST    /api/messages/<id>/pin/    →  Pin or unpin a message
```

---

## 📁 Project Structure

```
openclaw/
├── config/
│   ├── settings.py       # Django configuration
│   ├── urls.py           # URL routing
│   └── wsgi.py           # WSGI entry point
├── chat/
│   ├── models.py         # Chat & Message database models
│   ├── views.py          # API views + Groq streaming
│   └── migrations/       # Database migrations
├── templates/
│   └── index.html        # Full frontend (landing page + chat UI)
├── requirements.txt      # Python dependencies
├── Procfile              # Railway deployment config
└── railway.json          # Railway auto-deploy settings
```

---

## 🚢 Deploy to Railway

```
1. Fork this repo
2. Go to railway.app → New Project → Deploy from GitHub
3. Select CoderParva/openclaw
4. Add environment variable: SECRET_KEY = your-secret-key
5. Click Generate Domain → Get your live URL ✅
```

---

## 🎯 Why OpenClaw?

The original OpenClaw is powerful but built for developers. Here's what we fixed:

| Problem | Our Solution |
|---|---|
| ❌ Confusing developer UI | ✅ Clean, beautiful dark interface |
| ❌ Hard API key setup | ✅ Simple one-time paste on first open |
| ❌ No multiple chats | ✅ Full chat management with database |
| ❌ Rate limit crashes | ✅ Graceful error messages and retry |
| ❌ No mobile support | ✅ Fully responsive on all screens |
| ❌ Runs only on localhost | ✅ Deployed on live Railway URL |
| ❌ Shows raw technical output | ✅ Clean markdown-formatted responses |
| ❌ Single AI model | ✅ 4 models to choose from |

---

## 🙌 Built For

This project was built as part of the **OpenClaw Normie-Friendly Challenge** — making powerful AI accessible to everyone, not just developers.

---

## 📄 License

MIT License — feel free to use, modify, and distribute.

---

<div align="center">

**Built with ❤️ using Python · Django · Groq**

⭐ **Star this repo if you found it useful!** ⭐

[![GitHub stars](https://img.shields.io/github/stars/CoderParva/openclaw?style=social)](https://github.com/CoderParva/openclaw)

</div>
