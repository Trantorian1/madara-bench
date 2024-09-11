import logging
from typing import Annotated, Any

import docker
import fastapi
from docker.models.containers import Container

from app import error, models, rpc, stats

MADARA: str = "madara_runner"
MADARA_DB: str = "madara_runner_db"

ERROR_CODES: dict[int, dict[str, Any]] = {
    fastapi.status.HTTP_400_BAD_REQUEST: {
        "description": "Invalid block id",
        "model": error.ErrorMessage,
    },
    fastapi.status.HTTP_404_NOT_FOUND: {
        "description": "The node could not be found",
        "model": error.ErrorMessage,
    },
    fastapi.status.HTTP_409_CONFLICT: {
        "description": "Node exists but did not respond",
        "model": error.ErrorMessage,
    },
    fastapi.status.HTTP_410_GONE: {
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


# TODO: order this alphabetically


@app.get("/info/rpc/starknet_specVersion/{node}", responses={**ERROR_CODES})
async def starknet_specVersion(node: models.NodeName):
    container = stats.container_get(node)
    if isinstance(container, Container):
        url = rpc.rpc_url(node, container)
        return rpc.rpc_starknet_specVersion(url)
    else:
        return container


@app.get(
    "/info/rpc/starknet_getBlockWithTxHashes/{node}/", responses={**ERROR_CODES}
)
async def starknet_getBlockWithTxHashes(
    node: models.NodeName,
    block_hash: models.query.BlockHash = None,
    block_number: models.query.BlockNumber = None,
    block_tag: models.query.QueryBlockTag = None,
):
    container = stats.container_get(node)
    if isinstance(container, Container):
        url = rpc.rpc_url(node, container)
        block_id = rpc.to_block_id(block_hash, block_number, block_tag)
        if isinstance(block_id, error.ErrorBlockIdMissing):
            return block_id
        else:
            return rpc.rpc_starknet_getBlockWithTxHashes(url, block_id)
    else:
        return container


@app.get(
    "/info/rpc/starknet_getBlockWithTxs/{node}/", responses={**ERROR_CODES}
)
async def starknet_getBlockWithTxs(
    node: models.NodeName,
    block_hash: models.query.BlockHash = None,
    block_number: models.query.BlockNumber = None,
    block_tag: models.query.QueryBlockTag = None,
):
    container = stats.container_get(node)
    if isinstance(container, Container):
        url = rpc.rpc_url(node, container)
        block_id = rpc.to_block_id(block_hash, block_number, block_tag)
        if isinstance(block_id, error.ErrorBlockIdMissing):
            return block_id
        else:
            return rpc.rpc_starknet_getBlockWithTxs(url, block_id)
    else:
        return container


@app.get(
    "/info/rpc/starknet_getBlockWithReceipts/{node}/", responses={**ERROR_CODES}
)
async def starknet_getBlockWithReceipts(
    node: models.NodeName,
    block_hash: models.query.BlockHash = None,
    block_number: models.query.BlockNumber = None,
    block_tag: models.query.QueryBlockTag = None,
):
    container = stats.container_get(node)
    if isinstance(container, Container):
        url = rpc.rpc_url(node, container)
        block_id = rpc.to_block_id(block_hash, block_number, block_tag)
        if isinstance(block_id, error.ErrorBlockIdMissing):
            return block_id
        else:
            return rpc.rpc_starknet_getBlockWithReceipts(url, block_id)
    else:
        return container


@app.get("/info/rpc/starknet_getStateUpdate/{node}/", responses={**ERROR_CODES})
async def starknet_getStateUpdate(
    node: models.NodeName,
    block_hash: models.query.BlockHash = None,
    block_number: models.query.BlockNumber = None,
    block_tag: models.query.QueryBlockTag = None,
):
    container = stats.container_get(node)
    if isinstance(container, Container):
        url = rpc.rpc_url(node, container)
        block_id = rpc.to_block_id(block_hash, block_number, block_tag)
        if isinstance(block_id, error.ErrorBlockIdMissing):
            return block_id
        else:
            return rpc.rpc_starknet_getStateUpdate(url, block_id)
    else:
        return container


@app.get("/info/rpc/starknet_getStorageAt/{node}/", responses={**ERROR_CODES})
async def starknet_getStorageAt(
    node: models.NodeName,
    contract_address: models.query.ContractAddress,
    contract_key: models.query.ContractKey,
    block_hash: models.query.BlockHash = None,
    block_number: models.query.BlockNumber = None,
    block_tag: models.query.QueryBlockTag = None,
):
    container = stats.container_get(node)
    if isinstance(container, Container):
        url = rpc.rpc_url(node, container)
        block_id = rpc.to_block_id(block_hash, block_number, block_tag)
        if isinstance(block_id, error.ErrorBlockIdMissing):
            return block_id
        else:
            return rpc.rpc_starknet_getStorageAt(
                url, contract_address, contract_key, block_id
            )
    else:
        return container


@app.get(
    "/info/rpc/starknet_getTransactionStatus/{node}/", responses={**ERROR_CODES}
)
async def starknet_getTransactionStatus(
    node: models.NodeName,
    transaction_hash: models.query.TxHash,
):
    container = stats.container_get(node)
    if isinstance(container, Container):
        url = rpc.rpc_url(node, container)
        return rpc.rpc_starknet_getTransactionStatus(url, transaction_hash)
    else:
        return container


@app.get(
    "/info/rpc/starknet_getTransactionByHash/{node}/", responses={**ERROR_CODES}
)
async def starknet_getTransactionByHash(
    node: models.NodeName,
    transaction_hash: models.query.TxHash,
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
    transaction_index: models.query.TxIndex,
    block_hash: models.query.BlockHash = None,
    block_number: models.query.BlockNumber = None,
    block_tag: models.query.QueryBlockTag = None,
):
    container = stats.container_get(node)
    if isinstance(container, Container):
        url = rpc.rpc_url(node, container)
        block_id = rpc.to_block_id(block_hash, block_number, block_tag)
        if isinstance(block_id, error.ErrorBlockIdMissing):
            return block_id
        else:
            return rpc.rpc_starknet_getTransactionByBlockIdAndIndex(
                url, transaction_index, block_id
            )
    else:
        return container


@app.get(
    "/info/rpc/starknet_getTransactionReceipt/{node}/",
    responses={**ERROR_CODES},
)
async def starknet_getTransactionReceipt(
    node: models.NodeName,
    transaction_hash: models.query.TxHash,
):
    container = stats.container_get(node)
    if isinstance(container, Container):
        url = rpc.rpc_url(node, container)
        return rpc.rpc_starknet_getTransactionReceipt(url, transaction_hash)
    else:
        return container


@app.get("/info/rpc/starknet_getClass/{node}/", responses={**ERROR_CODES})
async def starknet_getClass(
    node: models.NodeName,
    class_hash: models.query.ClassHash,
    block_hash: models.query.BlockHash = None,
    block_number: models.query.BlockNumber = None,
    block_tag: models.query.QueryBlockTag = None,
):
    container = stats.container_get(node)
    if isinstance(container, Container):
        url = rpc.rpc_url(node, container)
        block_id = rpc.to_block_id(block_hash, block_number, block_tag)
        if isinstance(block_id, error.ErrorBlockIdMissing):
            return block_id
        else:
            return rpc.rpc_starnet_getClass(url, class_hash, block_id)
    else:
        return container


@app.get("/info/rpc/starknet_getClassHashAt/{node}/", responses={**ERROR_CODES})
async def starknet_getClassHashAt(
    node: models.NodeName,
    contract_address: models.query.ContractAddress,
    block_hash: models.query.BlockHash = None,
    block_number: models.query.BlockNumber = None,
    block_tag: models.query.QueryBlockTag = None,
):
    container = stats.container_get(node)
    if isinstance(container, Container):
        url = rpc.rpc_url(node, container)
        block_id = rpc.to_block_id(block_hash, block_number, block_tag)
        if isinstance(block_id, error.ErrorBlockIdMissing):
            return block_id
        else:
            return rpc.rpc_starknet_getClassHashAt(
                url, contract_address, block_id
            )
    else:
        return container


@app.get("/info/rpc/starknet_getClassAt/{node}/", responses={**ERROR_CODES})
async def starknet_getClassAt(
    node: models.NodeName,
    contract_address: models.query.ContractAddress,
    block_hash: models.query.BlockHash = None,
    block_number: models.query.BlockNumber = None,
    block_tag: models.query.QueryBlockTag = None,
):
    container = stats.container_get(node)
    if isinstance(container, Container):
        url = rpc.rpc_url(node, container)
        block_id = rpc.to_block_id(block_hash, block_number, block_tag)
        if isinstance(block_id, error.ErrorBlockIdMissing):
            return block_id
        else:
            return rpc.rpc_starknet_getClassAt(url, contract_address, block_id)
    else:
        return container


@app.get(
    "/info/rpc/starknet_getBlockTransactionCount/{node}/",
    responses={**ERROR_CODES},
)
async def starknet_getBlockTransactionCount(
    node: models.NodeName,
    block_hash: models.query.BlockHash = None,
    block_number: models.query.BlockNumber = None,
    block_tag: models.query.QueryBlockTag = None,
):
    container = stats.container_get(node)
    if isinstance(container, Container):
        url = rpc.rpc_url(node, container)
        block_id = rpc.to_block_id(block_hash, block_number, block_tag)
        if isinstance(block_id, error.ErrorBlockIdMissing):
            return block_id
        else:
            return rpc.rpc_starknet_getBlockTransactionCount(url, block_id)
    else:
        return container


@app.post("/info/rpc/starknet_call/{node}", responses={**ERROR_CODES})
async def starknet_call(
    node: models.NodeName,
    request: models.body.Call,
    block_hash: models.query.BlockHash = None,
    block_number: models.query.BlockNumber = None,
    block_tag: models.query.QueryBlockTag = None,
):
    container = stats.container_get(node)
    if isinstance(container, Container):
        url = rpc.rpc_url(node, container)
        block_id = rpc.to_block_id(block_hash, block_number, block_tag)
        if isinstance(block_id, error.ErrorBlockIdMissing):
            return block_id
        else:
            return rpc.rpc_starknet_call(url, request, block_id)
    else:
        return container


@app.post("/info/rpc/starknet_estimeFee/{node}", responses={**ERROR_CODES})
async def starknet_estimateFee(
    node: models.NodeName,
    body: models.body.EstimateFee,
    block_hash: models.query.BlockHash = None,
    block_number: models.query.BlockNumber = None,
    block_tag: models.query.QueryBlockTag = None,
):
    container = stats.container_get(node)
    if isinstance(container, Container):
        url = rpc.rpc_url(node, container)
        block_id = rpc.to_block_id(block_hash, block_number, block_tag)
        if isinstance(block_id, error.ErrorBlockIdMissing):
            return block_id
        else:
            return rpc.rpc_starknet_estimateFee(url, body, block_id)
    else:
        return container


@app.post(
    "/info/rpc/starknet_estimateMessageFee/{node}", responses={**ERROR_CODES}
)
async def starknet_estimateMessageFee(
    node: models.NodeName,
    body: models.body.EstimateMessageFee,
    block_hash: models.query.BlockHash = None,
    block_number: models.query.BlockNumber = None,
    block_tag: models.query.QueryBlockTag = None,
):
    container = stats.container_get(node)
    if isinstance(container, Container):
        url = rpc.rpc_url(node, container)
        block_id = rpc.to_block_id(block_hash, block_number, block_tag)
        if isinstance(block_id, error.ErrorBlockIdMissing):
            return block_id
        else:
            return rpc.rpc_starknet_estimateMessageFee(url, body, block_id)
    else:
        return container


@app.get("/info/rpc/starknet_chainId/{node}", responses={**ERROR_CODES})
async def starknet_chainId(node: models.NodeName):
    container = stats.container_get(node)
    if isinstance(container, Container):
        url = rpc.rpc_url(node, container)
        return rpc.rpc_starknet_chainId(url)
    else:
        return container


@app.get("/info/rpc/starknet_syncing/{node}", responses={**ERROR_CODES})
async def starknet_syncing(node: models.NodeName):
    container = stats.container_get(node)
    if isinstance(container, Container):
        url = rpc.rpc_url(node, container)
        return rpc.rpc_starknet_syncing(url)
    else:
        return container


@app.post("/info/rpc/starknet_getEvents/{node}", responses={**ERROR_CODES})
async def starknet_getEvents(
    node: models.NodeName,
    body: models.body.GetEvents,
):
    container = stats.container_get(node)
    if isinstance(container, Container):
        url = rpc.rpc_url(node, container)
        return rpc.rcp_starknet_getEvents(url, body)
    else:
        return container


@app.get("/info/rpc/starknet_getNonce/{node}/", responses={**ERROR_CODES})
async def starknet_getNonce(
    node: models.NodeName,
    contract_address: models.query.ContractAddress,
    block_hash: models.query.BlockHash = None,
    block_number: models.query.BlockNumber = None,
    block_tag: models.query.QueryBlockTag = None,
):
    container = stats.container_get(node)
    if isinstance(container, Container):
        url = rpc.rpc_url(node, container)
        block_id = rpc.to_block_id(block_hash, block_number, block_tag)
        if isinstance(block_id, error.ErrorBlockIdMissing):
            return block_id
        else:
            return rpc.rpc_starknet_getNonce(url, contract_address, block_id)
    else:
        return container


@app.post(
    "/info/rpc/starknet_simulateTransactions/{node}/",
    responses={**ERROR_CODES},
)
async def starknet_simulateTransactions(
    node: models.NodeName,
    body: models.body.SimulateTransactions,
    block_hash: models.query.BlockHash = None,
    block_number: models.query.BlockNumber = None,
    block_tag: models.query.QueryBlockTag = None,
):
    container = stats.container_get(node)
    if isinstance(container, Container):
        url = rpc.rpc_url(node, container)
        block_id = rpc.to_block_id(block_hash, block_number, block_tag)
        if isinstance(block_id, error.ErrorBlockIdMissing):
            return block_id
        else:
            return rpc.rpc_starknet_simulateTransactions(url, body, block_id)
    else:
        return container


@app.post(
    "/info/rpc/starknet_traceBlockTransactions/{node}/",
    responses={**ERROR_CODES},
)
async def starknet_traceBlockTransactions(
    node: models.NodeName,
    block_hash: models.query.BlockHash = None,
    block_number: models.query.BlockNumber = None,
    block_tag: models.query.QueryBlockTag = None,
):
    container = stats.container_get(node)
    if isinstance(container, Container):
        url = rpc.rpc_url(node, container)
        block_id = rpc.to_block_id(block_hash, block_number, block_tag)
        if isinstance(block_id, error.ErrorBlockIdMissing):
            return block_id
        else:
            return rpc.rpc_starknet_traceBlockTransactions(url, block_id)
    else:
        return container


@app.post(
    "/info/rpc/starknet_traceTransaction/{node}/",
    responses={**ERROR_CODES},
)
async def starknet_traceTransaction(
    node: models.NodeName,
    transaction_hash: models.query.TxHash,
):
    container = stats.container_get(node)
    if isinstance(container, Container):
        url = rpc.rpc_url(node, container)
        return rpc.rpc_starknet_traceTransaction(url, transaction_hash)
    else:
        return container


@app.post(
    "/info/rpc/starknet_addDeclareTransaction/{node}/",
    responses={**ERROR_CODES},
)
async def starknet_addDeclareTransaction(
    node: models.NodeName, declare_transaction: models.body.TxDeclare
):
    container = stats.container_get(node)
    if isinstance(container, Container):
        url = rpc.rpc_url(node, container)
        return rpc.rpc_starknet_addDeclareTransaction(url, declare_transaction)
    else:
        return container


@app.post(
    "/info/rpc/starknet_addDeployAccountTransaction/{node}/",
    responses={**ERROR_CODES},
)
async def starknet_addDeployAccountTransaction(
    node: models.NodeName, deploy_account_transaction: models.body.TxDeploy
):
    container = stats.container_get(node)
    if isinstance(container, Container):
        url = rpc.rpc_url(node, container)
        return rpc.rpc_starknet_addDeplyAccountTransaction(
            url, deploy_account_transaction
        )
    else:
        return container


@app.post(
    "/info/rpc/starknet_addInvokeTransaction/{node}/",
    responses={**ERROR_CODES},
)
async def starknet_addInvokeTransaction(
    node: models.NodeName, invoke_transaction: models.body.TxInvoke
):
    container = stats.container_get(node)
    if isinstance(container, Container):
        url = rpc.rpc_url(node, container)
        return rpc.rpc_starknetAddInvokeTransaction(url, invoke_transaction)
    else:
        return container
