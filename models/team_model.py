from models.user_model import db


class Team(db.Model):

    __tablename__ = 'teams'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    team_name = db.Column(
        db.String(200),
        nullable=False
    )

    leader_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )

    category_id = db.Column(
        db.Integer,
        db.ForeignKey('event_categories.id'),
        nullable=False
    )