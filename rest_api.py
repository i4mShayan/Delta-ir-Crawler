# run it through:
# uvicorn rest_api:app --reload

import json
import typing
from fastapi import FastAPI
from starlette.responses import Response
import pandas as pd
from elastic_data import connection
from time import gmtime, strftime

app = FastAPI()


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


async def addIndex(csv_file_path, index_name):
    response = "successful!"
    try:
        csv = pd.read_csv(csv_file_path)
        connection.addBulk(csv, index_name)
    except:
        response = "error!"
    return {"response": response, "file_path": csv_file_path, "index_name": index_name}


async def getIndex(index_name):
    try:
        return connection.get_json_by_index(index_name)
    except:
        return {"response": "error!", "index_name": index_name}


async def dropIndex(index_name):
    response = "successful!"
    try:
        connection.drop(index_name)
    except:
        response = "error!"
    return {"response": response, "index_name": index_name}

@app.get("", response_class=PrettyJSONResponse)
@app.get("/", response_class=PrettyJSONResponse)
@app.get("/test", response_class=PrettyJSONResponse)
async def test():
    return {"response": "Success! Server is up!", "Current Time":strftime("%Y-%m-%d %H:%M:%S", gmtime())}


@app.get("/add/{index_name}/from_csv/{csv_file_path:path}", response_class=PrettyJSONResponse)
async def addIndexApi(index_name: str, csv_file_path: str):
    return await addIndex(csv_file_path, index_name)


@app.get("/{index_name}", response_class=PrettyJSONResponse)
@app.get("/get/{index_name}/", response_class=PrettyJSONResponse)
async def getIndexApi(index_name: str):
    return await getIndex(index_name)



@app.get("/drop/{index_name}", response_class=PrettyJSONResponse)
async def dropIndexApiNotSure(index_name: str):
    return {"Message":"are you sure? add /iamsure at the end of url if so."}

@app.get("/drop/{index_name}/iamsure", response_class=PrettyJSONResponse)
async def dropIndexApi(index_name: str):
    return await dropIndex(index_name)
