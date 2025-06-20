# app.py

from flask import render_template
import config
from config import app, db
from models.UserModel import User

from routes.notes_bp import notes_bp
from routes.users_bp import users_bp
from routes.auth_bp import auth_bp
from routes.activity_log_bp import activity_logs_bp

# REGISTER ROUTES WITH BLUEPRINTS
app.register_blueprint(users_bp, url_prefix='/users')
app.register_blueprint(notes_bp, url_prefix='/notes')
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(activity_logs_bp, url_prefix='/activity-logs')

app = config.connex_app
# Create database schema
# with app.app_context():
#     db.drop_all()
#     db.create_all()

# LOAD SWAGGER DOCUMENTATION
app.add_api(config.basedir / "swagger.json")


# HOME ROUTE
@app.route("/")
def home():
    users = User.query.all()
    return render_template("home.html", users=users)


if __name__ == "__main__":
    config.connex_app.run(host="0.0.0.0", port=8000)