from models.user_model import db


class Performer(db.Model):

    __tablename__ = 'performers'

    id = db.Column(db.Integer, primary_key=True)

    event_id = db.Column(
        db.Integer,
        db.ForeignKey('events.id'),
        nullable=False
    )

    performer_name = db.Column(
        db.String(200),
        nullable=False
    )

    performance_title = db.Column(
        db.String(200),
        nullable=False
    )

    performance_time = db.Column(
        db.String(100)
    )

    description = db.Column(db.Text)

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )