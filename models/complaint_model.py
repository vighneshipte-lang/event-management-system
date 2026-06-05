from models.user_model import db


class Complaint(db.Model):

    __tablename__ = 'complaints'

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

    complaint_text = db.Column(
        db.Text,
        nullable=False
    )

    status = db.Column(
        db.String(20),
        default='pending'
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    # Relationships

    user = db.relationship(
        'User',
        foreign_keys=[user_id]
    )

    organizer = db.relationship(
        'User',
        foreign_keys=[organizer_id]
    )

    event = db.relationship(
        'Event',
        foreign_keys=[event_id]
    )