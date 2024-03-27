import json


class DBConfig:

    def __init__(self, config_path="auth_service/config/database/db_config.json"):
        self.dbname = json.load(open(config_path)).get("DBNAME")
        self.user = json.load(open(config_path)).get("USER")
