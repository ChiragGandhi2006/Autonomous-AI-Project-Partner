import os
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

# --------------------------------
# LOAD ENV VARIABLES
# --------------------------------
load_dotenv(override=True)
print("🔥 ENV CHECK:", os.getenv("GEMINI_API_KEY"))

# --------------------------------
# IMPORT CONTROLLERS
# --------------------------------
from backend.controllers.project_controller import (
    start_project,
    continue_project
)

# --------------------------------
# FLASK CONFIG
# --------------------------------
app = Flask(
    __name__,
    template_folder="frontend/templates",
    static_folder="frontend/static"
)

# --------------------------------
# HOME
# --------------------------------
@app.route("/")
def home():
    return render_template("index.html")

# --------------------------------
# START PROJECT
# --------------------------------
@app.route("/project/start-project", methods=["POST"])
def start_project_route():
    data = request.get_json()
    project_goal = data.get("project_goal")

    if not project_goal:
        return jsonify({"error": "Project goal required"}), 400

    response = start_project(project_goal)
    return jsonify(response)

# --------------------------------
# CONTINUE PROJECT (OPTIONS)
# --------------------------------
@app.route("/project/continue-project", methods=["POST"])
def continue_project_route():
    data = request.get_json()
    action = data.get("action")

    if not action:
        return jsonify({"error": "Action is required"}), 400

    response = continue_project(action)
    return jsonify(response)

# --------------------------------
# RUN SERVER
# --------------------------------
if __name__ == "__main__":
    app.run(debug=True)
