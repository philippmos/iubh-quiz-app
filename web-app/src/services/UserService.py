from .. import login_manager
from flask import redirect, url_for

from .abstracts.AbcUserService import AbcUserService

class UserService(AbcUserService):

    @login_manager.user_loader
    def load_user(user_id):
        return User.get(user_id)


    @login_manager.unauthorized_handler
    def unauthorized():
        # TODO: Needs to be enabled once we implemented Login-Action on Friday
        # return redirect(url_for('auth_controller.login'))
        raise NotImplementedError