from enum import Enum
from typing import Annotated

import fastapi
import pydantic

REGEX_HEX: str = "^0x[a-fA-F0-9]+$"

HexEntry = Annotated[str, fastapi.Query(pattern=REGEX_HEX)]


class NodeName(str, Enum):
    madara = "madara"


class BlockTag(str, Enum):
    latest = "latest"
    pending = "pending"


class CallRequest(pydantic.BaseModel):
    contract_address: HexEntry
    entry_point_selector: HexEntry
    calldata: list[HexEntry] = []
