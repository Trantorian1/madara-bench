from enum import Enum
from typing import Union

import pydantic


class NodeName(str, Enum):
    madara = "madara"


class BlockTag(str, Enum):
    latest = "latest"
    pending = "pending"


class BlockId(Enum):
    block_hash: str
    block_number: int
    block_tag: BlockTag
