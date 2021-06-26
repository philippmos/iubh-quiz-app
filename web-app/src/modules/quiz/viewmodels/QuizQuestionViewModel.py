from flask_wtf import FlaskForm
from wtforms import HiddenField, SubmitField, RadioField
from wtforms.validators import DataRequired


class QuizQuestionViewModel(FlaskForm):

    question_text: str = ''

    answers = {}

    question_number = HiddenField(
        'question-number',
        validators=[
            DataRequired()
        ]
    )

    answer_selection = RadioField(choices=[('A', 'a'), ('B', 'b'), ('C', 'c')])

    submit = SubmitField('Diese Frage auswerten')