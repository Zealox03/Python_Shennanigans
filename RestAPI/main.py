from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Define the app
app = FastAPI()

class Item(BaseModel):
    text: str = None
    is_done: bool = False 
    #False is the default value of the is_done

# A Decorator acts as a wrapper, lets you modify or extend 
# the behavior of another function or method without changing 
# its source code.

# To do items
items = []

# How to define a path in FastAPI
@app.get("/")
def root():
    return {"Hello": "World"}

# Define a path to see items
# Remember that POST Requests means Create 
@app.post("/items")
def create_item(item: Item):
    items.append(item)
    return items


# New endpoint
@app.get("/items", response_model=list[Item])
def list_items(limit: int = 10):
    return items[0:limit]


@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int) -> Item:
    if item_id < len(items):
        return items[item_id]
    else:
        raise HTTPException(status_code=404, detail=f"Item ID {item_id} not found")
