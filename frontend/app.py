import warnings
import logging
import json
import os
import re
import sys
import uuid
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

# ---------------- WARNING SUPPRESSION ----------------
warnings.filterwarnings("ignore")

logging.getLogger(
    "transformers"
).setLevel(logging.ERROR)

logging.getLogger(
    "PIL"
).setLevel(logging.ERROR)

os.environ[
    "TRANSFORMERS_NO_ADVISORY_WARNINGS"
] = "1"

os.environ[
    "TOKENIZERS_PARALLELISM"
] = "false"

os.environ[
    "TF_CPP_MIN_LOG_LEVEL"
] = "3"


# ---------------- PATH SETUP ----------------
sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

load_dotenv(override=True)

from backend.controllers.project_controller import handle_user_input
from core.router import Router
from services.llm_service import llm_service
from services.media_analysis_service import MediaAnalysisService


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Project Partner",
    page_icon="⚡",
    layout="wide"
)


# ---------------- SESSION ----------------
if "router" not in st.session_state:
    st.session_state.router = Router()

if "media_analyzer" not in st.session_state:
    st.session_state.media_analyzer = MediaAnalysisService()

router = st.session_state.router
media_analyzer = st.session_state.media_analyzer


# ---------------- PROJECT STORAGE ----------------
def load_projects():

    if os.path.exists("projects.json"):

        try:
            with open(
                "projects.json",
                "r",
                encoding="utf-8"
            ) as f:

                return json.load(f)

        except Exception:
            return {}

    return {}


def save_projects(data):

    with open(
        "projects.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=4
        )


# ---------------- PROJECT NAME ----------------
def generate_project_name(text):

    words = text.lower().split()

    ignore = [
        "build",
        "create",
        "make",
        "develop",
        "a",
        "an",
        "the"
    ]

    filtered = [
        word for word in words
        if word not in ignore
    ]

    return (
        " ".join(filtered[:3]).title()
        if filtered
        else "New Project"
    )


# ---------------- LAST CODE ----------------
def get_last_code_message(messages):

    for msg in reversed(messages):

        content = msg.get("content")

        if (
            isinstance(content, dict)
            and content.get("type") == "code"
        ):
            return content.get("data")

    return None


# ---------------- CHAT INPUT ----------------
def get_chat_text_and_files(chat_value):

    if isinstance(chat_value, str):
        return chat_value, []

    text = getattr(
        chat_value,
        "text",
        ""
    ) or ""

    files = getattr(
        chat_value,
        "files",
        []
    ) or []

    return text, files


# ---------------- SAVE FILES ----------------
def save_uploaded_files(
    uploaded_files,
    project_id
):

    upload_dir = (
        Path("uploads")
        / project_id
    )

    upload_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    saved_files = []

    for uploaded_file in uploaded_files:

        safe_name = (
            Path(uploaded_file.name)
            .name
        )

        file_path = (
            upload_dir /
            f"{uuid.uuid4().hex}_{safe_name}"
        )

        file_path.write_bytes(
            uploaded_file.getvalue()
        )

        saved_files.append({
            "name": safe_name,
            "path": str(file_path),
            "mime_type": uploaded_file.type,
        })

    return saved_files


# ---------------- STRUCTURE DETECTION ----------------
def contains_structure(text):

    structure_patterns = [
        "├──",
        "└──",
        "│",
        "src/",
        ".py",
        ".js",
        ".html",
        ".css",
        ".json",
        ".env"
    ]

    return any(
        pattern in text
        for pattern in structure_patterns
    )


# ---------------- CODE DETECTION ----------------
def contains_code(text):

    code_patterns = [
        "def ",
        "class ",
        "import ",
        "from ",
        "{",
        "}",
        "();",
        "return ",
        "if __name__"
    ]

    return any(
        pattern in text
        for pattern in code_patterns
    )


# ---------------- CLEAN RESPONSE ----------------
def clean_response(text):

    if not isinstance(text, str):
        return text

    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text
    )

    return text.strip()


# ---------------- RENDER CONTENT ----------------
def render_message_content(content):

    if not isinstance(content, dict):
        st.markdown(content)
        return

    rtype = content.get("type")
    data = content.get("data")

    if isinstance(data, str):
        data = clean_response(data)

    # TEXT
    if rtype == "text":

        if isinstance(data, str):

            # ASCII STRUCTURES
            if contains_structure(data):

                st.code(
                    data,
                    language=None
                )

            # CODE
            elif contains_code(data):

                st.code(
                    data,
                    language="python"
                )

            else:
                st.markdown(data)

        else:
            st.markdown(str(data))

    # CODE
    elif rtype == "code":

        st.code(
            data,
            language="python"
        )

    # IMAGE
    elif rtype == "image":

        if data and os.path.exists(data):

            try:
                st.image(
                    data,
                    use_container_width=True
                )

            except Exception:
                st.warning(
                    "Could not display image."
                )

        else:
            st.warning(
                "Generated image file missing."
            )

    # USER MEDIA
    elif rtype == "user_media":

        text = content.get("text")
        files = content.get("files", [])

        if text:
            st.markdown(text)

        for file_info in files:

            mime_type = (
                file_info.get("mime_type")
                or ""
            )

            # IMAGE FILES
            if mime_type.startswith("image/"):

                image_path = file_info.get(
                    "path",
                    ""
                )

                if (
                    image_path
                    and os.path.exists(
                        image_path
                    )
                ):

                    try:
                        st.image(
                            image_path,
                            caption=file_info["name"],
                            use_container_width=True
                        )

                    except Exception:
                        st.warning(
                            f"Could not display image: {file_info['name']}"
                        )

                else:
                    st.warning(
                        f"Image file missing: {file_info['name']}"
                    )

            # OTHER FILES
            else:
                st.markdown(
                    f"📎 Attached file: `{file_info['name']}`"
                )

    else:
        st.markdown("Unknown response")


# ---------------- TEXT RESPONSE ----------------
def answer_text_message(
    user_input,
    messages,
    project_data
):

    is_code = router.is_coding_query(
        user_input
    )

    is_code_explanation = (
        router.is_code_explanation_query(
            user_input
        )
    )

    # ==================================================
    # CODE GENERATION
    # LOCAL ROUTER
    # ==================================================
    if is_code and not is_code_explanation:

        with st.spinner("Generating code..."):

            generation_prompt = f"""
You are an expert software engineer.

Generate production-ready code.

IMPORTANT RULES:
- Generate scalable architecture
- Generate modular code
- Preserve indentation
- Preserve formatting
- Use clean coding standards
- Use modern best practices
- Generate optimized solutions
- Add comments where necessary

ASCII STRUCTURE RULES:
- Generate clean multiline ASCII trees
- Preserve hierarchy properly
- Generate dynamic structures
- DO NOT force fixed templates

User Request:

{user_input}
"""

            code_output = router.handle_prompt(
                generation_prompt
            )

            return {
                "type": "code",
                "data": code_output
            }

    # ==================================================
    # CODE EXPLANATION
    # GEMINI API
    # ==================================================
    elif is_code_explanation:

        with st.spinner("Explaining code..."):

            code_context = (
                get_last_code_message(messages)
            )

            explanation_prompt = f"""
You are a senior software engineer.

Explain the following code professionally.

IMPORTANT RULES:
- Preserve indentation exactly
- Preserve formatting exactly
- Preserve spacing
- Explain line by line
- Explain functions clearly
- Explain modules properly
- Preserve ASCII structures naturally

Code Context:

{code_context}

User Request:

{user_input}
"""

            explanation = (
                llm_service.generate_response(
                    explanation_prompt
                )
            )

            return {
                "type": "text",
                "data": explanation
            }

    # ==================================================
    # GENERAL AI REASONING
    # GEMINI API
    # ==================================================
    else:

        if not project_data["started"]:

            project_data["name"] = (
                generate_project_name(
                    user_input
                )
            )

            project_data["started"] = True

            save_projects(
                st.session_state.projects
            )

        with st.spinner("Thinking..."):

            reasoning_prompt = f"""
You are an intelligent AI project partner.

Provide:
- professional reasoning
- scalable architecture suggestions
- optimized workflows
- software engineering guidance
- modern development practices

IMPORTANT:
- Preserve formatting
- Generate dynamic architectures
- Use professional ASCII structures
- Preserve hierarchy naturally

User Request:

{user_input}
"""

            response = (
                llm_service.generate_response(
                    reasoning_prompt
                )
            )

            return {
                "type": "text",
                "data": response
            }


# ---------------- UI ----------------
st.title("⚡ AI Project Partner")

st.caption(
    "Code • Debug • Explain • Multimedia Analysis"
)


# ---------------- PROJECT INIT ----------------
if "projects" not in st.session_state:
    st.session_state.projects = load_projects()

if (
    "current_project"
    not in st.session_state
    or not st.session_state.projects
):

    pid = str(uuid.uuid4())

    st.session_state.current_project = pid

    st.session_state.projects[pid] = {
        "name": "New Project",
        "messages": [],
        "started": False,
    }

    save_projects(
        st.session_state.projects
    )


# ---------------- SIDEBAR ----------------
st.sidebar.title("Projects")


# NEW PROJECT
if st.sidebar.button("➕ New Project"):

    pid = str(uuid.uuid4())

    st.session_state.current_project = pid

    st.session_state.projects[pid] = {
        "name": "New Project",
        "messages": [],
        "started": False,
    }

    save_projects(
        st.session_state.projects
    )

    st.rerun()


current = st.session_state.current_project
project_data = st.session_state.projects[current]


# RENAME PROJECT
new_name = st.sidebar.text_input(
    "Rename Project",
    value=project_data["name"],
    key=f"name_{current}",
)

if new_name != project_data["name"]:

    project_data["name"] = new_name

    save_projects(
        st.session_state.projects
    )


st.sidebar.divider()


# SWITCH PROJECTS
for pid, pdata in st.session_state.projects.items():

    if st.sidebar.button(
        pdata["name"],
        key=pid
    ):
        st.session_state.current_project = pid
        st.rerun()


st.sidebar.divider()


# CLEAR CHAT
if st.sidebar.button(
    "🗑 Clear Current Chat"
):

    project_data["messages"] = []

    project_data["started"] = False

    project_data["name"] = "New Project"

    save_projects(
        st.session_state.projects
    )

    st.rerun()


# ---------------- CHAT HISTORY ----------------
messages = project_data["messages"]

for msg in messages:

    with st.chat_message(msg["role"]):

        render_message_content(
            msg["content"]
        )


# ---------------- CHAT INPUT ----------------
chat_value = st.chat_input(
    "Type your request...",
    accept_file="multiple",
    file_type=[
        "png", "jpg", "jpeg",
        "webp", "gif", "bmp",
        "pdf", "txt", "md",
        "csv", "json", "xml",
        "yaml", "yml",
        "py", "js", "ts",
        "html", "css", "java",
        "cpp", "c", "h",
        "hpp", "cs", "php",
        "rb", "go", "rs",
        "sql", "log",
    ],
)


if chat_value:

    user_input, uploaded_files = (
        get_chat_text_and_files(
            chat_value
        )
    )

    saved_files = save_uploaded_files(
        uploaded_files,
        current
    )

    user_content = (
        {
            "type": "user_media",
            "text": user_input,
            "files": saved_files
        }
        if saved_files
        else user_input
    )

    messages.append({
        "role": "user",
        "content": user_content
    })

    save_projects(
        st.session_state.projects
    )

    with st.chat_message("user"):

        render_message_content(
            user_content
        )

    try:

        # FILE ANALYSIS
        if saved_files:

            if not project_data["started"]:

                project_data["name"] = (
                    generate_project_name(
                        user_input
                        or saved_files[0]["name"]
                    )
                )

                project_data["started"] = True

                save_projects(
                    st.session_state.projects
                )

            with st.spinner(
                "Analyzing attachment..."
            ):

                extracted_content = (
                    media_analyzer.analyze(
                        user_input,
                        saved_files
                    )
                )

                explanation_prompt = f"""
You are a senior software engineer and software architect.

Analyze the uploaded content intelligently.

IMPORTANT RULES:
- Preserve indentation exactly
- Preserve spacing exactly
- Preserve hierarchy naturally
- Preserve formatting
- Explain professionally
- Generate clean ASCII structures

Uploaded Content:

{extracted_content}
"""

                media_output = (
                    llm_service.generate_response(
                        explanation_prompt
                    )
                )

                response = {
                    "type": "text",
                    "data": media_output
                }

        # NORMAL CHAT
        else:

            response = answer_text_message(
                user_input,
                messages,
                project_data
            )

    except Exception as e:

        response = {
            "type": "text",
            "data": f"Error: {str(e)}"
        }

    with st.chat_message("assistant"):

        render_message_content(
            response
        )

    messages.append({
        "role": "assistant",
        "content": response
    })

    save_projects(
        st.session_state.projects
    )