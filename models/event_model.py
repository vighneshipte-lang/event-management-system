from models.user_model import db


class Event(db.Model):

    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200), nullable=False)

    description = db.Column(db.Text, nullable=False)

    event_type = db.Column(db.String(20), nullable=False)

    categories = db.relationship("EventCategory", backref="event", lazy=True)

    venue = db.Column(db.String(200), nullable=False)

    start_date = db.Column(db.Date, nullable=False)

    end_date = db.Column(db.Date, nullable=False)

    start_time = db.Column(db.Time, nullable=False)

    end_time = db.Column(db.Time, nullable=False)

    max_participants = db.Column(db.Integer)

    organizer_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    status = db.Column(db.String(20), default="pending")

    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):

        return f"<Event {self.title}>"
