from typing import List, Dict, Union, Any
from enum import Enum


class TYPING(Enum):
    PARAMS = Dict[str, Dict[str, Any]]
    STR_LIST = List[str]
    RETURN_VALURE = Union[None, Any]
