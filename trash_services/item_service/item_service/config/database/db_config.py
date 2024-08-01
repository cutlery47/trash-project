from dataclasses import dataclass

@dataclass
class DBConfig:
    driver: str = ""
    host: str = ""
    port: str = ""
    dbname: str = ""
    username: str = ""
    password: str = ""
