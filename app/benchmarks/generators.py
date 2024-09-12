import asyncio
from typing import Any, AsyncGenerator

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
