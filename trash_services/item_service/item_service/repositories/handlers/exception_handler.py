from item_service.repositories.exceptions import InternalRepositoryException, DataNotFoundException

from sqlalchemy.exc import SQLAlchemyError, NoResultFound

from loguru import logger

class RepositoryExceptionHandler:
    _exception_mapping = {
        NoResultFound: DataNotFoundException,
        SQLAlchemyError: InternalRepositoryException
    }

    @classmethod
    def handle(cls, exception: SQLAlchemyError):
        logger.error(f'{type(exception)} raised {exception.args[0]}')
        mapped_exc = cls._exception_mapping.get(type(exception), None)
        if mapped_exc is not None:
            raise mapped_exc()
        else:
            raise InternalRepositoryException()
