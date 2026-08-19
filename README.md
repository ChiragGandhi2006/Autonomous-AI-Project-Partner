# 🚀 AI Project Partner

An intelligent, chat-based AI system that helps you **plan, build, and visualize projects** using Gemini for reasoning + code and OpenAI / pollinations for images.

---

## 🔥 Features

- 🧠 **AI Reasoning (Gemini API)** — plans, ideas, workflows, debugging
- 💻 **Code Generation (Gemini API)** — writes clean, structured code
- 📝 **Code Explanation (Gemini API)** — line-by-line explanation of generated code
- 🎨 **Image Generation** — OpenAI (`gpt-image-1`) with free **pollinations.ai** fallback (no API key needed)
- 🔍 **Multimedia Analysis** — upload images / PDFs / code files and get solutions or explanations
- 💬 **Chat-based Interface** — interactive UI like ChatGPT
- 📁 **Project Management** — create, rename, switch between multiple projects
- ☁️ **Streamlit Cloud ready** — 100% API-based, no local ML models

---

## 🧠 Architecture

```
User Input
    ↓
Project Controller
    ↓
Decision Layer
├── Code        → Gemini API (coding_service)
├── Explanation → Gemini API (llm_service)
├── Image       → OpenAI gpt-image-1 → pollinations.ai (free fallback)
├── Files       → Gemini API (media_analysis_service)
└── Chat / Plan → Gemini API (llm_service)
```

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **Backend:** Python
- **LLM / Code / Media:** Google Gemini (`gemini-3-flash-preview`)
- **Image Generation:** OpenAI `gpt-image-1` → pollinations.ai fallback

> No `torch` / `transformers` / `diffusers` — everything is API-based so it runs on the free Streamlit Cloud tier.

---

## 📂 Project Structure

```
├── agents/                  # Agent definitions (ideation, planning, coder, ...)
├── backend/controllers/     # project_controller.py
├── config/                  # settings / constants
├── core/                    # router.py, orchestrator.py
├── frontend/
│   └── app.py               # Streamlit entry point
├── memory/                  # short/long term memory managers
├── models/                  # intent / project type detectors
├── services/
│   ├── llm_service.py       # Gemini chat/reasoning
│   ├── coding_service.py    # Gemini code generation
│   ├── media_analysis_service.py
│   └── image_service.py     # OpenAI + pollinations fallback
├── .streamlit/
│   ├── config.toml
│   └── secrets.toml         # OPTIONAL local template (gitignored)
├── requirements.txt
└── projects.json            # stored chat projects
```

---

## ⚙️ Setup & Local Run

### 1️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 2️⃣ Set environment variables

Create a `.env` file in the project root:

```ini
GEMINI_API_KEY=your_gemini_key
OPENAI_API_KEY=your_openai_key     # optional — free pollinations fallback if missing
```

⚠️ Never upload `.env` to GitHub (already in `.gitignore`).

### 3️⃣ Run locally

```bash
streamlit run frontend/app.py
```

---

## ☁️ Deploy to Streamlit Community Cloud

1. Push this repo to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**.
3. Pick the repo and set **Main file path** to `frontend/app.py`.
4. In **Advanced Settings → Secrets**, add:

```toml
GEMINI_API_KEY = "your_gemini_key"
OPENAI_API_KEY = "your_openai_key"
```

5. Click **Deploy**. Done 🎉

> Tip: `projects.json` stores chat history. On Cloud it's per-user/ephemeral, which is fine for demos. Local runs reuse it.