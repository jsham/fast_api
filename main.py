from enum import Enum
from fastapi import FastAPI

# Define Enum as a class
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

app = FastAPI()

# Basic endpoint define
@app.get("/")
async def root():
    return { "message": "Hello Fast API"}


# Using parameter and parameter type
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id", item_id}

@app.get("/users/me")
async def read_user_me():
    return { "user_id", "the current user"}

@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return { "user_id": user_id}

# Using Class Object as a parameters
@app.get("/models/{model_name}")
async def get_model(model_name : ModelName):
    if model_name is ModelName.alexnet:
        return {"modle_name": model_name, "message": "Deep Learning FTW!"}
    if model_name.value == "lenet":
        return {"modle_name": model_name, "message": "LeCNN all the images"}
    return {"model_name": model_name, "message": "Have some residuls"}

# Using file path as a parameter
@app.get ("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path":file_path}

# Using query parameter
# Use command: 
# http://127.0.0.1:8000/items/?skip=0&limit=10
fake_items_db = [
    {"item_name": "foo"},
    {"item_name": "Bar"},
    {"item_name": "Baz"},
    ]
@app.get("/q_items/")
async def read_query_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip+limit]

# Using selective paramter
# Use command: 
# http://127.0.0.1:8000/a_items/alexis?q=444
from typing import Union
@app.get("/a_items/{item_id}")
async def read_item(item_id: str, q: Union[str, None] = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}

# Type casting from qurey parameter to bool
# Use command: 
# http://127.0.0.1:8000/c_items/foo?short=1
# http://127.0.0.1:8000/c_items/foo?short=True
# http://127.0.0.1:8000/c_items/foo?short=true
# http://127.0.0.1:8000/c_items/foo?short=on

@app.get("c_items/{item_id}")
async def read_item(item_id: str, q: Union[str, None]=None, short: bool=False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description" : "This is an amazing item that has a long description"}
        )
    return item