from pydantic import BaseModel, Field


class PurchaseOrderItemCreateSchema(BaseModel):
    item_id: int = Field(..., description="Reference to item.item_id")
    price: float = Field(..., gt=0, description="Current price (must be greater than 0)")
    quantity: int = Field(..., gt=0, description="Quantity (must be greater than 0)")


class PurchaseOrderPath(BaseModel):
    purchase_order_id: int = Field(..., description="ID of the purchase order from URL")
