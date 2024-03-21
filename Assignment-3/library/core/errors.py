from starlette.responses import JSONResponse

from core.constants import CLOSED_ERR, EXISTS_ERR, NOT_FOUND


class ExistsError(Exception):
    def __init__(
        self, resource_type: str, resource_field: str, resource_id: str
    ) -> None:
        self.type = resource_type
        self.id = resource_id
        self.field = resource_field

    def return_json_response(self) -> JSONResponse:
        content = {
            "error": {
                "message": f"{self.type} with {self.field}<{self.id}> already exists."
            }
        }
        return JSONResponse(status_code=EXISTS_ERR, content=content)


class DoesNotExistError(Exception):
    def __init__(self, resource_type: str, resource_id: str) -> None:
        self.type = resource_type
        self.id = resource_id

    def return_json_response(self) -> JSONResponse:
        content = {
            "error": {"message": f"{self.type} with id<{self.id}> does not exist."}
        }
        return JSONResponse(status_code=NOT_FOUND, content=content)


class ClosedError(Exception):
    def __init__(self, resource_type: str, resource_id: str) -> None:
        self.type = resource_type
        self.id = resource_id

    def return_json_response(self) -> JSONResponse:
        content = {"error": {"message": f"{self.type} with id<{self.id}> is closed."}}
        return JSONResponse(status_code=CLOSED_ERR, content=content)
