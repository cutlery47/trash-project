from item_service.exceptions.repository_exceptions import InternalRepositoryException, DataNotFoundException

from sqlalchemy.exc import SQLAlchemyError, NoResultFound

from loguru import logger

class RepositoryExceptionHandler:
    _exception_mapping = {
        NoResultFound: DataNotFoundException,
        SQLAlchemyError: InternalRepositoryException
    }

    @classmethod
    def handle(cls, exception: SQLAlchemyError):
        logger.error(exception.args[0])
        raise cls._exception_mapping[type(exception)]()
