from dataclasses import dataclass
import json

config_path = "config/database/db_config.json"


@dataclass
class DBConfig:
    dbname = json.load(open(config_path)).get("DBNAME")
    user = json.load(open(config_path)).get("USER")
