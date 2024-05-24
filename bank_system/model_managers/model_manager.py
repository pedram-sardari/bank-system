from ..db import db_queries as q


class ModelManager:
    """Fetch data from database and convert to Python objects"""

    def __init__(self, db_manager, table_name, model_class):
        self.db_manager = db_manager
        self.table_name = table_name
        self.model_class = model_class

    def _generate_query_from_kwargs(self, **kwargs):
        query = q.ALL.format(self.table_name)
        params = []
        if kwargs:
            query += q.WHERE
            query += q.AND.join([q.BY_COLUMN.format(column) for column in kwargs.keys()])
            params = tuple(kwargs.values())
        return query, params

    def _execute_query_from_kwargs(self, cursor, **kwargs):
        query, params = self._generate_query_from_kwargs(**kwargs)
        cursor.execute(query, params)

    def get(self, **kwargs):
        with self.db_manager as cursor:
            self._execute_query_from_kwargs(cursor, **kwargs)
            record = cursor.fetchone()
            if record:
                return self.model_class(**record)
            # TODO: raise a proper Error

    def all(self):
        return self.filter()
        # TODO: raise a proper Error

    def filter(self, **kwargs):
        with self.db_manager as cursor:
            self._execute_query_from_kwargs(cursor, **kwargs)
            records = cursor.fetchall()
            if records:
                return [self.model_class(**record) for record in records]
            # TODO: raise a proper Error
