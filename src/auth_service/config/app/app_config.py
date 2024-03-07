# DEPRECATED
# DEPRECATED
# DEPRECATED
from dataclasses import dataclass
import json

config_path = "app_config.json"


@dataclass
class AppConfig:
    debug = json.load(open(config_path)).get("DEBUG")
    secret = json.load(open(config_path)).get("SECRET")
