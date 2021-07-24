from flask import Blueprint, render_template, url_for
from flask_login import login_required, current_user
from werkzeug.utils import redirect

from ...models.user.User import User

from ...repositories.abstracts.AbcUserRepository import AbcUserRepository
from ...repositories.UserRepository import UserRepository

from ...services.abstracts.AbcUserService import AbcUserService
from ...services.abstracts.AbcQuizSuggestionService import AbcQuizSuggestionService
from ...services.UserService import UserService
from ...services.QuizSuggestionService import QuizSuggestionService

from .viewmodels.UserProfileViewModel import UserProfileViewModel

__userrepository: AbcUserRepository = UserRepository()
__userservice: AbcUserService = UserService()
__quizsuggestionservice: AbcQuizSuggestionService = QuizSuggestionService()


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

    user = __userrepository.find_by_id(current_user.id)

    role_status = '-'

    if __userservice.is_user_tutor(user):
        role_status = 'Tutor'
    elif __userservice.is_user_student(user):
        role_status = 'Student'

    viewmodel = UserProfileViewModel()
    viewmodel.email = user.email
    viewmodel.is_email_verified = user.is_active
    viewmodel.is_highscore_enabled.data = user.is_highscore_enabled
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
        user: User = UserRepository.find_by_id(current_user.get_id())
        user.is_highscore_enabled = viewmodel.is_highscore_enabled.data

        UserRepository.commit()

    return redirect(url_for('user_controller.profile'))
