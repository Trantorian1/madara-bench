import json
from typing import Any

import requests
from docker.models.containers import Container

from app import models
from app.error import ErrorBlockIdMissing

MADARA_RPC_PORT: str = "9944/tcp"
DOCKER_HOST_PORT: str = "HostPort"

STARKNET_SPEC_VERSION: str = "starknet_specVersion"
STARKNET_GET_BLOCK_WITH_TX_HASHES: str = "starknet_getBlockWithTxHashes"
STARKNET_GET_BLOCK_WITH_TXS: str = "starknet_getBlockWithTxs"
STARKNET_GET_BLOCK_WITH_RECEIPTS: str = "starknet_getBlockWithReceipts"
STARKNET_GET_STATE_UPDATE: str = "starknet_getStateUpdate"
STARKNET_GET_STORAGE_AT: str = "starknet_getStorageAt"
STARKNET_GET_TRANSACTION_STATUS: str = "starknet_getTransactionStatus"
STARKNET_GET_TRANSACTION_BY_HASH: str = "starknet_getTransactionByHash"
STARKNET_GET_TRANSACTION_BY_BLOCK_ID_AND_INDEX: str = (
    "starknet_getTransactionByBlockIdAndIndex"
)
STARKNET_GET_TRANSACTION_RECEIPT: str = "starknet_getTransactionReceipt"
STARKNET_GET_CLASS: str = "starknet_getClass"


def json_rpc(
    url: str, method: str, params: dict[str, Any] | list[Any] = {}
) -> dict[str, Any]:
    headers = {"content-type": "application/json"}
    data = {"id": 1, "jsonrpc": "2.0", "method": method, "params": params}

    response = requests.post(url=url, json=data, headers=headers)
    return response.json()


def to_block_id(
    block_hash: str | None, block_number: int | None, block_tag: models.BlockTag | None
) -> str | dict[str, str] | dict[str, int] | ErrorBlockIdMissing:
    if isinstance(block_hash, str):
        return {"block_hash": block_hash}
    elif isinstance(block_number, int):
        return {"block_number": block_number}
    elif isinstance(block_tag, models.BlockTag):
        return block_tag.name
    else:
        return ErrorBlockIdMissing()


def rpc_url(node: models.NodeName, container: Container):
    ports = container.ports

    match node:
        case models.NodeName.madara:
            port = ports[MADARA_RPC_PORT][0][DOCKER_HOST_PORT]
            return f"http://0.0.0.0:{port}"


def rpc_starknet_specVersion(url: str) -> dict[str, Any]:
    return json_rpc(url, STARKNET_SPEC_VERSION)


def rpc_starknet_getBlockWithTxHashes(
    url: str, block_id: str | dict[str, str] | dict[str, int]
) -> dict[str, Any]:
    return json_rpc(url, STARKNET_GET_BLOCK_WITH_TX_HASHES, {"block_id": block_id})


def rpc_starknet_getBlockWithTxs(
    url: str, block_id: str | dict[str, str] | dict[str, int]
) -> dict[str, Any]:
    return json_rpc(url, STARKNET_GET_BLOCK_WITH_TXS, {"block_id": block_id})


def rpc_starknet_getBlockWithReceipts(
    url: str, block_id: str | dict[str, str] | dict[str, int]
) -> dict[str, Any]:
    return json_rpc(url, STARKNET_GET_BLOCK_WITH_RECEIPTS, {"block_id": block_id})


def rpc_starknet_getStateUpdate(
    url: str, block_id: str | dict[str, str] | dict[str, int]
) -> dict[str, Any]:
    return json_rpc(url, STARKNET_GET_STATE_UPDATE, {"block_id": block_id})


def rpc_starknet_getStorageAt(
    url: str,
    contract_address: str,
    contract_key: str,
    block_id: str | dict[str, str] | dict[str, int],
) -> dict[str, Any]:
    return json_rpc(
        url,
        STARKNET_GET_STORAGE_AT,
        {
            "contract_address": contract_address,
            "key": contract_key,
            "block_id": block_id,
        },
    )


def rpc_starknet_getTransactionStatus(
    url: str, transaction_hash: str
) -> dict[str, Any]:
    return json_rpc(
        url, STARKNET_GET_TRANSACTION_STATUS, {"transaction_hash": transaction_hash}
    )


def rpc_starknet_getTransactionByHash(
    url: str, transaction_hash: str
) -> dict[str, Any]:
    return json_rpc(
        url, STARKNET_GET_TRANSACTION_BY_HASH, {"transaction_hash": transaction_hash}
    )


def rpc_starknet_getTransactionByBlockIdAndIndex(
    url: str, transaction_index: int, block_id: str | dict[str, str] | dict[str, int]
):
    return json_rpc(
        url,
        STARKNET_GET_TRANSACTION_BY_BLOCK_ID_AND_INDEX,
        {"block_id": block_id, "index": transaction_index},
    )


def rpc_starknet_getTransactionReceipt(url: str, transaction_hash: str):
    return json_rpc(
        url, STARKNET_GET_TRANSACTION_RECEIPT, {"transaction_hash": transaction_hash}
    )


def rpc_starnet_getClass(
    url: str, class_hash: str, block_id: str | dict[str, str] | dict[str, int]
):
    return json_rpc(
        url, STARKNET_GET_CLASS, {"block_id": block_id, "class_hash": class_hash}
    )
