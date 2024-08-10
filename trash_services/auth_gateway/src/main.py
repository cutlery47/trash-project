from src.application.factory import ApplicationFactory

app = ApplicationFactory.create(db_config_path="src/config/database/db_config.json").asgi_app()
