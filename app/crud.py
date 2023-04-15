import re
from random import randint

from tinydb import Query, TinyDB

from app.config import Settings

settings = Settings()


class CRUD:
    """The `CRUD` class is meant to emulate common database operations. It is a thin wrapper over
    TinyDB. It allows the usage of one method, whether operating on default table or one that is
    declared. Ordinarily, you might use a more robust ORM/ODM of your choice.

    Usage:
        `db = CRUD()` creates an instance of the CRUD class. ALl operations will be performed
        on the default table (the table name is `_default`).

        `db = CRUD(table="table_name")` creates an instance of the CRUD class, but defines the
        table that will be used for all operations.

        Then you can run any of the operations here, such as: `items = db.all_items()`

        Note that using an operation like `db.find("key", "value")` creates a query object,
        (`Query()`) which is used by TinyDB to search for the specified key within a table.

    Arguments:
        db: An instance of TinyDB
        table: The name of the table to use. If None, the default table will be used.
    """

    def __init__(
        self,
        db: TinyDB | None = None,
        table: str | None = None,
        db_name: str | None = "data.json",
    ):
        self.db = db
        self.query = Query()
        self.table = table
        self.db_name = db_name

    def all_items(self):
        if not self.db:
            self.init_db
        if self.table:
            self.db = self.table
        return self.db.all()

    def insert(self, data: dict):
        if not self.table:
            return self.db.upsert(data)
        return self.table.insert(data)

    def add(self, payload: dict):
        if not self.table:
            return self.db.insert(payload)
        return self.table.insert(payload)

    def find(self, key: str, value: str):
        q = getattr(self.query, key)
        if not self.table:
            return self.db.search(q == value)
        return self.table.search(q == value)

    def search(self, key: str, value: str):
        if not value:
            return None
        q = getattr(self.query, key)
        if not self.table:
            return self.db.search(q.search(f"{value}+", flags=re.IGNORECASE))
        return self.table.search(q.search(f"{value}+", flags=re.IGNORECASE))

    def get_random_item(self):
        if not self.table:
            num = randint(1, len(self.db))
            return self.db.get(doc_id=num)
        num = randint(1, len(self.table))
        return self.table.get(doc_id=num)

    @property
    def init_db(self):
        path = str(settings.DATA_DIR / self.db_name)
        self.db = TinyDB(path, sort_keys=True, indent=4, separators=(",", ": "))
        return self.db

    @classmethod
    def with_table(cls, table_name: str):
        crud = cls()
        _db = crud.init_db
        _table = _db.table(table_name)
        return cls(db=_db, table=_table)

