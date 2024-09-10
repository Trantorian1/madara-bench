import json
from typing import Any

import requests
from docker.models.containers import Container

from app import models

MADARA_RPC_PORT: str = "9944/tcp"
DOCKER_HOST_PORT: str = "HostPort"

STARKNET_SPECVERSION: str = "starknet_specVersion"
STARKNET_GETBLOCKWITHTXHASHES: str = "starknet_getBlockWithTxHashes"
STARKNET_GETBLOCKWITHTXS: str = "starknet_getBlockWithTxs"
STARKNET_GETBLOCKWITHRECEIPTS: str = "starknet_getBlockWithReceipts"
STARKNET_GETSTATEUPDATE: str = "starknet_getStateUpdate"
STARKNET_GETSTORAGEAT: str = "starknet_getStorageAt"


def json_rpc(
    url: str, method: str, params: dict[str, Any] | list[Any] = {}
) -> dict[str, Any]:
    headers = {"content-type": "application/json"}
    data = {"id": 1, "jsonrpc": "2.0", "method": method, "params": params}

    response = requests.post(url=url, json=data, headers=headers)
    return response.json()


def rpc_url(node: models.NodeName, container: Container):
    ports = container.ports

    match node:
        case models.NodeName.madara:
            port = ports[MADARA_RPC_PORT][0][DOCKER_HOST_PORT]
            return f"http://0.0.0.0:{port}"


def rpc_starknet_specVersion(url: str) -> dict[str, Any]:
    return json_rpc(url, STARKNET_SPECVERSION)


def rpc_starknet_getBlockWithTxHashes(
    url: str, block_id: str | dict[str, str] | dict[str, int]
) -> dict[str, Any]:
    return json_rpc(url, STARKNET_GETBLOCKWITHTXHASHES, {"block_id": block_id})


def rpc_starknet_getBlockWithTxs(
    url: str, block_id: str | dict[str, str] | dict[str, int]
) -> dict[str, Any]:
    return json_rpc(url, STARKNET_GETBLOCKWITHTXS, {"block_id": block_id})


def rpc_starknet_getBlockWithReceipts(
    url: str, block_id: str | dict[str, str] | dict[str, int]
) -> dict[str, Any]:
    return json_rpc(url, STARKNET_GETBLOCKWITHRECEIPTS, {"block_id": block_id})


def rpc_starknet_getStateUpdate(
    url: str, block_id: str | dict[str, str] | dict[str, int]
) -> dict[str, Any]:
    return json_rpc(url, STARKNET_GETSTATEUPDATE, {"block_id": block_id})


def rpc_starknet_getStorageAt(
    url: str,
    contract_address: str,
    contract_key: str,
    block_id: str | dict[str, str] | dict[str, int],
) -> dict[str, Any]:
    return json_rpc(
        url,
        STARKNET_GETSTORAGEAT,
        {
            "contract_address": contract_address,
            "key": contract_key,
            "block_id": block_id,
        },
    )
