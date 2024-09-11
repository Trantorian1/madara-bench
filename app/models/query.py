from typing import Annotated

import fastapi

from .models import *

BlockHash = Annotated[
    str | None,
    fastapi.Query(
        pattern=REGEX_HEX,
        description="A block hash, represented as a field element",
    ),
]


BlockNumber = Annotated[
    int | None, fastapi.Query(ge=0, description="A block number")
]

QueryBlockTag = Annotated[
    BlockTag | None,
    fastapi.Query(
        description="A block tag, ca be either 'latest' to reference the last synchronized block, or 'pending' to reference the last unverified block to yet be added to the chain",
    ),
]

ContractAddress = Annotated[
    str,
    fastapi.Query(
        pattern=REGEX_HEX,
        description="Address of a contract on-chain",
    ),
]

ContractKey = Annotated[
    str,
    fastapi.Query(
        pattern=REGEX_HEX, description="Key to a storage element in a contract"
    ),
]

TxHash = Annotated[
    str,
    fastapi.Query(
        pattern=REGEX_HEX, description="Address of a Transaction on-chain"
    ),
]

TxIndex = Annotated[
    int,
    fastapi.Query(
        ge=0,
        description="Index of a transaction in a given block, in order of occurrence",
    ),
]

ClassHash = Annotated[
    str,
    fastapi.Query(pattern=REGEX_HEX, description="Address of a class on-chain"),
]

BlockId = BlockHash | BlockNumber | BlockTag
