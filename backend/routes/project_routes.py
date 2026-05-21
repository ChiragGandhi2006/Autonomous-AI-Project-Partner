from flask import Blueprint, request, jsonify
from backend.controllers.project_controller import start_project
from core.orchestrator import Orchestrator

orchestrator = Orchestrator()


project_routes = Blueprint("project_routes", __name__)


@project_routes.route("/project/continue", methods=["POST"])
def continue_project():
    data = request.get_json()
    action = data.get("action")

    response = orchestrator.handle_action(action)
    return jsonify({"response": response})

