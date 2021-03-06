from flask_login import login_required, current_user
from flask import Blueprint, render_template, session, request, redirect, url_for, escape
from flask import current_app as app
from datetime import datetime

from ...models.suggestquestion.QuizSuggestion import QuizSuggestion

from .viewmodels.SubjectSelectionViewModel import SubjectSelectionViewModel
from .viewmodels.QuestionAndAnswerViewModel import QuestionAndAnswerViewModel

from ...repositories.abstracts.AbcQuizSuggestionRepository import AbcQuizSuggestionRepository
from ...repositories.QuizSuggestionRepository import QuizSuggestionRepository

from ...services.abstracts.AbcQuizSuggestionService import AbcQuizSuggestionService
from ...services.QuizSuggestionService import QuizSuggestionService


__quizsuggestionrepository: AbcQuizSuggestionRepository = QuizSuggestionRepository()
__quizsuggestionservice: AbcQuizSuggestionService = QuizSuggestionService()


suggestquestion_controller = Blueprint(
    'suggestquestion_controller',
    __name__,
    template_folder='views',
    url_prefix='/suggest-question'
)


@suggestquestion_controller.before_request
@login_required
def before_request():
    pass


# SuggestQuestion/SubjectSelection
@suggestquestion_controller.route('/subject-selection', methods=['GET', 'POST'])
def subjectselection():
    """
    Provides Option to select Subject, validate Input and store Information in Session
    """
    subject_selection_viewmodel = SubjectSelectionViewModel()

    if session.get('quizsuggest__subject_id') and session.get('quizsuggest__subject_name'):
        subject_selection_viewmodel.subject_id.data = session.get('quizsuggest__subject_id')
        subject_selection_viewmodel.subject_name.data = session.get('quizsuggest__subject_name')

    if request.method == 'POST' and subject_selection_viewmodel.validate_on_submit():
        session['quizsuggest__subject_id'] = escape(subject_selection_viewmodel.subject_id.data)
        session['quizsuggest__subject_name'] = escape(subject_selection_viewmodel.subject_name.data)

        return redirect(url_for('suggestquestion_controller.questionandanswer'))

    return render_template(
        'subjectselection.jinja2',
        form=subject_selection_viewmodel
    )


# SuggestQuestion/QuestionAndAnswer
@suggestquestion_controller.route('/question-and-answer', methods=['GET', 'POST'])
def questionandanswer():
    """
    Validate User Input for Question and Answer, finalizes Requests and Create Database Entries
    """
    questionandanswer_viewmodel = QuestionAndAnswerViewModel()

    if session.get('quizsuggest__subject_id'):
        questionandanswer_viewmodel.subject_id.data = session.get('quizsuggest__subject_id')
    else:
        return redirect(url_for('suggestquestion_controller.subjectselection'))

    if request.method == 'POST' and questionandanswer_viewmodel.validate_on_submit():

        new_quizsuggestion = QuizSuggestion()
        new_quizsuggestion.question = escape(questionandanswer_viewmodel.question_text.data)
        new_quizsuggestion.creation_date = datetime.now()
        new_quizsuggestion.is_approved = False
        new_quizsuggestion.is_declined = False
        new_quizsuggestion.subject_id = escape(questionandanswer_viewmodel.subject_id.data)
        new_quizsuggestion.user_id = current_user.id

        __quizsuggestionrepository.add_and_commit(new_quizsuggestion)

        if not new_quizsuggestion.id:
            return redirect(url_for('suggestquestion_controller.questionandanswer'))

        if not __quizsuggestionservice.add_answer_for_quizsuggestion(
            escape(questionandanswer_viewmodel.answer_1_text.data),
            questionandanswer_viewmodel.correct_answer_flag.data == '1',
            new_quizsuggestion.id
        ):
            app.logger.warn('QuizSuggestionAnswer was not saved successfully')

        if not __quizsuggestionservice.add_answer_for_quizsuggestion(
            escape(questionandanswer_viewmodel.answer_2_text.data),
            questionandanswer_viewmodel.correct_answer_flag.data == '2',
            new_quizsuggestion.id
        ):
            app.logger.warn('QuizSuggestionAnswer was not saved successfully')

        if not __quizsuggestionservice.add_answer_for_quizsuggestion(
            escape(questionandanswer_viewmodel.answer_3_text.data),
            questionandanswer_viewmodel.correct_answer_flag.data == '3',
            new_quizsuggestion.id
        ):
            app.logger.warn('QuizSuggestionAnswer was not saved successfully')

        session['quizsuggest__subject_id'] = None
        session['quizsuggest__subject_name'] = None

        return redirect(url_for('suggestquestion_controller.thanks'))

    return render_template(
        'questionandanswer.jinja2',
        form=questionandanswer_viewmodel
    )


# SuggestQuestion/Thanks
@suggestquestion_controller.route('/thanks', methods=['GET'])
def thanks():
    """
    Final Success Page, that is called when every Operation worked fine
    """

    return render_template('thanks.jinja2')
