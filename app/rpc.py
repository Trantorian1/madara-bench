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
STARKNET_GET_CLASS_HASH_AT: str = "starknet_getClassHashAt"
STARKNET_GET_CLASS_AT: str = "starknet_getClassAt"
STARKNET_GET_BLOCK_TRANSACTION_COUNT: str = "starknet_getBlockTransactionCount"
STARKNET_CALL: str = "starknet_call"
STARKNET_ESTIMATE_FEE: str = "starknet_estimateFee"
STARKNET_ESTIMATE_MESSAGE_FEE: str = "starknet_estimateMessageFee"
STARKNET_CHAIN_ID: str = "starknet_chainId"
STARKNET_SYNCING: str = "starknet_syncing"
STARKNET_GET_EVENTS: str = "starknet_getEvents"
STARKNET_GET_NONCE: str = "starknet_getNonce"

# Trace API
STARKNET_SIMULATE_TRANSACTIONS: str = "starknet_simulateTransactions"
STARKNET_TRACE_BLOCK_TRANSACTIONS: str = "starknet_traceBlockTransactions"
STARKNET_TRACE_TRANSACTION: str = "starknet_traceTransaction"

# ADD API
STARKNET_ADD_DECLARE_TRANSACTION: str = "starknet_addDeclareTransaction"
STARKNET_ADD_DEPLOY_ACCOUNT_TRANSACTION: str = (
    "starknet_addDeployAccountTransaction"
)


def json_rpc(
    url: str, method: str, params: dict[str, Any] | list[Any] = {}
) -> dict[str, Any]:
    headers = {"content-type": "application/json"}
    data = {"id": 1, "jsonrpc": "2.0", "method": method, "params": params}

    response = requests.post(url=url, json=data, headers=headers)
    return response.json()


def to_block_id(
    block_hash: str | None,
    block_number: int | None,
    block_tag: models.BlockTag | None,
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
    return json_rpc(
        url, STARKNET_GET_BLOCK_WITH_TX_HASHES, {"block_id": block_id}
    )


def rpc_starknet_getBlockWithTxs(
    url: str, block_id: str | dict[str, str] | dict[str, int]
) -> dict[str, Any]:
    return json_rpc(url, STARKNET_GET_BLOCK_WITH_TXS, {"block_id": block_id})


def rpc_starknet_getBlockWithReceipts(
    url: str, block_id: str | dict[str, str] | dict[str, int]
) -> dict[str, Any]:
    return json_rpc(
        url, STARKNET_GET_BLOCK_WITH_RECEIPTS, {"block_id": block_id}
    )


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
        url,
        STARKNET_GET_TRANSACTION_STATUS,
        {"transaction_hash": transaction_hash},
    )


def rpc_starknet_getTransactionByHash(
    url: str, transaction_hash: str
) -> dict[str, Any]:
    return json_rpc(
        url,
        STARKNET_GET_TRANSACTION_BY_HASH,
        {"transaction_hash": transaction_hash},
    )


def rpc_starknet_getTransactionByBlockIdAndIndex(
    url: str,
    transaction_index: int,
    block_id: str | dict[str, str] | dict[str, int],
) -> dict[str, Any]:
    return json_rpc(
        url,
        STARKNET_GET_TRANSACTION_BY_BLOCK_ID_AND_INDEX,
        {"block_id": block_id, "index": transaction_index},
    )


def rpc_starknet_getTransactionReceipt(
    url: str, transaction_hash: str
) -> dict[str, Any]:
    return json_rpc(
        url,
        STARKNET_GET_TRANSACTION_RECEIPT,
        {"transaction_hash": transaction_hash},
    )


def rpc_starnet_getClass(
    url: str, class_hash: str, block_id: str | dict[str, str] | dict[str, int]
) -> dict[str, Any]:
    return json_rpc(
        url,
        STARKNET_GET_CLASS,
        {"block_id": block_id, "class_hash": class_hash},
    )


def rpc_starknet_getClassHashAt(
    url: str,
    contract_address: str,
    block_id: str | dict[str, str] | dict[str, int],
) -> dict[str, Any]:
    return json_rpc(
        url,
        STARKNET_GET_CLASS_HASH_AT,
        {"block_id": block_id, "contract_address": contract_address},
    )


def rpc_starknet_getClassAt(
    url: str,
    contract_address: str,
    block_id: str | dict[str, str] | dict[str, int],
) -> dict[str, Any]:
    return json_rpc(
        url,
        STARKNET_GET_CLASS_AT,
        {"block_id": block_id, "contract_address": contract_address},
    )


def rpc_starknet_getBlockTransactionCount(
    url: str, block_id: str | dict[str, str] | dict[str, int]
) -> dict[str, Any]:
    return json_rpc(
        url, STARKNET_GET_BLOCK_TRANSACTION_COUNT, {"block_id": block_id}
    )


def rpc_starknet_call(
    url: str,
    request: models.body.Call,
    block_id: str | dict[str, str] | dict[str, int],
) -> dict[str, Any]:
    return json_rpc(
        url, STARKNET_CALL, {"request": vars(request), "block_id": block_id}
    )


def rpc_starknet_estimateFee(
    url: str,
    body: models.body.EstimateFee,
    block_id: str | dict[str, str] | dict[str, int],
) -> dict[str, Any]:
    return json_rpc(
        url,
        STARKNET_ESTIMATE_FEE,
        {
            "request": body.request,
            "simulation_flags": body.simulation_flags,
            "block_id": block_id,
        },
    )


def rpc_starknet_estimateMessageFee(
    url: str,
    body: models.body.EstimateMessageFee,
    block_id: str | dict[str, str] | dict[str, int],
) -> dict[str, Any]:
    return json_rpc(
        url,
        STARKNET_ESTIMATE_MESSAGE_FEE,
        {
            "from_address": body.from_address,
            "to_address": body.to_address,
            "entry_point_selector": body.entry_point_selector,
            "payload": body.payload,
            "block_id": block_id,
        },
    )


def rpc_starknet_chainId(url: str) -> dict[str, Any]:
    return json_rpc(url, STARKNET_CHAIN_ID)


def rpc_starknet_syncing(url: str) -> dict[str, Any]:
    return json_rpc(url, STARKNET_SYNCING)


def rcp_starknet_getEvents(
    url: str, body: models.body.GetEvents
) -> dict[str, Any]:
    return json_rpc(url, STARKNET_GET_EVENTS, {"filter": body})


def rpc_starknet_getNonce(
    url: str,
    contract_address: models.query.ContractAddress,
    block_id: str | dict[str, str] | dict[str, int],
) -> dict[str, Any]:
    return json_rpc(
        url,
        STARKNET_GET_NONCE,
        {"block_id": block_id, "contract_address": contract_address},
    )


def rpc_starknet_simulateTransactions(
    url: str,
    body: models.body.SimulateTransactions,
    block_id: str | dict[str, str] | dict[str, int],
):
    return json_rpc(
        url,
        STARKNET_SIMULATE_TRANSACTIONS,
        {
            "block_id": block_id,
            "transactions": body.transactions,
            "simulation_flags": body.simulation_flags,
        },
    )


def rpc_starknet_traceBlockTransactions(
    url: str,
    block_id: str | dict[str, str] | dict[str, int],
) -> dict[str, Any]:
    return json_rpc(
        url, STARKNET_TRACE_BLOCK_TRANSACTIONS, {"block_id": block_id}
    )


def rpc_starknet_traceTransaction(
    url: str, transaction_hash: models.query.TxHash
) -> dict[str, Any]:
    return json_rpc(
        url,
        STARKNET_TRACE_TRANSACTION,
        {"transaction_hash": transaction_hash},
    )


def rpc_starknet_addDeclareTransaction(
    url: str, declare_transaction: models.body.TxDeclare
) -> dict[str, Any]:
    return json_rpc(
        url,
        STARKNET_ADD_DECLARE_TRANSACTION,
        {"declare_transaction": declare_transaction},
    )


def rpc_starknet_addDeplyAccountTransaction(
    url: str, deploy_account_transaction: models.body.TxDeploy
) -> dict[str, Any]:
    return json_rpc(
        url,
        STARKNET_ADD_DEPLOY_ACCOUNT_TRANSACTION,
        {"deploy_account_transaction": deploy_account_transaction},
    )
