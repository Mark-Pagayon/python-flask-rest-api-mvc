
from models.ActivityLog import ActivityLog
from config import db

def log_activity(user_id, action):
    log = ActivityLog(user_id=user_id, action=action)
    db.session.add(log)
    db.session.commit()
