import json
import typing
from fastapi import FastAPI
from starlette.responses import Response

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
