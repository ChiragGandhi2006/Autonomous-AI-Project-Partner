# 🚀 AI Project Partner

An intelligent, chat-based AI system that helps you **plan, build, and visualize projects** using multiple AI models.

---

## 🔥 Features

- 🧠 **Project Planning (LLM)**
  - Generates idea, step-by-step plan, and workflow
- 💻 **Code Generation (Gemini API)**
  - Writes clean and structured code
- 🎨 **Image Generation (OpenAI)**
  - Converts text prompts into images
- 🔁 **Free Fallback (Stable Diffusion)**
  - Automatically switches to free model if OpenAI fails
- 💬 **Chat-based Interface**
  - Interactive UI like ChatGPT
- 📁 **Project Management**
  - Create, rename, and manage multiple projects

---

## 🧠 Architecture
User Input
↓
Project Controller
↓
Decision Layer
├── Code → Gemini API
├── Image → OpenAI / Stable Diffusion
└── Chat / Plan → LLM


---

## 🛠️ Tech Stack

- **Frontend:** Streamlit  
- **Backend:** Python  
- **LLM:** Custom LLM / HuggingFace  
- **Code Generation:** Gemini API  
- **Image Generation:** OpenAI (`gpt-image-1`)  
- **Fallback Model:** Stable Diffusion (Diffusers)  

---

## 📂 Project Structure
project/
│
├── backend/
│ └── controllers/
│ └── project_controller.py
│
├── services/
│ ├── llm_service.py
│ ├── image_service.py
│ ├── code_generation_service.py
│
├── core/
│ ├── router.py
│ ├── orchestrator.py
│
├── frontend/
│ └── app.py
│
├── projects.json
├── .env
├── requirements.txt


---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

pip install -r requirements.txt

2️⃣ Install dependencies
pip install -r requirements.txt
3️⃣ Setup environment variables

Create a .env file in root directory:

OPENAI_API_KEY=your_openai_key
GEMINI_API_KEY=your_gemini_key

⚠️ Important: Never upload .env file to GitHub

4️⃣ Run the application
streamlit run frontend/app.py
