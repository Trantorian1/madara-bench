import asyncio
import random
from typing import Any, AsyncGenerator

from starknet_py.net.full_node_client import FullNodeClient

from app import rpc

InputGenerator = AsyncGenerator[dict[str, Any], Any]


def latest_common_block_number(urls: list[str]) -> int:
    block_numbers: list[int] = [
        rpc.rpc_starknet_blockNumber(url).output["result"] for url in urls
    ]

    return min(block_numbers)


async def gen_starknet_getBlockWithTxs(
    urls: list[str],
    interval: float,
) -> InputGenerator:
    while True:
        yield {
            "block_id": rpc.to_block_id(
                block_number=latest_common_block_number(urls)
            )
        }
        await asyncio.sleep(interval)


async def gen_starknet_get_storage_at(
    urls: list[str], interval: float
) -> InputGenerator:
    """Generates a ramdom contract storage key

    Key is taken from the state diffs over the last 100 common blocks. It is
    possible for a key to be generated that falls before that range in some
    rare cases where the random block to have been chose had no storage diffs
    """
    client = FullNodeClient(node_url=urls[0])

    while True:
        block_number = latest_common_block_number(urls)
        block_number = random.randrange(block_number - 100, block_number)
        state_update = await client.get_state_update(block_number=block_number)

        while len(state_update.state_diff.storage_diffs) == 0:
            # This is safe since block 0 has storage diffs
            block_number -= 1
            state_update = await client.get_state_update(block_number)

        storage_diff = state_update.state_diff.storage_diffs[0]
        storage_entry = storage_diff.storage_entries[0]
        yield {
            "contract_address": storage_diff.address,
            "contract_key": storage_entry.key,
            "block_id": rpc.to_block_id(block_number=block_number),
        }
        await asyncio.sleep(interval)
