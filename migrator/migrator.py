import argparse
import psycopg2
import os


class Migrator:
    dbname = None
    user = None
    dirpath = None

    @classmethod
    def __init__(cls, dbname: str = None, user: str = 'postgres', dirpath: str = None):
        if dbname is None:
            raise AttributeError
        cls.dbname = dbname

        if user is None:
            raise AttributeError
        cls.user = user

        if dirpath is None:
            raise AttributeError
        cls.dirpath = dirpath

    @classmethod
    def exec(cls):
        # iterating over each migration in the specified directory
        migrations = sorted(os.listdir(cls.dirpath))
        for migration in migrations:
            if migration.endswith(".sql"):
                cls._handle_migration(migration)

    @classmethod
    def _handle_migration(cls, migration):
        filepath = cls.dirpath + migration
        fd = os.open(filepath, os.O_RDONLY)
        script = os.read(fd, os.stat(filepath).st_size).decode()

        connection = psycopg2.connect(f"dbname={cls.dbname} user={cls.user}")
        try:
            cur = connection.cursor()
            cur.execute(script)
            cur.close()
        except psycopg2.OperationalError as err:
            print(err)

        connection.commit()
        connection.close()

        os.close(fd)


def handle_args(*args):
    parser = argparse.ArgumentParser()

    for arg in args:
        parser.add_argument(arg)
    args = parser.parse_args()

    return args


if __name__ == "__main__":
    args = handle_args("dbname", "user", "dirpath")

    Migrator(args.dbname, args.user, args.dirpath)
    Migrator.exec()
