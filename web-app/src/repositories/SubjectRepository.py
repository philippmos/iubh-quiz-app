from typing import List

from .abstracts.AbcSubjectRepository import AbcSubjectRepository
from .Repository import Repository
from ..models.Subject import Subject


class SubjectRepository(Repository, AbcSubjectRepository):

    @staticmethod
    def get_all() -> List[Subject]:
        """
        Returns all available Items
        """
        return Subject.query.all()


    @staticmethod
    def find_by_id(id) -> Subject:
        """
        Get a specific Item by ID
        """
        return Subject.query.get(id)
