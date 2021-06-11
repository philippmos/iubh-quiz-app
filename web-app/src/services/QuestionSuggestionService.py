from flask import current_app as app
from typing import List

from .abstracts.AbcQuestionSuggestionService import AbcQuestionSuggestionService

from ..repositories.QuizSuggestionAnswerRepository import QuizSuggestionAnswerRepository

from ..models.suggestquestion.QuizSuggestionAnswer import QuizSuggestionAnswer


class QuestionSuggestionService(AbcQuestionSuggestionService):

    @staticmethod    
    def add_answer_for_questionsuggestion(text, is_correct, quiz_suggestion_id) -> bool:
        """
        Adds Answer related to QuestionSuggestion to Database
        """
        new_answer = QuizSuggestionAnswer()
        new_answer.text = text
        new_answer.is_correct = is_correct
        new_answer.quiz_suggestion_id = quiz_suggestion_id

        QuizSuggestionAnswerRepository().add_and_commit(new_answer)

        if new_answer.id:
            return True
        else:
            app.logger.critical('New Answer for Questionsuggestion has not been created')
            return False


    