import logging

import docker
import fastapi
from docker.models.containers import Container

from app import stats

MADARA: str = "madara_runner"
MADARA_DB: str = "madara_runner_db"

logger = logging.getLogger(__name__)
app = fastapi.FastAPI()



@app.get("/bench/cpu/{node}", responses={
    404: { 
        "description": "The node could not be found",
        "content": {
            "application/json": {
                "example": {
                    "message": "string"
                }
            }
        }
    },
    409: {
        "description": "Node exists but did not respond",
        "content": {
            "application/json": {
                "example": {
                    "message": "string"
                }
            }
        }
    },
    410: {
        "description": "Node exists but is not running",
        "content": {
            "application/json": {
                "example": {
                    "message": "string"
                }
            }
        }
    },
})
async def node_get_cpu_normalized(node: stats.NodeName):
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


@app.get("/bench/cpu/system/{node}", responses={
    404: { 
        "description": "The node could not be found",
        "content": {
            "application/json": {
                "example": {
                    "message": "string"
                }
            }
        }
    },
    409: {
        "description": "Node exists but did not respond",
        "content": {
            "application/json": {
                "example": {
                    "message": "string"
                }
            }
        }
    },
    410: {
        "description": "Node exists but is not running",
        "content": {
            "application/json": {
                "example": {
                    "message": "string"
                }
            }
        }
    },
})
async def node_get_cpu_system(node: stats.NodeName):
    """Get node cpu usage.

    This is represented as a percent value of total system usage. So, for 
    example, 75% represents 75% of the capabilites of the entire system.
    """

    container = stats.container_get(node)
    if isinstance(container, Container):
        return stats.stats_cpu_system(node, container)
    else:
        return container


@app.get("/bench/memory/{node}", responses={
    404: { 
        "description": "The node could not be found",
        "content": {
            "application/json": {
                "example": {
                    "message": "string"
                }
            }
        }
    },
    409: {
        "description": "Node exists but did not respond",
        "content": {
            "application/json": {
                "example": {
                    "message": "string"
                }
            }
        }
    },
    410: {
        "description": "Node exists but is not running",
        "content": {
            "application/json": {
                "example": {
                    "message": "string"
                }
            }
        }
    },
})
async def node_get_memory(node: stats.NodeName):
    """Get node memory usage.

    Fetches the amount of ram used by the node in bytes.
    """

    container = stats.container_get(node)
    if isinstance(container, Container):
        return stats.stats_memory(node, container)
    else:
        return container


@app.get("/bench/storage/{node}", responses={
    404: { 
        "description": "The node could not be found",
        "content": {
            "application/json": {
                "example": {
                    "message": "string"
                }
            }
        }
    },
    409: {
        "description": "Node exists but did not respond",
        "content": {
            "application/json": {
                "example": {
                    "message": "string"
                }
            }
        }
    },
    410: {
        "description": "Node exists but is not running",
        "content": {
            "application/json": {
                "example": {
                    "message": "string"
                }
            }
        }
    },
})
async def node_get_storage(node: stats.NodeName):
    """Returns node storage usage

    Fetches the amount of space the node database is currently taking up, in
    bytes
    """

    container = stats.container_get(node)
    if isinstance(container, Container):
        return stats.stats_storage(node, container)
    else:
        return container


@app.get("/info/docker/running")
async def docker_get_running():
    """List all running container instances"""
    client = docker.client.from_env()
    client.containers.list()

