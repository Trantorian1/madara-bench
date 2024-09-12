import datetime

import docker
from docker import errors as docker_errors
from docker.models.containers import Container

from app import error, models


def container_get(
    node: models.NodeName,
) -> Container:
    try:
        client = docker.client.from_env()
        return client.containers.get(node + "_runner")

    except docker_errors.NotFound:
        raise error.ErrorNodeNotFound(node)
    except docker_errors.APIError:
        raise error.ErrorNodeSilent(node)


# As explained in https://github.com/moby/moby/issues/26711
def stats_cpu_normalized(
    node: models.NodeName, container: Container
) -> models.ResponseModelStats[float]:
    error.container_check_running(node, container)

    time_start = datetime.datetime.now()

    try:
        stats = container.stats(stream=False)
    except docker_errors.APIError:
        raise error.ErrorNodeSilent(node)

    cpu_delta: int = (
        stats["cpu_stats"]["cpu_usage"]["total_usage"]
        - stats["precpu_stats"]["cpu_usage"]["total_usage"]
    )
    cpu_count: int = stats["cpu_stats"]["online_cpus"]
    system_delta: int = (
        stats["cpu_stats"]["system_cpu_usage"]
        - stats["precpu_stats"]["system_cpu_usage"]
    )

    cpu_usage = (
        (float(cpu_delta) / float(system_delta)) * float(cpu_count) * 100.0
        if system_delta > 0
        else 0.0
    )

    return models.ResponseModelStats(
        node=node, when=time_start, value=cpu_usage
    )


def stats_cpu_system(
    node: models.NodeName, container: Container
) -> models.ResponseModelStats[float]:
    error.container_check_running(node, container)

    time_start = datetime.datetime.now()

    try:
        stats = container.stats(stream=False)
    except docker_errors.APIError:
        raise error.ErrorNodeSilent(node)

    cpu_delta: int = (
        stats["cpu_stats"]["cpu_usage"]["total_usage"]
        - stats["precpu_stats"]["cpu_usage"]["total_usage"]
    )
    system_delta: int = (
        stats["cpu_stats"]["system_cpu_usage"]
        - stats["precpu_stats"]["system_cpu_usage"]
    )

    cpu_usage = (
        (float(cpu_delta) / float(system_delta)) * 100.0
        if system_delta > 0
        else 0.0
    )

    return models.ResponseModelStats(
        node=node, when=time_start, value=cpu_usage
    )


def stats_memory(
    node: models.NodeName, container: Container
) -> models.ResponseModelStats[int]:
    error.container_check_running(node, container)

    time_start = datetime.datetime.now()

    try:
        stats = container.stats(stream=False)
    except docker_errors.APIError:
        raise error.ErrorNodeSilent(node)

    memory_usage = stats["memory_stats"]["usage"]
    return models.ResponseModelStats(
        node=node, when=time_start, value=memory_usage
    )


def stats_storage(
    node: models.NodeName, container: Container
) -> models.ResponseModelStats[int]:
    error.container_check_running(node, container)

    time_start = datetime.datetime.now()

    try:
        result = container.exec_run(["du", "-sb", "/data"])
    except docker_errors.APIError:
        raise error.ErrorNodeSilent(node)

    stdin: str = result.output.decode("utf8")
    test = stdin.removesuffix("\t/data\n")
    storage_usage = int(test)

    return models.ResponseModelStats(
        node=node, when=time_start, value=storage_usage
    )
