import fastapi

from app.stats import NodeName


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
