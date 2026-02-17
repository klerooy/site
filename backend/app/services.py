from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Any

from .data import (
    account_demo,
    benefits,
    categories,
    contact_messages,
    contacts_info,
    favorites_demo,
    home_slider,
    orders_demo,
    products,
    promo_codes,
    special_sections,
)


def get_admin_stats() -> dict[str, Any]:
    valid_orders = [o for o in orders_demo if str(o.get("status")).lower() != "отменен"]
    revenue = sum(float(o.get("total", 0)) for o in valid_orders)
    return {
        "revenue": format_price(revenue),
        "ordersCount": len(orders_demo)
    }

def get_all_orders() -> list[dict[str, Any]]:
    return orders_demo

def update_order_status(order_id: str, new_status: str) -> dict[str, Any]:
    for o in orders_demo:
        if o["id"] == order_id:
            o["status"] = new_status
            return o
    raise ValueError("Заказ не найден")

def delete_product(product_id: int) -> bool:
    for i in range(len(products) - 1, -1, -1):
        if products[i].get("id") == product_id:
            products.pop(i)
            return True
    return False

def _product_index() -> dict[int, dict[str, Any]]:
    return {product["id"]: product for product in products}


def format_price(value: float) -> float:
    return float(f"{value:.2f}")


def get_home_payload() -> dict[str, Any]:
    popular = sorted(products, key=lambda item: item.get("popularity", 0), reverse=True)[:6]
    promotions = [product for product in products if product.get("old_price")][:4]
    return {
        "slider": home_slider,
        "categories": categories,
        "popular": popular,
        "promotions": promotions,
        "benefits": benefits,
    }


def get_categories() -> list[dict[str, Any]]:
    return categories


def category_filters_map() -> dict[str, list[str]]:
    return {
        "paints": ["type", "brand", "color"],
        "brushes": ["shape", "size", "brand"],
        "paper": ["type", "brand", "color"],
        "pencils": ["type", "hardness", "brand"],
        "sets": ["type", "brand", "color"],
        "easels": ["type", "brand", "color"],
    }


def get_filters_for_category(category: str | None) -> dict[str, list[str]]:
    if not category:
        return {}

    allowed_keys = category_filters_map().get(category, [])
    scoped_products = [product for product in products if product["category"] == category]
    result: dict[str, list[str]] = {}

    for key in allowed_keys:
        values = sorted(
            {
                str(product[key]).strip()
                for product in scoped_products
                if key in product and str(product[key]).strip()
            }
        )
        result[key] = values

    return result


def filter_products(
    category: str | None,
    query: str | None,
    sort: str,
    type_filter: str | None,
    brand_filter: str | None,
    color_filter: str | None,
    shape_filter: str | None,
    size_filter: str | None,
    hardness_filter: str | None,
) -> dict[str, Any]:
    result = deepcopy(products)

    if category and category != "Все":
        result = [item for item in result if item.get("category") == category]

    if query:
        q = query.lower().strip()
        result = [
            item
            for item in result
            if q in item["name"].lower()
            or q in item.get("brand", "").lower()
            or q in item.get("color", "").lower()
            or q in " ".join(item.get("tags", [])).lower()
        ]

    exact_filters = {
        "type": type_filter,
        "brand": brand_filter,
        "color": color_filter,
        "shape": shape_filter,
        "size": size_filter,
        "hardness": hardness_filter,
    }

    for key, value in exact_filters.items():
        if value:
            result = [item for item in result if str(item.get(key, "")).lower() == value.lower()]

    if sort == "price_asc":
        result.sort(key=lambda item: item["price"])
    elif sort == "price_desc":
        result.sort(key=lambda item: item["price"], reverse=True)
    elif sort == "popular":
        result.sort(key=lambda item: item.get("popularity", 0), reverse=True)
    else:
        result.sort(key=lambda item: item["id"], reverse=True)

    return {
        "items": result,
        "filters": get_filters_for_category(category),
        "count": len(result),
    }


def get_product_by_id(product_id: int) -> dict[str, Any] | None:
    product_map = _product_index()
    product = product_map.get(product_id)
    if not product:
        return None

    related = [product_map[rel_id] for rel_id in product.get("related_ids", []) if rel_id in product_map]
    reviews = [
        {
            "author": "Екатерина",
            "rating": 5,
            "date": "2026-01-11",
            "text": "Отличное качество, приятная упаковка и быстрая доставка.",
        },
        {
            "author": "Максим",
            "rating": 4,
            "date": "2025-12-26",
            "text": "Материал хороший, беру второй раз для студии.",
        },
    ]

    payload = deepcopy(product)
    payload["related"] = related
    payload["reviews"] = reviews
    return payload


def get_special_sections() -> list[dict[str, Any]]:
    product_map = _product_index()
    items: list[dict[str, Any]] = []
    for section in special_sections:
        section_copy = deepcopy(section)
        section_copy["products"] = [
            product_map[pid] for pid in section.get("product_ids", []) if pid in product_map
        ]
        items.append(section_copy)
    return items


def get_search_suggestions(query: str) -> list[dict[str, Any]]:
    if not query or len(query.strip()) < 2:
        return []

    q = query.lower().strip()
    suggestions: list[dict[str, Any]] = []

    for item in products:
        haystack = " ".join(
            [
                item["name"],
                item.get("brand", ""),
                item.get("color", ""),
                item.get("type", ""),
                item.get("shape", ""),
            ]
        ).lower()

        if q in haystack:
            suggestions.append(
                {
                    "id": item["id"],
                    "name": item["name"],
                    "brand": item.get("brand"),
                    "color": item.get("color"),
                    "slug": item.get("slug", ""),
                }
            )

    return suggestions[:8]


def empty_cart() -> dict[str, Any]:
    return {
        "items": [],
        "promo_code": None,
        "discount": 0.0,
        "subtotal": 0.0,
        "delivery_method": "courier",
        "delivery_cost": 350.0,
        "total": 350.0,
    }


def _base_delivery_cost(method: str) -> float:
    return 350.0 if method == "courier" else 0.0


def recalc_cart(cart: dict[str, Any]) -> dict[str, Any]:
    product_map = _product_index()
    subtotal = 0.0
    detailed_items: list[dict[str, Any]] = []

    for line in cart.get("items", []):
        product = product_map.get(line["product_id"])
        if not product:
            continue
        qty = max(1, int(line.get("qty", 1)))
        line_total = product["price"] * qty
        subtotal += line_total
        detailed_items.append(
            {
                "product": product,
                "qty": qty,
                "line_total": format_price(line_total),
            }
        )

    cart["subtotal"] = format_price(subtotal)

    discount = 0.0
    code = cart.get("promo_code")
    if code and code in promo_codes:
        promo = promo_codes[code]
        if promo["type"] == "percent":
            discount = subtotal * (promo["value"] / 100)
        else:
            discount = float(promo["value"])

    cart["discount"] = format_price(min(discount, subtotal))

    method = cart.get("delivery_method", "courier")
    delivery_cost = _base_delivery_cost(method)
    if subtotal >= 3500:
        delivery_cost = 0.0
    cart["delivery_cost"] = format_price(delivery_cost)

    total = max(0.0, subtotal - cart["discount"] + delivery_cost)
    cart["total"] = format_price(total)
    cart["detailed_items"] = detailed_items
    return cart


def default_account_payload() -> dict[str, Any]:
    return {
        "profile": account_demo,
        "orders": orders_demo,
        "favorites": [product for product in products if product["id"] in favorites_demo],
    }


def submit_contact_message(name: str, email: str, message: str) -> dict[str, Any]:
    entry = {
        "id": len(contact_messages) + 1,
        "name": name,
        "email": email,
        "message": message,
        "created_at": datetime.utcnow().isoformat() + "Z",
    }
    contact_messages.append(entry)
    return entry


def checkout_order(
    cart: dict[str, Any],
    full_name: str,
    phone: str,
    delivery_method: str,
    payment_method: str,
    address: str | None,
) -> dict[str, Any]:
    updated = recalc_cart(cart)
    if not updated.get("detailed_items"):
        raise ValueError("Корзина пуста")

    order = {
        "id": f"A-{datetime.utcnow().year}-{len(orders_demo) + 1:04d}",
        "date": datetime.utcnow().date().isoformat(),
        "status": "Принят",
        "total": updated["total"],
        "delivery_method": delivery_method,
        "payment_method": payment_method,
        "address": address,
        "recipient": full_name,
        "phone": phone,
        "items": [
            {"product_id": item["product"]["id"], "qty": item["qty"]}
            for item in updated["detailed_items"]
        ],
    }

    orders_demo.insert(0, order)
    return order


def get_contacts_payload() -> dict[str, Any]:
    return contacts_info