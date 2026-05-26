from models.user_model import db
from models.user_model import User
from models.event_model import Event
from models.event_category_model import EventCategory
from models.team_model import Team


class Participation(db.Model):

    __tablename__ = "participations"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    event_id = db.Column(
        db.Integer,
        db.ForeignKey("events.id"),
        nullable=False
    )

    category_id = db.Column(
        db.Integer,
        db.ForeignKey("event_categories.id"),
        nullable=True
    )

    team_id = db.Column(
        db.Integer,
        db.ForeignKey("teams.id"),
        nullable=True
    )

    joined_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    performance_time = db.Column(
        db.String(100)
    )

    status = db.Column(
        db.String(20),
        default="pending"
    )

    # Relationships

    user = db.relationship(
        "User",
        backref="participations",
        lazy=True
    )

    event = db.relationship(
        "Event",
        backref="participations",
        lazy=True
    )

    category = db.relationship(
        "EventCategory",
        backref="participations",
        lazy=True
    )

    team = db.relationship(
        "Team",
        backref="participations",
        lazy=True
    )