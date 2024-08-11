from dataclasses import dataclass

@dataclass
class CacheConfig:
    port: str = None,
    host: str = None,
    decode_responses: bool = None,

