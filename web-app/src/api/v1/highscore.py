from flask import current_app as app
from flask import Blueprint, jsonify, request

from ...services.abstracts.AbcHighscoreService import AbcHighscoreService
from ...services.HighscoreService import HighscoreService


__highscoreservice: AbcHighscoreService = HighscoreService()


api_v1__highscore_controller = Blueprint(
    'api_v1__highscore_controller',
    __name__,
    url_prefix='/api/v1/highscore'
)


@api_v1__highscore_controller.route('/update', methods=['GET'])
def update():
    """
    Run the Highscore Calculation and Update Entries
    """

    if request.args.get('migrationkey') != app.config['MIGRATION_KEY']:
        return jsonify({'status': 'denied'}), 403

    status_message: str = 'failed'
    status_code: int = 500

    if __highscoreservice.calculate_highscores_and_update():
        status_message = 'success'
        status_code = 200

    return jsonify(
        {'status': status_message}
    ), status_code
