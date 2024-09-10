from enum import Enum

import docker
import fastapi
from docker import errors as docker_errors
from docker.models.containers import Container

from app import error, models


def container_get(node: models.NodeName) -> Container | fastapi.responses.JSONResponse:
    try:
        client = docker.client.from_env()
        return client.containers.get(node + "_runner")

    except docker_errors.NotFound:
        return error.ErrorNodeNotFound(node)
    except docker_errors.APIError:
        return error.ErrorNodeSilent(node)


# As explained in https://github.com/moby/moby/issues/26711
def stats_cpu_normalized(
    node: models.NodeName, container: Container
) -> float | fastapi.responses.JSONResponse:
    if container.status != "running":
        return error.ErrorNodeNotRunning(node)

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


def stats_cpu_system(
    node: models.NodeName, container: Container
) -> float | fastapi.responses.JSONResponse:
    if container.status != "running":
        return error.ErrorNodeNotRunning(node)

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


def stats_memory(
    node: models.NodeName, container: Container
) -> int | fastapi.responses.JSONResponse:
    if container.status != "running":
        return error.ErrorNodeNotRunning(node)

    stats = container.stats(stream=False)
    return stats["memory_stats"]["usage"]


def stats_storage(
    node: models.NodeName, container: Container
) -> int | fastapi.responses.JSONResponse:
    if container.status != "running":
        return error.ErrorNodeNotRunning(node)

    try:
        result = container.exec_run(["du", "-sb", "/data"])
        stdin: str = result.output.decode("utf8")
        test = stdin.removesuffix("\t/data\n")
        return int(test)

    except docker_errors.APIError:
        return error.ErrorNodeSilent(node)
