from models.user_model import db


class Participation(db.Model):

    __tablename__ = "participations"

    id = db.Column(db.Integer, primary_key=True)

    team_id = db.Column(
    db.Integer,
    db.ForeignKey('teams.id'),
    nullable=True
    )

    category_id = db.Column(
        db.Integer, db.ForeignKey("event_categories.id"), nullable=True
    )

    category = db.relationship("EventCategory", backref="participations", lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False)

    joined_at = db.Column(db.DateTime, server_default=db.func.now())

    performance_time = db.Column(db.String(100))

    status = db.Column(db.String(20), default="pending")
