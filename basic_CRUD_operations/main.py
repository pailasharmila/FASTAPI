from typing import Annotated

from fastapi import FastAPI, HTTPException
from pydantic import Field
from typing_extensions import TypedDict

app = FastAPI(prefix="/items", responses={404: {"description": "Item not found."}})


class Item(TypedDict):
    name: Annotated[str, Field(description="The name.")]
    description: Annotated[str | None, Field(None, description="The description.")]


class ItemOutput(Item):
    id: Annotated[int, Field(description="The Item ID.")]


items: dict[int, Item] = {}
id_counter = 0


@app.get("/")
async def read_items() -> list[ItemOutput]:
    """Read all items."""
    return [{"id": id, **item} for id, item in items.items()]


@app.get("/{item_id}")
def read_item(item_id: int) -> ItemOutput:
    """Read a single item."""
    try:
        return {"id": item_id, **items[item_id]}
    except KeyError:
        raise HTTPException(status_code=404, detail="Item not found")


@app.post("/")
def create_item(item: Item) -> ItemOutput:
    """Create a new item."""
    global id_counter
    items[id_counter] = item
    id_counter += 1
    return {"id": id_counter - 1, **item}


@app.put("/{item_id}")
def update_item(item_id: int, item: Item) -> ItemOutput:
    """Update an item."""
    try:
        items[item_id] = item
        return {"id": item_id, **item}
    except KeyError:
        raise HTTPException(status_code=404, detail="Item not found")


@app.delete("/{item_id}")
async def delete_item(item_id: int) -> ItemOutput:
    """Delete an item."""
    try:
        item = items.pop(item_id)
        return {"id": item_id, **item}
    except KeyError:
        raise HTTPException(status_code=404, detail="Item not found")