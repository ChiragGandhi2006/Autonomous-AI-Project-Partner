import json
import os
import sys
import uuid
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

load_dotenv(override=True)

from backend.controllers.project_controller import handle_user_input
from core.router import Router
from services.llm_service import llm_service
from services.media_analysis_service import MediaAnalysisService


st.set_page_config(page_title="AI Project Partner", page_icon="⚡")

if "router" not in st.session_state:
    st.session_state.router = Router()

if "media_analyzer" not in st.session_state:
    st.session_state.media_analyzer = MediaAnalysisService()

router = st.session_state.router
media_analyzer = st.session_state.media_analyzer


def load_projects():
    if os.path.exists("projects.json"):
        with open("projects.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_projects(data):
    with open("projects.json", "w", encoding="utf-8") as f:
        json.dump(data, f)


def generate_project_name(text):
    words = text.lower().split()
    ignore = ["build", "create", "make", "develop", "a", "an", "the"]
    filtered = [word for word in words if word not in ignore]

    return " ".join(filtered[:3]).title() if filtered else "New Project"


def get_last_code_message(messages):
    for msg in reversed(messages):
        content = msg.get("content")
        if isinstance(content, dict) and content.get("type") == "code":
            return content.get("data")
    return None


def get_chat_text_and_files(chat_value):
    if isinstance(chat_value, str):
        return chat_value, []

    text = getattr(chat_value, "text", "") or ""
    files = getattr(chat_value, "files", []) or []
    return text, files


def save_uploaded_files(uploaded_files, project_id):
    upload_dir = Path("uploads") / project_id
    upload_dir.mkdir(parents=True, exist_ok=True)

    saved_files = []
    for uploaded_file in uploaded_files:
        safe_name = Path(uploaded_file.name).name
        file_path = upload_dir / f"{uuid.uuid4().hex}_{safe_name}"
        file_path.write_bytes(uploaded_file.getvalue())

        saved_files.append({
            "name": safe_name,
            "path": str(file_path),
            "mime_type": uploaded_file.type,
        })

    return saved_files


def render_message_content(content):
    if not isinstance(content, dict):
        st.markdown(content)
        return

    rtype = content.get("type")
    data = content.get("data")

    if rtype == "text":
        st.markdown(data)
    elif rtype == "code":
        st.code(data)
    elif rtype == "image":
        st.image(data)
    elif rtype == "user_media":
        text = content.get("text")
        files = content.get("files", [])

        if text:
            st.markdown(text)

        for file_info in files:
            mime_type = file_info.get("mime_type") or ""
            if mime_type.startswith("image/"):
                st.image(file_info["path"], caption=file_info["name"])
            else:
                st.markdown(f"Attached file: `{file_info['name']}`")
    else:
        st.markdown("Unknown response")


def answer_text_message(user_input, messages, project_data):
    is_code = router.is_coding_query(user_input)
    is_code_explanation = router.is_code_explanation_query(user_input)

    if is_code:
        spinner_text = "Explaining code..." if is_code_explanation else "Generating code..."

        with st.spinner(spinner_text):
            code_context = get_last_code_message(messages) if is_code_explanation else None
            code_output = router.handle_prompt(user_input, code_context)
            response_type = "text" if is_code_explanation else "code"
            return {"type": response_type, "data": code_output}

    if not project_data["started"]:
        project_data["name"] = generate_project_name(user_input)
        project_data["started"] = True
        save_projects(st.session_state.projects)

    with st.spinner("Thinking..."):
        return handle_user_input(user_input, llm_service)


st.title("⚡ AI Project Partner")
st.caption("Chat-based AI Project Assistant")


if "projects" not in st.session_state:
    st.session_state.projects = load_projects()

if "current_project" not in st.session_state or not st.session_state.projects:
    pid = str(uuid.uuid4())
    st.session_state.current_project = pid
    st.session_state.projects[pid] = {
        "name": "New Project",
        "messages": [],
        "started": False,
    }
    save_projects(st.session_state.projects)


st.sidebar.title("Projects")

if st.sidebar.button("New Project"):
    pid = str(uuid.uuid4())
    st.session_state.current_project = pid
    st.session_state.projects[pid] = {
        "name": "New Project",
        "messages": [],
        "started": False,
    }
    save_projects(st.session_state.projects)
    st.rerun()

current = st.session_state.current_project
project_data = st.session_state.projects[current]

new_name = st.sidebar.text_input(
    "Rename Project",
    value=project_data["name"],
    key=f"name_{current}",
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

if st.sidebar.button("Clear Current Chat"):
    project_data["messages"] = []
    project_data["started"] = False
    project_data["name"] = "New Project"
    save_projects(st.session_state.projects)
    st.rerun()


messages = project_data["messages"]

for msg in messages:
    with st.chat_message(msg["role"]):
        render_message_content(msg["content"])


chat_value = st.chat_input(
    "Type your request...",
    accept_file="multiple",
    file_type=[
        "png", "jpg", "jpeg", "webp", "gif", "bmp",
        "pdf", "txt", "md", "csv", "json", "xml", "yaml", "yml",
        "py", "js", "ts", "html", "css", "java", "cpp", "c",
        "h", "hpp", "cs", "php", "rb", "go", "rs", "sql", "log",
    ],
)

if chat_value:
    user_input, uploaded_files = get_chat_text_and_files(chat_value)
    saved_files = save_uploaded_files(uploaded_files, current)

    user_content = (
        {"type": "user_media", "text": user_input, "files": saved_files}
        if saved_files
        else user_input
    )
    messages.append({"role": "user", "content": user_content})
    save_projects(st.session_state.projects)

    with st.chat_message("user"):
        render_message_content(user_content)

    try:
        if saved_files:
            if not project_data["started"]:
                project_data["name"] = generate_project_name(user_input or saved_files[0]["name"])
                project_data["started"] = True
                save_projects(st.session_state.projects)

            with st.spinner("Analyzing attachment..."):
                media_output = media_analyzer.analyze(user_input, saved_files)
                response = {"type": "text", "data": media_output}
        else:
            response = answer_text_message(user_input, messages, project_data)
    except Exception as e:
        response = {"type": "text", "data": f"Error: {str(e)}"}

    with st.chat_message("assistant"):
        render_message_content(response)

    messages.append({"role": "assistant", "content": response})
    save_projects(st.session_state.projects)
