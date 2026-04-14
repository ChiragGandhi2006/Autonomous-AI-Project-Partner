import streamlit as st
from dotenv import load_dotenv
import uuid
import json
import os

# Load env
load_dotenv(override=True)

# Backend (existing)
from backend.controllers.project_controller import start_project, continue_project

# 🔥 NEW: Router (Hybrid AI)
from core.router import Router


# ── INIT ROUTER (ONLY ONCE) ────────────────────────────────
if "router" not in st.session_state:
    st.session_state.router = Router()

router = st.session_state.router


# ── FILE STORAGE FUNCTIONS ─────────────────────────────────
def load_projects():
    if os.path.exists("projects.json"):
        with open("projects.json", "r") as f:
            return json.load(f)
    return {}


def save_projects(data):
    with open("projects.json", "w") as f:
        json.dump(data, f)


# ── AUTO PROJECT NAME FUNCTION ─────────────────────────────
def generate_project_name(text):
    words = text.lower().split()

    ignore = ["build", "create", "make", "develop", "a", "an", "the"]

    filtered = [w for w in words if w not in ignore]

    if not filtered:
        return "New Project"

    return " ".join(filtered[:3]).title()


# ── Page config ─────────────────────────────────────────────
st.set_page_config(page_title="AI Project Partner", page_icon="⚡")

st.title("⚡ AI Project Partner")
st.caption("Chat-based AI Project Assistant")


# ── SESSION STATE INIT ──────────────────────────────────────
if "projects" not in st.session_state:
    st.session_state.projects = load_projects()

if "current_project" not in st.session_state or not st.session_state.projects:
    pid = str(uuid.uuid4())
    st.session_state.current_project = pid
    st.session_state.projects[pid] = {
        "name": "New Project",
        "messages": [],
        "started": False
    }
    save_projects(st.session_state.projects)


# ── SIDEBAR ────────────────────────────────────────────────
st.sidebar.title("🧠 Projects")

# ➕ New Project
if st.sidebar.button("➕ New Project"):
    pid = str(uuid.uuid4())
    st.session_state.current_project = pid
    st.session_state.projects[pid] = {
        "name": "New Project",
        "messages": [],
        "started": False
    }
    save_projects(st.session_state.projects)
    st.rerun()

# Current project
current = st.session_state.current_project
project_data = st.session_state.projects[current]

# ✏️ Rename Project
new_name = st.sidebar.text_input(
    "✏️ Rename Project",
    value=project_data["name"],
    key=f"name_{current}"
)

if new_name != project_data["name"]:
    project_data["name"] = new_name
    save_projects(st.session_state.projects)

st.sidebar.divider()

# 📂 Project List
for pid, pdata in st.session_state.projects.items():
    if st.sidebar.button(pdata["name"], key=pid):
        st.session_state.current_project = pid
        st.rerun()

st.sidebar.divider()

# 🗑 Clear Current Chat
if st.sidebar.button("🗑 Clear Current Chat"):
    project_data["messages"] = []
    project_data["started"] = False
    project_data["name"] = "New Project"
    save_projects(st.session_state.projects)
    st.rerun()


# ── CURRENT CHAT ───────────────────────────────────────────
messages = project_data["messages"]


# ── DISPLAY CHAT ───────────────────────────────────────────
for msg in messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# ── CHAT INPUT ─────────────────────────────────────────────
user_input = st.chat_input("Type your request...")

if user_input:

    # Save user message
    messages.append({
        "role": "user",
        "content": user_input
    })
    save_projects(st.session_state.projects)

    with st.chat_message("user"):
        st.markdown(user_input)

    # 🔥 NEW: Detect coding query
    is_code = router.is_coding_query(user_input)

    # FIRST MESSAGE → START PROJECT (only if NOT coding)
    if not project_data["started"] and not is_code:

        project_data["name"] = generate_project_name(user_input)
        save_projects(st.session_state.projects)

        with st.chat_message("assistant"):
            with st.spinner("Starting project..."):
                try:
                    result = start_project(user_input)
                except Exception as e:
                    result = {"error": str(e)}

            response_text = ""

            if isinstance(result, dict):
                for key, value in result.items():
                    response_text += f"### {key.capitalize()}\n{value}\n\n"
            else:
                response_text = str(result)

            st.markdown(response_text)

        messages.append({
            "role": "assistant",
            "content": response_text
        })
        save_projects(st.session_state.projects)

        project_data["started"] = True

    # 🔥 CODING QUERY → BYPASS PROJECT SYSTEM
    elif is_code:

        with st.chat_message("assistant"):
            with st.spinner("Generating code... ⚡"):
                try:
                    response_text = router.handle_prompt(user_input)
                except Exception as e:
                    response_text = f"Error: {str(e)}"

            st.markdown(response_text)

        messages.append({
            "role": "assistant",
            "content": response_text
        })
        save_projects(st.session_state.projects)

    # NORMAL CONTINUE PROJECT
    else:

        with st.chat_message("assistant"):
            with st.spinner("Running agents..."):
                try:
                    result = continue_project(user_input)
                except Exception as e:
                    result = {"error": str(e)}

            response_text = ""

            if isinstance(result, dict):
                for key, value in result.items():
                    response_text += f"### {key.capitalize()}\n{value}\n\n"
            else:
                response_text = str(result)

            st.markdown(response_text)

        messages.append({
            "role": "assistant",
            "content": response_text
        })
        save_projects(st.session_state.projects)