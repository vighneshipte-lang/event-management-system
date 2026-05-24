from models.user_model import db


class Rating(db.Model):

    __tablename__ = 'ratings'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )

    organizer_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )

    event_id = db.Column(
        db.Integer,
        db.ForeignKey('events.id'),
        nullable=False
    )

    rating = db.Column(db.Integer, nullable=False)

    review = db.Column(db.Text)

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )