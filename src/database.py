# database.py

from datetime import datetime
from config import app, db
from models.UserModel import User, Note
from models.ActivityLog import ActivityLog
from werkzeug.security import generate_password_hash


# Sample data for users and their notes
USER_NOTES = [
    {
        "fname": "Fairy",
        "lname": "Tooth",
        "email": "fairytooth@mailinator.com",
        "password": generate_password_hash("123456"),
        "notes": [
            ("I brush my teeth after each meal.", "2022-01-06 17:10:24"),
            ("The other day a friend said, I have big teeth.", "2022-03-05 22:17:54"),
            ("Do you pay per gram?", "2022-03-05 22:18:10"),
        ],
    },
    {
        "fname": "Ruprecht",
        "lname": "Knecht",
        "email": "ruprechtknecht@mailinator.com",
        "password": generate_password_hash("123456"),
        "notes": [
            ("I swear, I'll do better this year.", "2022-01-01 09:15:03"),
            ("Really! Only good deeds from now on!", "2022-02-06 13:09:21"),
        ],
    },
    {
        "fname": "Bunny",
        "lname": "Easte",
        "email": "Bunnyeaste@mailinator.com",
        "password": generate_password_hash("123456"),
        "notes": [
            ("Please keep the current inflation rate in mind!", "2022-01-07 22:47:54"),
            ("No need to hide the eggs this time.", "2022-04-06 13:03:17"),
        ],
    },
]

# SEED THE DATABASE / INITIALIZE THE DATABASE WITH THE SAMPLE DATA

with app.app_context():
    db.drop_all()
    db.create_all()
    
    for data in USER_NOTES:
        new_user = User(
            fname=data.get("fname"),
            lname=data.get("lname"),
            email=data.get("email"),
            password=data.get("password")
        )

        db.session.add(new_user)
        db.session.flush()  # get new_user.id before commit

        # Add activity log for user creation
        db.session.add(ActivityLog(
            user_id=new_user.id,
            action="user_created",
        ))

        for content, timestamp in data.get("notes", []):
            note = Note(
                content=content,
                timestamp=datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S"),
                user_id=new_user.id
            )
            db.session.add(note)

            # Log note creation
            db.session.add(ActivityLog(
                user_id=new_user.id,
                action="create_note",
            ))

    db.session.commit()
