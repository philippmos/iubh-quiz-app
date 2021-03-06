import os
from dotenv import load_dotenv


class Config(object):

    basedir = os.path.abspath(os.path.dirname(__file__))
    load_dotenv(os.path.join(basedir, '.env'))

    # General Application Configuration
    FLASK_APP = 'app.py'

    SECRET_KEY = os.environ.get("SECRET_KEY")

    FLASK_ENV = os.environ.get("FLASK_ENV")

    MIGRATION_KEY = os.environ.get("MIGRATION_KEY")

    DEBUG = False
    TESTING = False

    APP_ENCODING_TYPE = "utf-8"

    # Database Settings
    SQLALCHEMY_DATABASE_URI = os.environ.get("POSTGRESQLCONNSTR_APPDB")
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEFAULT_RESULT_ITEM_MAX_COUNT = 100
    IS_CACHING_ENABLED = (os.environ.get("IS_CACHING_ENABLED") == 'True')

    # Google Tag Manager
    GOOGLE_TAGMANAGER_ACTIVE = (os.environ.get("GOOGLE_TAGMANAGER_ACTIVE") == 'True')
    GOOGLE_TAGMANAGER_KEY = os.environ.get("GOOGLE_TAGMANAGER_KEY")

    # Google ReCaptcha v3
    IS_GOOGLE_RECAPTCHA_ACTIVE = (os.environ.get("IS_GOOGLE_RECAPTCHA_ACTIVE") == 'True')
    GOOGLE_RECAPTCHA_SITEKEY = os.environ.get("GOOGLE_RECAPTCHA_SITEKEY")
    GOOGLE_RECAPTCHA_SECRETKEY = os.environ.get("GOOGLE_RECAPTCHA_SECRETKEY")
    GOOGLE_RECAPTCHA_SITEVERIFY_URL = 'https://www.google.com/recaptcha/api/siteverify'

    # Signup Process
    IS_SIGNUP_EMAIL_VALIDATION_ACTIVE = (os.environ.get("IS_SIGNUP_EMAIL_VALIDATION_ACTIVE") == 'True')
    USER_SIGNUP_EMAIL_LIMITATION = os.environ.get("USER_SIGNUP_EMAIL_LIMITATION")

    # Userlike
    IS_USERLIKE_ACTIVE = (os.environ.get("IS_USERLIKE_ACTIVE") == 'True')
    USERLIKE_SECRET = os.environ.get("USERLIKE_SECRET")

    # UserRoles
    USERROLE_STUDENT = 1
    USERROLE_TUTOR = 2

    # Quiz Module
    AMOUNT_OF_QUESTIONS_PER_QUIZ = 5
    AMOUNT_OF_ANSWERS_PER_QUESTION = 3
    SHOW_QUESTIONRESULTS_ONLY_SUMMARIZED = False

    # User Dashboard
    DASHBOARD_AMOUNT_OF_QUIZGAMES = 4

    # Swagger UI
    SWAGGERUI_API_PATH = '/api/docs'
    SWAGGERUI_CONFIGURATION_LOCATION = '/static/swagger.json'

    # External Applications
    QUICKSTART_DOCUMENTATION_URL = "https://iuquiz.gitbook.io/quickstart/"
    GRAVATAR_URL = "https://www.gravatar.com/avatar/"

    # Special Environment Settings
    if FLASK_ENV == 'development':
        DEBUG = True
        TESTING = True
        SQLALCHEMY_ECHO = True
    elif FLASK_ENV == 'staging':
        TESTING = True
