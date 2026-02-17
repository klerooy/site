from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class Product(BaseModel):
    id: int
    name: str
    price: int
    image: str
    category: str
    description: Optional[str] = None
    is_popular: bool = False

class CartItemInput(BaseModel):
    product_id: int
    qty: int = Field(default=1, ge=1, le=99)


class CartDeliveryUpdate(BaseModel):
    delivery_method: Literal["courier", "pickup"]


class PromoApplyRequest(BaseModel):
    code: str = Field(min_length=2, max_length=32)


class ContactRequest(BaseModel):
    name: str = Field(min_length=2, max_length=64)
    email: str = Field(min_length=5, max_length=128)
    message: str = Field(min_length=5, max_length=2000)


class CheckoutRequest(BaseModel):
    full_name: str = Field(min_length=2, max_length=128)
    phone: str = Field(min_length=6, max_length=32)
    delivery_method: Literal["courier", "pickup"]
    payment_method: Literal["card", "cash", "sbp"]
    address: str | None = Field(default=None, max_length=200)


class ApiMessage(BaseModel):
    message: str
    data: dict[str, Any] | list[Any] | None = None
