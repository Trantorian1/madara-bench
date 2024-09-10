from enum import Enum

import docker
import fastapi
from docker import errors as docker_errors
from docker.models.containers import Container
from pydantic import BaseModel


class NodeName(str, Enum):
    madara = "madara"


class ErrorMessage(BaseModel):
    message: str


class ErrorNodeNotFound(fastapi.responses.JSONResponse):
    def __init__(self, node: NodeName) -> None:
        super().__init__(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            content={
                "message": f"{node.capitalize()} node not found, it might not be running or have a different name"
            },
        )


class ErrorNodeSilent(fastapi.responses.JSONResponse):
    def __init__(self, node: NodeName) -> None:
        super().__init__(
            status_code=fastapi.status.HTTP_409_CONFLICT,
            content={
                "message": f"Failed to query {node.name.capitalize()} node docker, something is seriously wrong"
            },
        )


class ErrorNodeNotRunning(fastapi.responses.JSONResponse):
    def __init__(self, node: NodeName) -> None:
        super().__init__(
            status_code=fastapi.status.HTTP_410_GONE,
            content={
                "message": f"{node.name.capitalize()} node container is no longer running"
            },
        )


def container_get(node: NodeName) -> Container | fastapi.responses.JSONResponse:
    try:
        client = docker.client.from_env()
        return client.containers.get(node + "_runner")

    except docker_errors.NotFound:
        return ErrorNodeNotFound(node)
    except docker_errors.APIError:
        return ErrorNodeSilent(node)


# As explained in https://github.com/moby/moby/issues/26711
def stats_cpu_normalized(node: NodeName, container: Container) -> float | fastapi.responses.JSONResponse:
    if container.status != "running":
        return ErrorNodeNotRunning(node)

    stats = container.stats(stream=False)

    cpu_delta: int = (
        stats["cpu_stats"]["cpu_usage"]["total_usage"]
        - stats["precpu_stats"]["cpu_usage"]["total_usage"]
    )
    cpu_count: int = stats["cpu_stats"]["online_cpus"]
    system_delta: int = (
        stats["cpu_stats"]["system_cpu_usage"]
        - stats["precpu_stats"]["system_cpu_usage"]
    )

    if system_delta > 0:
        return (float(cpu_delta) / float(system_delta)) * float(cpu_count) * 100.0
    else:
        return 0.0

def stats_cpu_system(node: NodeName, container: Container) -> float | fastapi.responses.JSONResponse:
    if container.status != "running":
        return ErrorNodeNotRunning(node)

    stats = container.stats(stream=False)

    cpu_delta: int = (
        stats["cpu_stats"]["cpu_usage"]["total_usage"]
        - stats["precpu_stats"]["cpu_usage"]["total_usage"]
    )
    system_delta: int = (
        stats["cpu_stats"]["system_cpu_usage"]
        - stats["precpu_stats"]["system_cpu_usage"]
    )

    if system_delta > 0:
        return (float(cpu_delta) / float(system_delta)) * 100.0
    else:
        return 0.0


def stats_memory(node: NodeName, container: Container) -> int | fastapi.responses.JSONResponse:
    if container.status != "running":
        return ErrorNodeNotRunning(node)

    stats = container.stats(stream=False)
    return stats["memory_stats"]["usage"]

def stats_storage(node: NodeName, container: Container) -> int | fastapi.responses.JSONResponse:
    if container.status != "running":
        return ErrorNodeNotRunning(node)

    try:
        result = container.exec_run(["du", "-sb", "/data"])
        stdin: str = result.output.decode('utf8')
        test = stdin.removesuffix("\t/data\n")
        return int(test)

    except docker_errors.APIError:
        return ErrorNodeSilent(node)
