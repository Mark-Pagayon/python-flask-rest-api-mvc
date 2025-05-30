from flask import Blueprint, jsonify
from controllers.ActivityLogsController import *

activity_logs_bp = Blueprint("activity_log_bp", __name__)
activity_logs_bp.route("/user", methods=["GET"])(get_activity_logs)

activity_logs_bp.route('/', methods=['GET'])(get_all_logs)
activity_logs_bp.route('/', methods=['POST'])(create_activity_log)
activity_logs_bp.route('/<int:id>', methods=['GET'])(get_log)
activity_logs_bp.route('/<int:id>', methods=['PUT'])(update_log)
activity_logs_bp.route('/<int:id>', methods=['DELETE'])(delete_log)

