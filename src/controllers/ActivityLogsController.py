from flask import jsonify, request, abort
from config import db
from flask_jwt_extended import get_jwt_identity
from models.ActivityLog import ActivityLog
from flask_jwt_extended import jwt_required, get_jwt_identity


def get_logs_for_user(user_id):
    logs = ActivityLog.query.filter_by(user_id=user_id).order_by(ActivityLog.timestamp.desc()).all()
    return [{
        "action": log.action,
        "timestamp": log.timestamp.isoformat()
    } for log in logs], 200

@jwt_required()
def get_activity_logs():
    user_id = get_jwt_identity()
    logs = get_logs_for_user(user_id)
    return jsonify(logs), 200



def create_activity_log():
    data = request.get_json()
    user_id = data.get('user_id')
    action = data.get('action')

    if not user_id or not action:
        abort(400, 'Missing required fields.')

    log = ActivityLog(user_id=user_id, action=action)
    db.session.add(log)
    db.session.commit()

    return jsonify({'message': 'Activity log created', 'id': log.id}), 201


def get_all_logs():
    logs = ActivityLog.query.all()
    return jsonify([
        {
            'id': log.id,
            'user_id': log.user_id,
            'action': log.action,
            'timestamp': log.timestamp.isoformat()
        } for log in logs
    ]), 200


def get_log(id):
    log = ActivityLog.query.get_or_404(id)
    return jsonify({
        'id': log.id,
        'user_id': log.user_id,
        'action': log.action,
        'timestamp': log.timestamp.isoformat()
    }), 200


def update_log(id):
    log = ActivityLog.query.get_or_404(id)
    data = request.get_json()

    if not data or 'action' not in data:
        return jsonify({'error': 'No update data provided'}), 400

    log.action = data.get('action', log.action)
    db.session.commit()

    return jsonify({'message': 'Activity log updated'}), 200


def delete_log(id):
    log = ActivityLog.query.get_or_404(id)
    db.session.delete(log)
    db.session.commit()

    return jsonify({'message': 'Log deleted successfully'}), 200
