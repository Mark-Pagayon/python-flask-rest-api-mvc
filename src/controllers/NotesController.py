# NotesController.py

from flask import abort, make_response, request
from config import db
from models.UserModel import User, Note
from models.schema.NoteSchema import note_schema
from utils.activity_logger import log_activity

# Create Note
def create():
    data = request.get_json()
    
    user_id = data.get("user_id")
    user = User.query.get(user_id)

    if user:
        new_note = note_schema.load(data, session=db.session)
        user.notes.append(new_note)
        db.session.commit()

        log_activity(user_id, "note_created")

        return note_schema.dump(new_note), 201
    else:
        abort(
            404,
            f"User not found for user ID: {user_id}"
        )

# Read Note       
def read_one(note_id):
    note = Note.query.get(note_id)
    if note is not None:
        return note_schema.dump(note)
    else:
        abort(
            404, f"Note with ID {note_id} not found"
        )

# Update Note
def update(note_id):

    data = request.get_json()

    note = data

    existing_note = Note.query.get(note_id)
    if existing_note:
        existing_note.content = note["content"]
        db.session.merge(existing_note)
        db.session.commit()

        log_activity(existing_note.user_id, "note_updated")

        return note_schema.dump(existing_note), 201
    else:
        abort(404, f"Note with ID {note_id} not found")

# Delete Note
def delete(note_id):
    existing_note = Note.query.get(note_id)
    if existing_note:
        db.session.delete(existing_note)
        db.session.commit()

        log_activity(existing_note.user_id, "note_deleted")

        return make_response(f"{note_id} successfully deleted", 204)
    else:
        abort(404, f"Note with ID {note_id} not found")