from flask import Blueprint, request, jsonify
from backend.controllers.agent_controller import run_agents


agent_routes = Blueprint("agent_routes", __name__)


@agent_routes.route("/run-agents", methods=["POST"])
def run_agents_route():
    data = request.get_json()
    return jsonify(run_agents(data))
