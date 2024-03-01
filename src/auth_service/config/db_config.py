from dataclasses import dataclass
import json

config_path = "src/auth_service/config/db_config.json"


@dataclass
class DBConfig:
    dbname = json.load(open(config_path)).get("DBNAME")
    user = json.load(open(config_path)).get("USER")
