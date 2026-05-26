from flask import Flask, render_template
from config import Config
from models.user_model import db, User
from models.event_model import Event
from routes.auth_routes import auth
from flask_login import LoginManager
from routes.admin_routes import admin
from routes.organizer_routes import organizer
from routes.user_routes import user
from models.participation_model import Participation
from models.rating_model import Rating
from models.complaint_model import Complaint
from models.expense_model import Expense
from models.performer_model import Performer
from models.notification_model import Notification
from models.event_category_model import EventCategory
from models.team_model import Team
from models.schedule_model import Schedule

app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
db.init_app(app)

# Flask Login Manager
login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = "auth.login"

# Register blueprint
app.register_blueprint(auth)
app.register_blueprint(admin)
app.register_blueprint(organizer)
app.register_blueprint(user)


# Load logged-in user
@login_manager.user_loader
def load_user(user_id):

    return User.query.get(int(user_id))


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(host="0.0.0.0", port=5000, debug=True)
