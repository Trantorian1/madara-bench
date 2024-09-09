import logging

import docker
import fastapi
from stats import (NodeName, container_get, stats_cpu_normalized,
                   stats_cpu_system, stats_memory)

MADARA: str = "madara_runner"

logger = logging.getLogger(__name__)
app = fastapi.FastAPI()



@app.get("/bench/cpu/normalized{node}")
async def node_get_cpu_normalized(node: NodeName) -> float:
    """Get node CPU usage.

    This is represented as a percent value normalized to the number of CPU
    cores. So, for example, 800% represents 800% of the capabilites of a single
    core, and not the entire system.

    Args:
        node: the node to inspect.

    Raises:
        HTTPException: 404 if the node cannot be found,
        409 if the node exists but does not respond.

    Returns:
        % of CPU used by the node, relative to the number of CPU cores.
    """

    return stats_cpu_normalized(container_get(node))

@app.get("/bench/cpu/system/{node}")
async def node_get_cpu_system(node: NodeName) -> float:
    """Get node cpu usage.

    This is represented as a percent value of total system usage. So, for 
    example, 75% represents 75% of the capabilites of the entire system.

    Args:
        node: the node to inspect.

    Raises:
        HTTPException: 404 if the node cannot be found,
        409 if the node exists but does not respond.

    Returns:
        % of CPU used by the node, relative to the system.
    """

    return stats_cpu_system(container_get(node))


@app.get("/bench/memory/{node}")
async def node_get_memory(node: NodeName) -> int:
    """Get node memory usage.

    Args:
        node: the node to inspect.

    Raises:
        HTTPException: 404 if the node cannot be found,
        409 if the node exists but does not respond.

    Returns:
        Amount of ram used by the node, in bytes.
    """

    return stats_memory(container_get(node))


@app.get("/bench/storage/{node}")
async def node_get_storage(node: NodeName):
    """Returns node storage usage

    Args:
        node: the node to inspect
    """
    pass


@app.get("/info/docker/running")
async def docker_get_running():
    """List all running container instances"""
    client = docker.client.from_env()
    client.containers.list()



if __name__ == "__main__":
    import uvicorn

    logging.basicConfig(filename="debug.log", level=logging.INFO)

    client = docker.client.from_env()
    madara = client.containers.get("madara_runner")
    stats = madara.stats(stream=False)
    print(stats)

    uvicorn.run(app, host="0.0.0.0", port=8000)
