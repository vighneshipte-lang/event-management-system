from models.user_model import db


class EventCategory(db.Model):

    __tablename__ = 'event_categories'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    event_id = db.Column(
        db.Integer,
        db.ForeignKey('events.id'),
        nullable=False
    )

    category_name = db.Column(
        db.String(200),
        nullable=False
    )

    registration_type = db.Column(
        db.String(50),
        nullable=False
    )
    # solo or team

    prize_amount = db.Column(
        db.Float,
        nullable=False
    )

    max_participants = db.Column(
        db.Integer,
        nullable=False
    )