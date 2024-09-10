import json
from typing import Any

import requests
from docker.models.containers import Container

from app import stats

MADARA_RPC_PORT: str = "9944/tcp"
DOCKER_HOST_PORT: str = "HostPort"

STARKNET_SPECVERSION: str = "starknet_specVersion"


def json_rpc(url: str, method: str, params: list[Any] = []) -> dict[str, Any]:
    headers = {"content-type": "application/json"}
    data = {"id": 1, "jsonrpc": "2.0", "method": method, "params": params}

    response = requests.post(url=url, json=data, headers=headers)
    return response.json()


def rpc_starknet_specVersion(url: str):
    return json_rpc(url, STARKNET_SPECVERSION)


def rpc_url(node: stats.NodeName, container: Container):
    ports = container.ports

    match node:
        case stats.NodeName.madara:
            port = ports[MADARA_RPC_PORT][0][DOCKER_HOST_PORT]
            return f"http://0.0.0.0:{port}"
