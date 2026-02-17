from __future__ import annotations

from typing import Any

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Импортируем данные (список)
from .data import blog_posts, promo_codes, products
from .schemas import (
    CartDeliveryUpdate,
    CartItemInput,
    CheckoutRequest,
    ContactRequest,
    PromoApplyRequest,
    Product,
)
from .services import (
    checkout_order,
    default_account_payload,
    empty_cart,
    filter_products,
    get_categories,
    get_contacts_payload,
    get_home_payload,
    get_product_by_id,
    get_search_suggestions,
    get_special_sections,
    recalc_cart,
    submit_contact_message,
)

app = FastAPI(
    title="Artistic Shop API",
    version="1.0.0",
    description="API интернет-магазина художественных принадлежностей",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

cart_state: dict[str, Any] = empty_cart()


class CartQtyUpdate(BaseModel):
    qty: int = Field(ge=1, le=99)


@app.get("/api/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/home")
def home() -> dict[str, Any]:
    return get_home_payload()


@app.get("/api/categories")
def categories() -> list[dict[str, Any]]:
    return get_categories()

@app.get("/api/products/popular", response_model=list[Product])
def get_popular_products():
    # Теперь products ссылается на импортированный список, а не на функцию ниже
    return [p for p in products if p.get("is_popular")]

# --- ИСПРАВЛЕНИЕ ЗДЕСЬ: Переименовали функцию из products в get_products ---
@app.get("/api/products")
def get_products(
    category: str | None = None,
    q: str | None = Query(default=None, alias="query"),
    sort: str = Query(default="new", pattern="^(new|price_asc|price_desc|popular)$"),
    type: str | None = None,
    brand: str | None = None,
    color: str | None = None,
    shape: str | None = None,
    size: str | None = None,
    hardness: str | None = None,
) -> dict[str, Any]:
    return filter_products(
        category=category,
        query=q,
        sort=sort,
        type_filter=type,
        brand_filter=brand,
        color_filter=color,
        shape_filter=shape,
        size_filter=size,
        hardness_filter=hardness,
    )


@app.get("/api/products/{product_id}")
def product_details(product_id: int) -> dict[str, Any]:
    for p in products:
        if p.get("id") == product_id:
            return p
            
    raise HTTPException(status_code=404, detail="Товар не найден")


@app.get("/api/search/suggest")
def search_suggest(q: str = Query(min_length=2)) -> list[dict[str, Any]]:
    return get_search_suggestions(q)


@app.get("/api/specials")
def specials() -> list[dict[str, Any]]:
    return get_special_sections()


@app.get("/api/account")
def account() -> dict[str, Any]:
    return default_account_payload()


@app.get("/api/contacts")
def contacts() -> dict[str, Any]:
    return get_contacts_payload()


@app.get("/api/cart")
def get_cart() -> dict[str, Any]:
    return recalc_cart(cart_state)


class OrderStatusUpdate(BaseModel):
    status: str


class AdminProductUpsert(BaseModel):
    name: str = Field(min_length=1)
    price: float = Field(ge=0)
    category: str = Field(min_length=1)
    image: str | None = None
    description: str | None = None
    in_stock: bool | None = None


class AdminBlogPostUpsert(BaseModel):
    title: str = Field(min_length=1)
    excerpt: str = Field(min_length=1)
    category: str = Field(min_length=1)
    date: str = Field(min_length=1)
    readTime: str = Field(min_length=1)
    image: str | None = None
    featured: bool = False
    content: str | None = None

@app.get("/api/admin/stats")
def admin_stats():
    from .services import get_admin_stats
    return get_admin_stats()

@app.get("/api/admin/orders")
def admin_orders():
    from .services import get_all_orders
    return get_all_orders()

@app.patch("/api/admin/orders/{order_id}/status")
def admin_update_order(order_id: str, payload: OrderStatusUpdate):
    from .services import update_order_status
    try:
        return update_order_status(order_id, payload.status)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))

@app.delete("/api/admin/products/{product_id}")
def admin_delete_product(product_id: int):
    from .services import delete_product
    if delete_product(product_id):
        return {"message": "Удалено успешно"}
    raise HTTPException(status_code=404, detail="Товар не найден")


@app.get("/api/blog")
def get_blog_posts() -> list[dict[str, Any]]:
    return blog_posts


@app.post("/api/admin/blog")
def admin_create_blog_post(payload: AdminBlogPostUpsert) -> dict[str, Any]:
    new_id = max((int(p.get("id", 0)) for p in blog_posts), default=0) + 1
    post: dict[str, Any] = {
        "id": new_id,
        "title": payload.title,
        "excerpt": payload.excerpt,
        "category": payload.category,
        "date": payload.date,
        "readTime": payload.readTime,
        "featured": bool(payload.featured),
    }
    if payload.image is not None:
        post["image"] = payload.image
    if payload.content is not None:
        post["content"] = payload.content

    if post.get("featured"):
        for existing in blog_posts:
            existing["featured"] = False

    blog_posts.insert(0, post)
    return post


@app.put("/api/admin/blog/{post_id}")
def admin_update_blog_post(post_id: int, payload: AdminBlogPostUpsert) -> dict[str, Any]:
    for p in blog_posts:
        if int(p.get("id")) == post_id:
            p["title"] = payload.title
            p["excerpt"] = payload.excerpt
            p["category"] = payload.category
            p["date"] = payload.date
            p["readTime"] = payload.readTime
            p["featured"] = bool(payload.featured)
            if payload.image is not None:
                p["image"] = payload.image
            else:
                p.pop("image", None)
            if payload.content is not None:
                p["content"] = payload.content
            else:
                p.pop("content", None)

            if p.get("featured"):
                for other in blog_posts:
                    if other is not p:
                        other["featured"] = False

            return p

    raise HTTPException(status_code=404, detail="Пост не найден")


@app.delete("/api/admin/blog/{post_id}")
def admin_delete_blog_post(post_id: int) -> dict[str, Any]:
    for i in range(len(blog_posts) - 1, -1, -1):
        if int(blog_posts[i].get("id")) == post_id:
            blog_posts.pop(i)
            return {"message": "Удалено успешно"}

    raise HTTPException(status_code=404, detail="Пост не найден")


@app.post("/api/admin/products")
def admin_create_product(payload: AdminProductUpsert) -> dict[str, Any]:
    new_id = max((int(p.get("id", 0)) for p in products), default=0) + 1
    product: dict[str, Any] = {
        "id": new_id,
        "name": payload.name,
        "price": payload.price,
        "category": payload.category,
    }
    if payload.image is not None:
        product["image"] = payload.image
    if payload.description is not None:
        product["description"] = payload.description
    if payload.in_stock is not None:
        product["in_stock"] = payload.in_stock

    products.insert(0, product)
    return product


@app.put("/api/admin/products/{product_id}")
def admin_update_product(product_id: int, payload: AdminProductUpsert) -> dict[str, Any]:
    for p in products:
        if int(p.get("id")) == product_id:
            p["name"] = payload.name
            p["price"] = payload.price
            p["category"] = payload.category
            if payload.image is not None:
                p["image"] = payload.image
            else:
                p.pop("image", None)
            if payload.description is not None:
                p["description"] = payload.description
            else:
                p.pop("description", None)
            if payload.in_stock is not None:
                p["in_stock"] = payload.in_stock
            return p

    raise HTTPException(status_code=404, detail="Товар не найден")

@app.post("/api/cart/items")
def add_to_cart(payload: CartItemInput) -> dict[str, Any]:
    for line in cart_state["items"]:
        if line["product_id"] == payload.product_id:
            line["qty"] += payload.qty
            return recalc_cart(cart_state)
        
    cart_state["items"].append({
        "product_id": payload.product_id, 
        "qty": payload.qty
    })
    
    return recalc_cart(cart_state)


@app.patch("/api/cart/items/{product_id}")
def update_cart_item(product_id: int, payload: CartQtyUpdate) -> dict[str, Any]:
    for line in cart_state["items"]:
        if line["product_id"] == product_id:
            line["qty"] = payload.qty
            return recalc_cart(cart_state)

    raise HTTPException(status_code=404, detail="Позиция в корзине не найдена")


@app.delete("/api/cart/items/{product_id}")
def remove_cart_item(product_id: int) -> dict[str, Any]:
    cart_state["items"] = [line for line in cart_state["items"] if line["product_id"] != product_id]
    return recalc_cart(cart_state)


@app.patch("/api/cart/delivery")
def update_delivery(payload: CartDeliveryUpdate) -> dict[str, Any]:
    cart_state["delivery_method"] = payload.delivery_method
    return recalc_cart(cart_state)


@app.post("/api/cart/promo")
def apply_promo(payload: PromoApplyRequest) -> dict[str, Any]:
    code = payload.code.strip().upper()
    if code not in promo_codes:
        raise HTTPException(status_code=400, detail="Промокод не найден")

    cart_state["promo_code"] = code
    return recalc_cart(cart_state)


@app.delete("/api/cart/promo")
def clear_promo() -> dict[str, Any]:
    cart_state["promo_code"] = None
    return recalc_cart(cart_state)


@app.post("/api/checkout")
def checkout(payload: CheckoutRequest) -> dict[str, Any]:
    if payload.delivery_method == "courier" and not payload.address:
        raise HTTPException(status_code=422, detail="Для курьерской доставки нужен адрес")

    try:
        order = checkout_order(
            cart=cart_state,
            full_name=payload.full_name,
            phone=payload.phone,
            delivery_method=payload.delivery_method,
            payment_method=payload.payment_method,
            address=payload.address,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    cart_state.update(empty_cart())
    return {"message": "Заказ успешно оформлен", "order": order}


@app.post("/api/contact")
def send_contact(payload: ContactRequest) -> dict[str, Any]:
    entry = submit_contact_message(
        name=payload.name,
        email=payload.email,
        message=payload.message,
    )
    return {"message": "Спасибо! Мы свяжемся с вами в течение дня.", "contact": entry}