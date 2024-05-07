from pydantic import BaseModel
from uuid import UUID, uuid4


class Grocery(BaseModel):
    id: UUID = uuid4()
    title: str
    quantity: int

class GroceryRequest(BaseModel):
    title: str
    quantity: int