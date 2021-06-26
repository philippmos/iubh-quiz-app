from ... import db


class QuizGameSetupAnswer(db.Model):

    __tablename__ = 'quiz_game_setup_answers'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    quizanswer_text = db.Column(
        db.String(),
        index=False,
        unique=False,
        nullable=False
    )

    quizanswer_is_correct = db.Column(
        db.Boolean()
    )

    quizanswer_id = db.Column(
        db.Integer,
        db.ForeignKey('quiz_answers.id'),
        nullable=False
    )

    quizgamesetup_id = db.Column(
        db.Integer,
        db.ForeignKey('quiz_game_setups.id'),
        nullable=False
    )
