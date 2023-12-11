import json
import typing
from fastapi import FastAPI, Request
from starlette.responses import Response, JSONResponse

from elastic_data import connection


class PrettyJSONResponse(Response):
    media_type = "application/json"

    def render(self, content: typing.Any) -> bytes:
        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=4,
            separators=(", ", ": "),
        ).encode("utf-8")


app = FastAPI()


@app.get("/test")
async def test():
    return {"test": "successful!"}


@app.get("/homes", response_class=PrettyJSONResponse)
async def getHomes():
    json = connection.get_json_by_index('housing_test')
    return json


@app.get("/index/{index_name}", response_class=PrettyJSONResponse)
async def getHomes(index_name: str):
    json = connection.get_json_by_index(index_name)
    return json

async def value_error_exception_handler(request: Request):
    return JSONResponse(
        status_code=400,
        content={"message": "Error, probably index name not found"},
    )