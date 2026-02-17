from __future__ import annotations

from typing import Any


categories: list[dict[str, Any]] = [
    {
        "slug": "paints",
        "name": "Краски",
        "description": "Акварель, гуашь, акрил и масло для любой техники.",
        "image": "https://images.unsplash.com/photo-1513364776144-60967b0f800f?auto=format&fit=crop&w=1200&q=80",
    },
    {
        "slug": "brushes",
        "name": "Кисти",
        "description": "Мягкие и упругие кисти для акварели, масла и акрила.",
        "image": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?auto=format&fit=crop&w=1200&q=80",
    },
    {
        "slug": "paper",
        "name": "Бумага",
        "description": "Скетчбуки и профессиональная бумага разных фактур.",
        "image": "https://images.unsplash.com/photo-1455390582262-044cdead277a?auto=format&fit=crop&w=1200&q=80",
    },
    {
        "slug": "pencils",
        "name": "Карандаши",
        "description": "Графит, цветные и пастельные карандаши.",
        "image": "https://images.unsplash.com/photo-1449247613801-ab06418e2861?auto=format&fit=crop&w=1200&q=80",
    },
    {
        "slug": "sets",
        "name": "Наборы",
        "description": "Готовые комплекты для начинающих и подарков.",
        "image": "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?auto=format&fit=crop&w=1200&q=80",
    },
    {
        "slug": "easels",
        "name": "Мольберты",
        "description": "Настольные и напольные мольберты для дома и студии.",
        "image": "https://images.unsplash.com/photo-1513366208864-87536b8bd7b4?auto=format&fit=crop&w=1200&q=80",
    },
]

products: list[dict[str, Any]] = [
    {
        "id": 101,
        "name": "Набор акварели \"Белые ночи\"",
        "price": 2400,
        "image": "https://images.unsplash.com/photo-1629196914375-f7e48f477b6d?auto=format&fit=crop&w=500&q=80",
        "category": "Акварель",
        "description": "Профессиональные акварельные краски высшего качества.",
        "is_popular": True,
        "photos": [
            "https://images.unsplash.com/photo-1629196914375-f7e48f477b6d?auto=format&fit=crop&w=1000&q=80",
            "https://images.unsplash.com/photo-1513364776144-60967b0f800f?auto=format&fit=crop&w=1000&q=80"
        ],
        "specs": [
            {"label": "Светостойкость", "value": "Высокая (***)"},
            {"label": "Форма", "value": "Кюветы 2.5мл"}
        ],
        "reviews": [
            {"id": 1, "user": "Анна", "date": "10.02.2026", "text": "Лучшая акварель!", "rating": 5}
        ]
    },
    {
        "id": 102,
        "name": "Холст на подрамнике 40x50",
        "price": 850,
        "image": "https://артснаб.рф/wa-data/public/shop/products/53/55/5553/images/23638/23638.970.jpg",
        "category": "Холсты",
        "is_popular": True
    },
    {
        "id": 103,
        "name": "Набор кистей (Синтетика)",
        "price": 1200,
        "image": "https://artgammamarket.ru/wa-data/public/shop/products/80/20/2080/images/3714/3714.750x0.jpg",
        "category": "Кисти",
        "is_popular": True
    },
    {
        "id": 104,
        "name": "Масло \"Мастер-Класс\", набор",
        "price": 3600,
        "image": "https://krasniykarandash.ru/upload/resize_cache/iblock/2b2/758_758_1/2b238bb540d08a9e19953f616b007865.jpg",
        "category": "Масло",
        "is_popular": True
    },
]

special_sections: list[dict[str, Any]] = [
    {
        "slug": "beginner-kits",
        "title": "Наборы для начинающих",
        "description": "Продуманные комплекты с понятным стартом и инструкциями.",
        "product_ids": [11, 8, 10],
        "image": "https://images.unsplash.com/photo-1453738773917-9c3eff1db985?auto=format&fit=crop&w=1200&q=80",
    },
    {
        "slug": "gift-ideas",
        "title": "Подарочные сертификаты и наборы",
        "description": "Красивые подарки, которые вдохновляют творить.",
        "product_ids": [12, 15, 1],
        "image": "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?auto=format&fit=crop&w=1200&q=80",
    },
]

home_slider: list[dict[str, str]] = [
    {
        "title": "Место, где рождаются идеи",
        "subtitle": "Премиальные материалы для живописи, скетчинга и вдохновения.",
        "image": "https://images.unsplash.com/photo-1455390582262-044cdead277a?auto=format&fit=crop&w=1800&q=80",
        "cta": "Смотреть каталог",
        "cta_link": "/catalog",
    },
    {
        "title": "Нежные палитры, мягкий свет",
        "subtitle": "Собрали коллекцию приглушенных оттенков для уютной студии.",
        "image": "https://images.unsplash.com/photo-1452860606245-08befc0ff44b?auto=format&fit=crop&w=1800&q=80",
        "cta": "Наборы для старта",
        "cta_link": "/specials",
    },
    {
        "title": "Подарки для творческих людей",
        "subtitle": "Сертификаты и готовые боксы с эстетичной упаковкой.",
        "image": "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?auto=format&fit=crop&w=1800&q=80",
        "cta": "Выбрать подарок",
        "cta_link": "/specials",
    },
]

benefits: list[dict[str, str]] = [
    {
        "icon": "🚚",
        "title": "Бесплатная доставка",
        "description": "При заказе от 3500 ₽ по всей России.",
    },
    {
        "icon": "🎁",
        "title": "Подарок в каждом заказе",
        "description": "Маленький творческий бонус внутри коробки.",
    },
    {
        "icon": "🧑‍🎨",
        "title": "Подбор материалов",
        "description": "Поможем собрать набор под вашу технику.",
    },
    {
        "icon": "↩️",
        "title": "Лёгкий возврат",
        "description": "14 дней на обмен и возврат без сложностей.",
    },
]

promo_codes: dict[str, dict[str, Any]] = {
    "ARTSTART": {"type": "percent", "value": 10},
    "GIFT500": {"type": "fixed", "value": 500},
    "CREAM": {"type": "percent", "value": 7},
}

orders_demo: list[dict[str, Any]] = [

]

favorites_demo: list[int] = [10, 11, 16]

account_demo: dict[str, Any] = {
    "name": "Анна Морозова",
    "email": "anna@example.com",
    "bonuses": 740,
}

contacts_info: dict[str, Any] = {
    "address": "Курск, ул. Артельная, 12",
    "phone": "+7 (495) 123-45-67",
    "email": "hello@artistic-shop.ru",
    "work_hours": "Ежедневно: 10:00-21:00",
    "map_embed": "https://www.openstreetmap.org/export/embed.html?bbox=37.6063%2C55.7488%2C37.6363%2C55.7688&layer=mapnik&marker=55.7588%2C37.6213",
    "photo": "https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?auto=format&fit=crop&w=1200&q=80",
}

contact_messages: list[dict[str, Any]] = []

blog_posts: list[dict[str, Any]] = [
    {
        "id": 1,
        "title": "Как выбрать свою первую акварель: полное руководство",
        "excerpt": "Разбираемся в пигментах, связующих и форматах. Что лучше для новичка: кюветы или тубы? И почему не стоит экономить на бумаге.",
        "category": "Уроки и техники",
        "date": "15 Фев 2026",
        "readTime": "8 мин",
        "image": "https://images.unsplash.com/photo-1513364776144-60967b0f800f?auto=format&fit=crop&w=1200&q=80",
        "featured": True,
        "content": "",
    },
    {
        "id": 2,
        "title": "Колонок против синтетики: битва кистей",
        "excerpt": "Тестируем современные синтетические кисти и сравниваем их с классическим натуральным ворсом. Результаты вас удивят.",
        "category": "Обзоры материалов",
        "date": "10 Фев 2026",
        "readTime": "5 мин",
        "image": "https://images.unsplash.com/photo-1515462277126-2dd0c162007a?auto=format&fit=crop&w=800&q=80",
        "featured": False,
        "content": "",
    },
]
