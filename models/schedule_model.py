from models.user_model import db


class Schedule(db.Model):

    __tablename__ = 'schedules'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    event_id = db.Column(
        db.Integer,
        db.ForeignKey('events.id'),
        nullable=False
    )

    category_id = db.Column(
        db.Integer,
        db.ForeignKey('event_categories.id'),
        nullable=True
    )

    participant_name = db.Column(
        db.String(200),
        nullable=False
    )

    stage_name = db.Column(
        db.String(200),
        nullable=False
    )
    # Finals, Semi Finals, Classical Round etc.

    event_day = db.Column(
        db.Date,
        nullable=False
    )

    start_time = db.Column(
        db.Time,
        nullable=False
    )

    end_time = db.Column(
        db.Time,
        nullable=False
    )

    category = db.relationship(
    'EventCategory',
    backref='schedules',
    lazy=True
    )