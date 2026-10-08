from pydantic import Field, BaseModel


class ItemCreateSchema(BaseModel):
    name: str = Field(..., description="Name of the item")
    optimal_stock: int = Field(..., description="Restock is suggested if review_item.quantity is less than this value")
    volume: float
    weight: float


class ItemPath(BaseModel):
    item_id: int = Field(..., description="The ID of the item target")
