from typing import List
from flask import Blueprint, render_template, url_for, escape, flash
from flask_login import login_required, current_user
from werkzeug.utils import redirect

from ...models.user.User import User
from ...models.quizgame.QuizGameResult import QuizGameResult

from ...repositories.abstracts.AbcUserRepository import AbcUserRepository
from ...repositories.abstracts.AbcQuizGameResultRepository import AbcQuizGameResultRepository
from ...repositories.UserRepository import UserRepository
from ...repositories.QuizGameResultRepository import QuizGameResultRepository


from ...services.abstracts.AbcUserService import AbcUserService
from ...services.abstracts.AbcQuizSuggestionService import AbcQuizSuggestionService
from ...services.abstracts.AbcHighscoreService import AbcHighscoreService
from ...services.UserService import UserService
from ...services.QuizSuggestionService import QuizSuggestionService
from ...services.HighscoreService import HighscoreService

from .viewmodels.UserProfileViewModel import UserProfileViewModel

__userrepository: AbcUserRepository = UserRepository()
__quizgameresultrepository: AbcQuizGameResultRepository = QuizGameResultRepository()
__userservice: AbcUserService = UserService()
__quizsuggestionservice: AbcQuizSuggestionService = QuizSuggestionService()
__highscoreservice: AbcHighscoreService = HighscoreService()


user_controller = Blueprint(
    'user_controller',
    __name__,
    template_folder='views',
    url_prefix='/user'
)


@user_controller.before_request
@login_required
def before_request():
    pass


# User/Profile
@user_controller.route('/profile', methods=['GET'])
def profile():
    """
    User Profile Overview Page
    """

    user: User = __userrepository.find_by_id(current_user.id)

    role_status = '-'

    if __userservice.is_user_tutor(user):
        role_status = 'Tutor'
    elif __userservice.is_user_student(user):
        role_status = 'Student'

    all_quizgameresults: List[QuizGameResult] = __quizgameresultrepository.get_all_finalized_by_userid(current_user.id)

    viewmodel = UserProfileViewModel()

    viewmodel.email = user.email
    viewmodel.is_email_verified = user.is_active

    viewmodel.amount_played_games = all_quizgameresults.count()

    viewmodel.amount_games_won = 0
    for quizgame in all_quizgameresults:
        if quizgame.is_won:
            viewmodel.amount_games_won += 1

    viewmodel.amount_games_lost = viewmodel.amount_played_games - viewmodel.amount_games_won

    viewmodel.is_highscore_enabled.data = user.is_highscore_enabled
    viewmodel.highscore_alias.data = user.highscore_alias
    viewmodel.highscore_rank = __highscoreservice.get_rank_for_user(user.id)

    viewmodel.registered_since = user.creation_date.strftime("%d.%m.%Y")
    viewmodel.role_status = role_status
    viewmodel.user_profile_quiz_suggestion = __quizsuggestionservice.get_stat_values_for_user_profile_by_user_id(user.id)

    return render_template(
        'profile.jinja2',
        viewmodel=viewmodel
    )


@user_controller.route('/save-highscore', methods=['POST'])
def save_highscore():
    """
    Saves the User Highscore Setting
    """
    viewmodel = UserProfileViewModel()

    if viewmodel.validate_on_submit():
        user: User = __userrepository.find_by_id(current_user.get_id())
        if not user.is_highscore_enabled:
            user.is_highscore_enabled = viewmodel.is_highscore_enabled.data

        user_highscore_alias: str = escape(viewmodel.highscore_alias.data)
        if not __userservice.is_useralias_already_existing(user_highscore_alias):
            user.highscore_alias = user_highscore_alias
        else:
            flash('Dieser Alias existiert bereits.')

        __userrepository.commit()

    return redirect(url_for('user_controller.profile'))
