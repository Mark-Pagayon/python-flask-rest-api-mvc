from flask import Blueprint, jsonify
from controllers.ActivityLogsController import *

activity_logs_bp = Blueprint("logs", __name__)
activity_logs_bp.route("/activity_logs/user", methods=["GET"])(get_activity_logs)

activity_logs_bp.route('/activity-logs', methods=['GET'])(get_all_logs)
activity_logs_bp.route('/activity-logs', methods=['POST'])(create_activity_log)
activity_logs_bp.route('/activity-logs/<int:id>', methods=['GET'])(get_log)
activity_logs_bp.route('/activity-logs/<int:id>', methods=['PUT'])(update_log)
activity_logs_bp.route('/activity-logs/<int:id>', methods=['DELETE'])(delete_log)

