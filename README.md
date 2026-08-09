# Norwick & Co. — Full-Stack Storefront

A complete e-commerce site built with **FastAPI** (Python) and **SQLite**. Product listings,
categories, product detail pages, cart, checkout with a simulated payment form, user
registration/login, and order history are all included. No React/Node — server-rendered
HTML pages, one process, one database file.

## Run it (2 commands, one time setup)

```bash
pip install -r requirements.txt --break-system-packages
uvicorn main:app --reload
```

Then open **http://127.0.0.1:8000** in your browser.

That's it — every time after this, you only need:

```bash
uvicorn main:app --reload
```

The database (`store.db`) and 25 product images are generated automatically the first
time the app starts, so there's nothing else to configure.

## What's included

- **Catalog** — 25 products across Electronics, Fashion, Home & Kitchen, Books, and
  Sports & Outdoors, each with its own hand-drawn line-art badge image (generated locally,
  no external image downloads or API keys needed).
- **Product pages** — description, price, rating, related items, quantity picker.
- **Search & sort** — search by name, filter by category, sort by price or rating.
- **Cart** — add/update/remove items, live subtotal, shipping and tax estimate.
- **Checkout** — shipping address form + a card payment form (number/expiry/CVV with
  input formatting and validation). This is a **simulated** payment flow for
  demonstration — no real charge is ever made and no card data is sent anywhere.
- **Accounts** — register/login with securely hashed passwords (PBKDF2), session cookies.
- **Order history** — "My Orders" page and a per-order confirmation/detail page.

## Project structure

```
store/
├── main.py              # FastAPI app & all routes
├── models.py             # SQLAlchemy models (User, Product, CartItem, Order, OrderItem)
├── database.py            # DB engine/session setup
├── seed_data.py            # The 25 products (auto-loaded on first run)
├── gen_icons.py             # Generates the product badge SVGs (already run — output in static/images/products)
├── requirements.txt
├── templates/               # Jinja2 HTML templates
└── static/
    ├── css/style.css          # All styling
    ├── js/checkout.js          # Card input formatting
    └── images/products/          # Generated product badge SVGs
```

## Notes

- To reset the store (fresh database, empty orders), just delete `store.db` and restart.
- To regenerate product images after editing `seed_data.py`, run `python3 gen_icons.py`.
- Change the port with `uvicorn main:app --reload --port 8080`.
