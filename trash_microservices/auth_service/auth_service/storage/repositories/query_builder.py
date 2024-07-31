from pypika import Query, Table, Criterion


class CRUDQueryBuilder:

    @staticmethod
    def create(table: Table, fields: tuple) -> str:
        return Query.into(table).insert(*fields).get_sql()

    @staticmethod
    def read(table: Table, fields: tuple, condition: Criterion = None) -> str:
        q = Query.from_(table).select(*fields)

        # if condition is not provided -- generate "get all" query
        if condition is not None:
            q = q.where(condition)

        return q.get_sql()

    @staticmethod
    def update(table: Table, fields: [str, str], condition: Criterion) -> str:
        q = Query.update(table)

        for field in fields:
            # first value - field name
            # second value - field value
            q = q.set(field[0], field[1])

        q = q.where(condition).get_sql()

        return q

    @staticmethod
    def delete(table: Table, condition: Criterion) -> str:
        return Query.from_(table).delete().where(condition).get_sql()
