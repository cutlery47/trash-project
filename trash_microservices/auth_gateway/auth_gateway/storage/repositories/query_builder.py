from pypika import Query, Table


class QueryBuilder:
    @staticmethod
    def get(table: Table, fields: tuple, condition=None) -> str:
        q = Query.from_(table).select(*fields)

        # if condition is not provided -- generate "get all" query
        if condition is not None:
            q = q.where(condition)

        return q.get_sql()

    @staticmethod
    def create(table: Table, fields: tuple) -> str:
        return Query.into(table).insert(*fields).get_sql()

    @staticmethod
    def delete(table: Table, condition) -> str:
        return Query.from_(table).delete().where(condition).get_sql()

    @staticmethod
    def update(table: Table, fields: [tuple], condition) -> str:
        q = Query.update(table)

        for field in fields:
            # first value - field name
            # second value - field value
            q = q.set(field[0], field[1])

        q = q.where(condition).get_sql()

        return q



