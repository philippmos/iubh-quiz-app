from ... import db


class HighscoreRank(db.Model):

    __tablename__ = 'highscore_ranks'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    rank = db.Column(
        db.Integer,
        index=False,
        unique=True,
        nullable=False
    )

    user_profilepicture = db.Column(
        db.String(),
        unique=False,
        nullable=False
    )

    user_alias = db.Column(
        db.String(255),
        nullable=False,
        unique=True
    )

    amount_of_games_won = db.Column(
        db.Integer,
        nullable=False,
        unique=False
    )