from injector import inject

from ..db_session import DatabaseSession


class BaseRepository:
    @inject
    def __init__(self, db: DatabaseSession):
        self.db = db
