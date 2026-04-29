import streamlit as st
from dotenv import load_dotenv
import uuid
import json
import os
import sys

# 🔥 FIX IMPORT PATH (VERY IMPORTANT)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Load env
load_dotenv(override=True)

# Imports
from backend.controllers.project_controller import handle_user_input
from services.llm_service import llm_service
from core.router import Router


# ── INIT ROUTER ────────────────────────────────
if "router" not in st.session_state:
    st.session_state.router = Router()

router = st.session_state.router


# ── FILE STORAGE ──────────────────────────────
def load_projects():
    if os.path.exists("projects.json"):
        with open("projects.json", "r") as f:
            return json.load(f)
    return {}


def save_projects(data):
    with open("projects.json", "w") as f:
        json.dump(data, f)


# ── AUTO PROJECT NAME ─────────────────────────
def generate_project_name(text):
    words = text.lower().split()
    ignore = ["build", "create", "make", "develop", "a", "an", "the"]
    filtered = [w for w in words if w not in ignore]

    return " ".join(filtered[:3]).title() if filtered else "New Project"


# ── PAGE CONFIG ───────────────────────────────
st.set_page_config(page_title="AI Project Partner", page_icon="⚡")

st.title("⚡ AI Project Partner")
st.caption("Chat-based AI Project Assistant")


# ── SESSION STATE INIT ────────────────────────
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


# ── SIDEBAR ───────────────────────────────────
st.sidebar.title("🧠 Projects")

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

current = st.session_state.current_project
project_data = st.session_state.projects[current]

new_name = st.sidebar.text_input(
    "✏️ Rename Project",
    value=project_data["name"],
    key=f"name_{current}"
)

if new_name != project_data["name"]:
    project_data["name"] = new_name
    save_projects(st.session_state.projects)

st.sidebar.divider()

for pid, pdata in st.session_state.projects.items():
    if st.sidebar.button(pdata["name"], key=pid):
        st.session_state.current_project = pid
        st.rerun()

st.sidebar.divider()

if st.sidebar.button("🗑 Clear Current Chat"):
    project_data["messages"] = []
    project_data["started"] = False
    project_data["name"] = "New Project"
    save_projects(st.session_state.projects)
    st.rerun()


# ── CHAT DISPLAY ──────────────────────────────
messages = project_data["messages"]

for msg in messages:
    with st.chat_message(msg["role"]):

        content = msg["content"]

        if isinstance(content, dict):
            rtype = content.get("type")
            data = content.get("data")

            if rtype == "text":
                st.markdown(data)

            elif rtype == "code":
                st.code(data)

            elif rtype == "image":
                st.image(data)

        else:
            st.markdown(content)


# ── INPUT ─────────────────────────────────────
user_input = st.chat_input("Type your request...")

if user_input:

    # Save user message
    messages.append({"role": "user", "content": user_input})
    save_projects(st.session_state.projects)

    with st.chat_message("user"):
        st.markdown(user_input)

    # 🔥 CODE ROUTER (Gemini)
    is_code = router.is_coding_query(user_input)

    if is_code:
        with st.spinner("Generating code... ⚡"):
            try:
                code_output = router.handle_prompt(user_input)
                response = {"type": "code", "data": code_output}
            except Exception as e:
                response = {"type": "text", "data": f"Error: {str(e)}"}

    else:
        # First message → set project name
        if not project_data["started"]:
            project_data["name"] = generate_project_name(user_input)
            project_data["started"] = True
            save_projects(st.session_state.projects)

        with st.spinner("Thinking... 🤖"):
            try:
                response = handle_user_input(user_input, llm_service)
            except Exception as e:
                response = {"type": "text", "data": f"Error: {str(e)}"}

    # ── DISPLAY RESPONSE ──────────────────────
    with st.chat_message("assistant"):

        if isinstance(response, dict):
            rtype = response.get("type")
            data = response.get("data")

            if rtype == "text":
                st.markdown(data)

            elif rtype == "code":
                st.code(data)

            elif rtype == "image":
                st.image(data)

            else:
                st.markdown("⚠️ Unknown response")

        else:
            st.markdown(response)

    # Save response
    messages.append({"role": "assistant", "content": response})
    save_projects(st.session_state.projects)