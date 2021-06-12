from flask import current_app as app
from .abstracts.AbcRepository import AbcRepository

from .. import db

# TODO: Switch to usage of Generics and implement get_all, get_by_id
class Repository(AbcRepository):

    @staticmethod
    def add_and_commit(item) -> None:
        """
        Adds a new Item and Commit the Changes to Database
        """
        try:
            db.session.add(item)
            db.session.commit()
        except Exception as e:
            app.logger.critical(e)
            db.session.rollback()


    @staticmethod
    def delete_and_commit(item) -> None:
        """
        Deletes a existing Item and Commit the Changes to Database
        """
        try:
            db.session.delete(item)
            db.session.commit()
        except Exception as e:
            app.logger.critical(e)
            db.session.rollback()


    @staticmethod
    def update_and_commit(item) -> None:
        """
        Updates a defined Record with new Values and Commits to Database
        """
        raise NotImplementedError



    @staticmethod
    def add(item) -> None:
        """
        Adds a new Item
        """
        try:
            db.session.add(item)
        except Exception as e:
            app.logger.critical(e)
            db.session.rollback()


    @staticmethod
    def delete(item) -> None:
        """
        Deletes a existing Item
        """
        try:
            db.session.delete(item)
        except Exception as e:
            app.logger.critical(e)
            db.session.rollback()


    @staticmethod
    def update(item) -> None:
        """
        Updates a defined Record with new Values
        """
        raise NotImplementedError


    @staticmethod
    def commit() -> None:
        """
        Commits Db-Session to Database
        """
        db.session.commit()