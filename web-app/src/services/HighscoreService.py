from typing import List
from datetime import datetime

from .abstracts.AbcHighscoreService import AbcHighscoreService

from ..models.highscore.HighscoreRank import HighscoreRank
from ..models.user.User import User

from ..modules.highscore.viewmodels.HighscoreRankViewModel import HighscoreRankViewModel
from ..modules.highscore.viewmodels.HighscoreOverviewViewModel import HighscoreOverviewViewModel

from ..repositories.HighscoreRankRepository import HighscoreRankRepository
from ..repositories.QuizGameResultRepository import QuizGameResultRepository
from ..repositories.UserRepository import UserRepository

from ..helpers.ImageHelper import ImageHelper


class HighscoreService(AbcHighscoreService):

    @staticmethod
    def get_highscoreoverview_viewmodel() -> HighscoreOverviewViewModel:
        viewmodel = HighscoreOverviewViewModel()
        viewmodel.highscorerank_viewmodels = HighscoreService.get_highscore_rank_viewmodel_list()
        viewmodel.last_updated = HighscoreService.get_last_update_datestring()

        return viewmodel

    @staticmethod
    def get_highscore_rank_viewmodel_list() -> List[HighscoreRankViewModel]:
        """
        Builds all Highscore Ranks and return List of ViewModles
        """

        all_highscoreranks = HighscoreRankRepository.get_all_ordered_by_rank()

        viewmodel_list = []

        for highscorerank in all_highscoreranks:
            viewmodel = HighscoreRankViewModel()
            viewmodel.rank = highscorerank.rank
            viewmodel.user_alias = highscorerank.user_alias
            viewmodel.user_profilepicture = highscorerank.user_profilepicture
            viewmodel.amount_of_games_won = highscorerank.amount_of_games_won

            viewmodel_list.append(viewmodel)

        return viewmodel_list

    @staticmethod
    def calculate_highscores_and_update() -> bool:

        results_sorted = sorted(
            QuizGameResultRepository.get_all_grouped_and_count_by_user(),
            key=lambda x: x.amount_of_games_won,
            reverse=True
        )

        counter = 0

        if len(results_sorted) > 0:
            HighscoreService.__cleanup_highscore_entries()

        for result in results_sorted:

            user: User = UserRepository.find_by_id(result.user_id)

            if not user or not user.is_highscore_enabled:
                continue

            counter += 1

            highscore_rank: HighscoreRank = HighscoreRank()

            highscore_rank.rank = counter
            highscore_rank.user_id = user.id
            highscore_rank.user_alias = user.highscore_alias
            highscore_rank.user_profilepicture = ImageHelper.build_gavatar_image_url(user.email)
            highscore_rank.amount_of_games_won = result.amount_of_games_won
            highscore_rank.last_update = datetime.now()

            HighscoreService.__replace_or_create_ranking(highscore_rank)

        return True

    @staticmethod
    def get_last_update_datestring() -> str:
        last_updated_item: HighscoreRank = HighscoreRankRepository.get_last_updated_item()

        if not last_updated_item:
            return '-'

        return last_updated_item.last_update.strftime('%d.%m.%Y %H:%M')

    @staticmethod
    def get_rank_for_user(user_id: int) -> str:
        highscore_rank = HighscoreRankRepository.get_item_by_user_id(user_id)

        if highscore_rank:
            return highscore_rank.rank

        return '-'

    @staticmethod
    def __replace_or_create_ranking(highscore_rank: HighscoreRank) -> None:

        db_highscorerank: HighscoreRank = HighscoreRankRepository.find_by_rank(highscore_rank.rank)

        if db_highscorerank:
            if (
                db_highscorerank.user_id != highscore_rank.user_id or
                db_highscorerank.amount_of_games_won != highscore_rank.amount_of_games_won
            ):
                db_highscorerank.last_update = highscore_rank.last_update

            db_highscorerank.user_id = highscore_rank.user_id
            db_highscorerank.user_alias = highscore_rank.user_alias
            db_highscorerank.user_profilepicture = highscore_rank.user_profilepicture
            db_highscorerank.amount_of_games_won = highscore_rank.amount_of_games_won

        else:
            HighscoreRankRepository.add(highscore_rank)

        HighscoreRankRepository.commit()

    @staticmethod
    def __cleanup_highscore_entries() -> None:
        """
        Cleans up all current Highscore Entries
        """

        highscore_ranks = HighscoreRankRepository.get_all(5000)

        for highscore_rank in highscore_ranks:

            HighscoreRankRepository.delete(highscore_rank)

        HighscoreRankRepository.commit()
