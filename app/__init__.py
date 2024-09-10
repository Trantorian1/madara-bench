import logging
from typing import Annotated, Any

import docker
import fastapi
from docker.models.containers import Container

from app import error, models, rpc, stats

MADARA: str = "madara_runner"
MADARA_DB: str = "madara_runner_db"

REGEX_HEX: str = "^0x[a-fA-F0-9]+$"

ERROR_CODES: dict[int, dict[str, Any]] = {
    404: {
        "description": "The node could not be found",
        "model": error.ErrorMessage,
    },
    409: {
        "description": "Node exists but did not respond",
        "model": error.ErrorMessage,
    },
    410: {
        "description": "Node exists but is not running",
        "model": error.ErrorMessage,
    },
}


logger = logging.getLogger(__name__)
app = fastapi.FastAPI()


@app.get("/bench/cpu/{node}", responses={**ERROR_CODES})
async def node_get_cpu_normalized(node: models.NodeName):
    """Get node CPU usage.

    This is represented as a percent value normalized to the number of CPU
    cores. So, for example, 800% represents 800% of the capabilites of a single
    core, and not the entire system.
    """

    container = stats.container_get(node)
    if isinstance(container, Container):
        return stats.stats_cpu_normalized(node, container)
    else:
        return container


@app.get("/bench/cpu/system/{node}", responses={**ERROR_CODES})
async def node_get_cpu_system(node: models.NodeName):
    """Get node cpu usage.

    This is represented as a percent value of total system usage. So, for
    example, 75% represents 75% of the capabilites of the entire system.
    """

    container = stats.container_get(node)
    if isinstance(container, Container):
        return stats.stats_cpu_system(node, container)
    else:
        return container


@app.get("/bench/memory/{node}", responses={**ERROR_CODES})
async def node_get_memory(node: models.NodeName):
    """Get node memory usage.

    Fetches the amount of ram used by the node in bytes.
    """

    container = stats.container_get(node)
    if isinstance(container, Container):
        return stats.stats_memory(node, container)
    else:
        return container


@app.get("/bench/storage/{node}", responses={**ERROR_CODES})
async def node_get_storage(node: models.NodeName):
    """Returns node storage usage

    Fetches the amount of space the node database is currently taking up, in
    bytes
    """

    container = stats.container_get(node)
    if isinstance(container, Container):
        return stats.stats_storage(node, container)
    else:
        return container


@app.get("/info/docker/running", responses={**ERROR_CODES})
async def docker_get_running():
    """List all running container instances"""
    client = docker.client.from_env()
    client.containers.list()


@app.get("/info/docker/ports/{node}", responses={**ERROR_CODES})
async def docker_get_ports(node: models.NodeName):
    """List all the ports exposed by a node's container"""

    container = stats.container_get(node)
    if isinstance(container, Container):
        return container.ports
    else:
        return container


@app.get("/info/rpc/starknet_specVersion/{node}", responses={**ERROR_CODES})
async def starknet_specVersion(node: models.NodeName):
    container = stats.container_get(node)
    if isinstance(container, Container):
        url = rpc.rpc_url(node, container)
        return rpc.rpc_starknet_specVersion(url)
    else:
        return container


@app.get("/info/rpc/starknet_getBlockWithTxHashes/{node}/", responses={**ERROR_CODES})
async def starknet_getBlockWithTxHashes(
    node: models.NodeName,
    block_hash: Annotated[str | None, fastapi.Query(pattern=REGEX_HEX)] = None,
    block_numer: Annotated[int | None, fastapi.Query(ge=0)] = None,
    block_tag: models.BlockTag | None = None,
):
    container = stats.container_get(node)
    if isinstance(container, Container):
        url = rpc.rpc_url(node, container)
        if isinstance(block_hash, str):
            return rpc.rpc_starknet_getBlockWithTxHashes(
                url, {"block_hash": block_hash}
            )
        elif isinstance(block_numer, int):
            return rpc.rpc_starknet_getBlockWithTxHashes(
                url, {"block_number": block_numer}
            )
        elif isinstance(block_tag, models.BlockTag):
            return rpc.rpc_starknet_getBlockWithTxHashes(
                url,
                block_tag.name,
            )
    else:
        return container


@app.get("/info/rpc/starknet_getBlockWithTxs/{node}/", responses={**ERROR_CODES})
async def starknet_getBlockWithTxs(
    node: models.NodeName,
    block_hash: Annotated[str | None, fastapi.Query(pattern=REGEX_HEX)] = None,
    block_numer: Annotated[int | None, fastapi.Query(ge=0)] = None,
    block_tag: models.BlockTag | None = None,
):
    container = stats.container_get(node)
    if isinstance(container, Container):
        url = rpc.rpc_url(node, container)
        if isinstance(block_hash, str):
            return rpc.rpc_starknet_getBlockWithTxs(url, {"block_hash": block_hash})
        elif isinstance(block_numer, int):
            return rpc.rpc_starknet_getBlockWithTxs(url, {"block_number": block_numer})
        elif isinstance(block_tag, models.BlockTag):
            return rpc.rpc_starknet_getBlockWithTxs(
                url,
                block_tag.name,
            )
    else:
        return container


@app.get("/info/rpc/starknet_getBlockWithReceipts/{node}/", responses={**ERROR_CODES})
async def starknet_getBlockWithReceipts(
    node: models.NodeName,
    block_hash: Annotated[str | None, fastapi.Query(pattern=REGEX_HEX)] = None,
    block_numer: Annotated[int | None, fastapi.Query(ge=0)] = None,
    block_tag: models.BlockTag | None = None,
):
    container = stats.container_get(node)
    if isinstance(container, Container):
        url = rpc.rpc_url(node, container)
        if isinstance(block_hash, str):
            return rpc.rpc_starknet_getBlockWithReceipts(
                url, {"block_hash": block_hash}
            )
        elif isinstance(block_numer, int):
            return rpc.rpc_starknet_getBlockWithReceipts(
                url, {"block_number": block_numer}
            )
        elif isinstance(block_tag, models.BlockTag):
            return rpc.rpc_starknet_getBlockWithReceipts(
                url,
                block_tag.name,
            )
    else:
        return container


@app.get("/info/rpc/starknet_getStateUpdate/{node}/", responses={**ERROR_CODES})
async def starknet_getStateUpdate(
    node: models.NodeName,
    block_hash: Annotated[str | None, fastapi.Query(pattern=REGEX_HEX)] = None,
    block_numer: Annotated[int | None, fastapi.Query(ge=0)] = None,
    block_tag: models.BlockTag | None = None,
):
    container = stats.container_get(node)
    if isinstance(container, Container):
        url = rpc.rpc_url(node, container)
        if isinstance(block_hash, str):
            return rpc.rpc_starknet_getStateUpdate(url, {"block_hash": block_hash})
        elif isinstance(block_numer, int):
            return rpc.rpc_starknet_getStateUpdate(url, {"block_number": block_numer})
        elif isinstance(block_tag, models.BlockTag):
            return rpc.rpc_starknet_getStateUpdate(
                url,
                block_tag.name,
            )
    else:
        return container


@app.get("/info/rpc/starknet_getStorageAt/{node}/", responses={**ERROR_CODES})
async def starknet_getStorageAt(
    node: models.NodeName,
    contract_address: Annotated[str, fastapi.Query(pattern=REGEX_HEX)],
    contract_key: Annotated[str, fastapi.Query(pattern=REGEX_HEX)],
    block_hash: Annotated[str | None, fastapi.Query(pattern=REGEX_HEX)] = None,
    block_numer: Annotated[int | None, fastapi.Query(ge=0)] = None,
    block_tag: models.BlockTag | None = None,
):
    container = stats.container_get(node)
    if isinstance(container, Container):
        url = rpc.rpc_url(node, container)
        if isinstance(block_hash, str):
            return rpc.rpc_starknet_getStorageAt(
                url, contract_address, contract_key, {"block_hash": block_hash}
            )
        elif isinstance(block_numer, int):
            return rpc.rpc_starknet_getStorageAt(
                url, contract_address, contract_key, {"block_number": block_numer}
            )
        elif isinstance(block_tag, models.BlockTag):
            return rpc.rpc_starknet_getStorageAt(
                url,
                contract_address,
                contract_key,
                block_tag.name,
            )
    else:
        return container


@app.get("/info/rpc/starknet_getTransactionStatus/{node}/", responses={**ERROR_CODES})
async def starknet_getTransactionStatus(
    node: models.NodeName,
    transaction_hash: Annotated[str, fastapi.Query(pattern=REGEX_HEX)],
):
    container = stats.container_get(node)
    if isinstance(container, Container):
        url = rpc.rpc_url(node, container)
        return rpc.rpc_starknet_getTransactionStatus(url, transaction_hash)
    else:
        return container


@app.get("/info/rpc/starknet_getTransactionByHash/{node}/", responses={**ERROR_CODES})
async def starknet_getTransactionByHash(
    node: models.NodeName,
    transaction_hash: Annotated[str, fastapi.Query(pattern=REGEX_HEX)],
):
    container = stats.container_get(node)
    if isinstance(container, Container):
        url = rpc.rpc_url(node, container)
        return rpc.rpc_starknet_getTransactionByHash(url, transaction_hash)
    else:
        return container


@app.get(
    "/info/rpc/starknet_getTransactionByBlockIdAndIndex/{node}/",
    responses={**ERROR_CODES},
)
async def starknet_getTransactionByBlockIdAndIndex(
    node: models.NodeName,
    transaction_index: Annotated[int, fastapi.Query(ge=0)],
    block_hash: Annotated[str | None, fastapi.Query(pattern=REGEX_HEX)] = None,
    block_numer: Annotated[int | None, fastapi.Query(ge=0)] = None,
    block_tag: models.BlockTag | None = None,
):
    container = stats.container_get(node)
    if isinstance(container, Container):
        url = rpc.rpc_url(node, container)
        if isinstance(block_hash, str):
            return rpc.rpc_starknet_getTransactionByBlockIdAndIndex(
                url, transaction_index, {"block_hash": block_hash}
            )
        elif isinstance(block_numer, int):
            return rpc.rpc_starknet_getTransactionByBlockIdAndIndex(
                url, transaction_index, {"block_number": block_numer}
            )
        elif isinstance(block_tag, models.BlockTag):
            return rpc.rpc_starknet_getTransactionByBlockIdAndIndex(
                url, transaction_index, block_tag.name
            )
    else:
        return container


@app.get("/info/rpc/starknet_getTransactionReceipt/{node}/", responses={**ERROR_CODES})
async def starknet_getTransactionReceipt(
    node: models.NodeName,
    transaction_hash: Annotated[str, fastapi.Query(pattern=REGEX_HEX)],
):
    container = stats.container_get(node)
    if isinstance(container, Container):
        url = rpc.rpc_url(node, container)
        return rpc.rpc_starknet_getTransactionReceipt(url, transaction_hash)
    else:
        return container
