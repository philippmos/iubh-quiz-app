from flask import Blueprint, render_template
from flask_login import login_required

from .viewmodels.QuizQuestionViewModel import QuizQuestionViewModel


quiz_controller = Blueprint(
    'quiz_controller',
    __name__,
    template_folder='views',
    url_prefix='/quiz'
)


@quiz_controller.before_request
@login_required
def before_request():
    pass


# Quiz/Question/{question_number}
@quiz_controller.route('/question/<int:question_number>', methods=['GET'])
def question(question_number: int):
    """
    Quiz Question
    """

    viewmodel = QuizQuestionViewModel(
        'Lorem ipsum dolor sit amet?',
        [
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit',
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit',
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit'
        ]
    )

    viewmodel.question_number = question_number

    return render_template(
        'question.jinja2',
        question_number=str(question_number),
        viewmodel=viewmodel
    )
