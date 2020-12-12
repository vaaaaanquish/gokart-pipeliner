from typing import List, Dict, Any
from enum import Enum


class TYPING(Enum):
    PARAMS = Dict[str, Dict[str, Any]]
    STR_LIST = List[str]
