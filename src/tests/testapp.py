import pytest

from src.auth_service.app import TrashAssApplication


@pytest.fixture
def setup():
    trash_test = TrashAssApplication.create()

    from src.auth_service.router.router import router
    trash_test.register_blueprint(router)

    trash_test.run(host="0.0.0.0", port=9876)

