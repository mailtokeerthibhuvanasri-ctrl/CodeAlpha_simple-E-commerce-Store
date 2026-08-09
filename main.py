import hashlib
import hmac
import os
import re
import secrets
from datetime import datetime

from fastapi import FastAPI, Request, Depends, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func

from database import Base, engine, get_db
from models import User, Product, CartItem, Order, OrderItem
from seed_data import PRODUCTS

APP_SECRET = os.environ.get("APP_SECRET", secrets.token_hex(32))

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Norwick & Co.")
app.add_middleware(SessionMiddleware, secret_key=APP_SECRET, session_cookie="norwick_session")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

CATEGORIES = ["Electronics", "Fashion", "Home & Kitchen", "Books", "Sports & Outdoors"]


def slugify(name: str) -> str:
    s = name.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def hash_password(password: str, salt: str | None = None) -> str:
    salt = salt or secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 130_000)
    return f"{salt}${digest.hex()}"


def verify_password(password: str, stored: str) -> bool:
    try:
        salt, digest_hex = stored.split("$")
    except ValueError:
        return False
    check = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 130_000)
    return hmac.compare_digest(check.hex(), digest_hex)


def seed_products(db: Session):
    if db.query(Product).count() > 0:
        return
    for p in PRODUCTS:
        db.add(Product(
            name=p["name"], slug=slugify(p["name"]), category=p["category"],
            price=p["price"], compare_price=p.get("compare_price"),
            description=p["description"], tagline=p["tagline"],
            icon_key=p["icon_key"], accent=p["accent"],
            stock=30, rating=p["rating"], reviews=p["reviews"],
        ))
    db.commit()


with next(get_db()) as db:
    seed_products(db)


def current_user(request: Request, db: Session) -> User | None:
    user_id = request.session.get("user_id")
    if not user_id:
        return None
    return db.query(User).filter(User.id == user_id).first()


def cart_count(db: Session, user: User | None) -> int:
    if not user:
        return 0
    total = db.query(func.sum(CartItem.quantity)).filter(CartItem.user_id == user.id).scalar()
    return total or 0


def base_context(request: Request, db: Session, **extra):
    user = current_user(request, db)
    return {
        "request": request,
        "user": user,
        "categories": CATEGORIES,
        "cart_count": cart_count(db, user),
        **extra,
    }


# ---------- Home & catalog ----------

@app.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    featured = db.query(Product).order_by(Product.reviews.desc()).limit(4).all()
    on_sale = db.query(Product).filter(Product.compare_price.isnot(None)).limit(4).all()
    by_category = {c: db.query(Product).filter(Product.category == c).limit(4).all() for c in CATEGORIES}
    ctx = base_context(request, db, featured=featured, on_sale=on_sale, by_category=by_category)
    return templates.TemplateResponse("index.html", ctx)


@app.get("/shop", response_class=HTMLResponse)
def shop(request: Request, db: Session = Depends(get_db), category: str = "", q: str = "", sort: str = ""):
    query = db.query(Product)
    if category and category in CATEGORIES:
        query = query.filter(Product.category == category)
    if q:
        like = f"%{q}%"
        query = query.filter(Product.name.ilike(like))
    if sort == "price_low":
        query = query.order_by(Product.price.asc())
    elif sort == "price_high":
        query = query.order_by(Product.price.desc())
    elif sort == "rating":
        query = query.order_by(Product.rating.desc())
    else:
        query = query.order_by(Product.id.asc())
    products = query.all()
    ctx = base_context(request, db, products=products, active_category=category, q=q, sort=sort)
    return templates.TemplateResponse("shop.html", ctx)


@app.get("/product/{slug}", response_class=HTMLResponse)
def product_detail(slug: str, request: Request, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.slug == slug).first()
    if not product:
        return RedirectResponse("/shop", status_code=303)
    related = (db.query(Product)
               .filter(Product.category == product.category, Product.id != product.id)
               .limit(4).all())
    ctx = base_context(request, db, product=product, related=related, added=request.query_params.get("added"))
    return templates.TemplateResponse("product_detail.html", ctx)


# ---------- Auth ----------

@app.get("/register", response_class=HTMLResponse)
def register_form(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("register.html", base_context(request, db, error=None))


@app.post("/register")
def register(request: Request, db: Session = Depends(get_db),
             name: str = Form(...), email: str = Form(...), password: str = Form(...)):
    email = email.strip().lower()
    if db.query(User).filter(User.email == email).first():
        ctx = base_context(request, db, error="An account with that email already exists.")
        return templates.TemplateResponse("register.html", ctx, status_code=400)
    if len(password) < 6:
        ctx = base_context(request, db, error="Password must be at least 6 characters.")
        return templates.TemplateResponse("register.html", ctx, status_code=400)
    user = User(name=name.strip(), email=email, password_hash=hash_password(password))
    db.add(user)
    db.commit()
    db.refresh(user)
    request.session["user_id"] = user.id
    return RedirectResponse("/", status_code=303)


@app.get("/login", response_class=HTMLResponse)
def login_form(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("login.html", base_context(request, db, error=None))


@app.post("/login")
def login(request: Request, db: Session = Depends(get_db),
          email: str = Form(...), password: str = Form(...)):
    user = db.query(User).filter(User.email == email.strip().lower()).first()
    if not user or not verify_password(password, user.password_hash):
        ctx = base_context(request, db, error="Incorrect email or password.")
        return templates.TemplateResponse("login.html", ctx, status_code=400)
    request.session["user_id"] = user.id
    return RedirectResponse("/", status_code=303)


@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status_code=303)


# ---------- Cart ----------

@app.post("/cart/add")
def cart_add(request: Request, db: Session = Depends(get_db),
             product_id: int = Form(...), quantity: int = Form(1), next: str = Form("/cart")):
    user = current_user(request, db)
    if not user:
        return RedirectResponse(f"/login?next={next}", status_code=303)
    item = db.query(CartItem).filter(CartItem.user_id == user.id, CartItem.product_id == product_id).first()
    if item:
        item.quantity += max(1, quantity)
    else:
        db.add(CartItem(user_id=user.id, product_id=product_id, quantity=max(1, quantity)))
    db.commit()
    return RedirectResponse(next, status_code=303)


@app.post("/cart/update")
def cart_update(request: Request, db: Session = Depends(get_db),
                 item_id: int = Form(...), quantity: int = Form(...)):
    user = current_user(request, db)
    if not user:
        return RedirectResponse("/login", status_code=303)
    item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.user_id == user.id).first()
    if item:
        if quantity <= 0:
            db.delete(item)
        else:
            item.quantity = quantity
        db.commit()
    return RedirectResponse("/cart", status_code=303)


@app.post("/cart/remove")
def cart_remove(request: Request, db: Session = Depends(get_db), item_id: int = Form(...)):
    user = current_user(request, db)
    if user:
        item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.user_id == user.id).first()
        if item:
            db.delete(item)
            db.commit()
    return RedirectResponse("/cart", status_code=303)


@app.get("/cart", response_class=HTMLResponse)
def cart_view(request: Request, db: Session = Depends(get_db)):
    user = current_user(request, db)
    items = []
    subtotal = 0.0
    if user:
        items = db.query(CartItem).filter(CartItem.user_id == user.id).all()
        subtotal = sum(i.product.price * i.quantity for i in items)
    shipping = 0.0 if subtotal == 0 or subtotal >= 75 else 6.5
    tax = round(subtotal * 0.07, 2)
    total = round(subtotal + shipping + tax, 2)
    ctx = base_context(request, db, items=items, subtotal=round(subtotal, 2),
                        shipping=shipping, tax=tax, total=total)
    return templates.TemplateResponse("cart.html", ctx)


# ---------- Checkout ----------

@app.get("/checkout", response_class=HTMLResponse)
def checkout_form(request: Request, db: Session = Depends(get_db)):
    user = current_user(request, db)
    if not user:
        return RedirectResponse("/login?next=/checkout", status_code=303)
    items = db.query(CartItem).filter(CartItem.user_id == user.id).all()
    if not items:
        return RedirectResponse("/cart", status_code=303)
    subtotal = sum(i.product.price * i.quantity for i in items)
    shipping = 0.0 if subtotal >= 75 else 6.5
    tax = round(subtotal * 0.07, 2)
    total = round(subtotal + shipping + tax, 2)
    ctx = base_context(request, db, items=items, subtotal=round(subtotal, 2),
                        shipping=shipping, tax=tax, total=total, error=None)
    return templates.TemplateResponse("checkout.html", ctx)


@app.post("/checkout")
def checkout_submit(
    request: Request, db: Session = Depends(get_db),
    full_name: str = Form(...), address: str = Form(...), city: str = Form(...),
    postal_code: str = Form(...), card_number: str = Form(...),
    card_expiry: str = Form(...), card_cvv: str = Form(...),
):
    user = current_user(request, db)
    if not user:
        return RedirectResponse("/login?next=/checkout", status_code=303)
    items = db.query(CartItem).filter(CartItem.user_id == user.id).all()
    if not items:
        return RedirectResponse("/cart", status_code=303)

    digits = re.sub(r"\D", "", card_number)
    errors = []
    if len(digits) < 15 or len(digits) > 16:
        errors.append("Enter a valid 15 or 16 digit card number.")
    if not re.match(r"^(0[1-9]|1[0-2])\/?\d{2}$", card_expiry.strip()):
        errors.append("Enter the expiry as MM/YY.")
    if not re.match(r"^\d{3,4}$", card_cvv.strip()):
        errors.append("Enter a valid CVV.")

    if errors:
        subtotal = sum(i.product.price * i.quantity for i in items)
        shipping = 0.0 if subtotal >= 75 else 6.5
        tax = round(subtotal * 0.07, 2)
        total = round(subtotal + shipping + tax, 2)
        ctx = base_context(request, db, items=items, subtotal=round(subtotal, 2),
                            shipping=shipping, tax=tax, total=total, error=" ".join(errors))
        return templates.TemplateResponse("checkout.html", ctx, status_code=400)

    subtotal = sum(i.product.price * i.quantity for i in items)
    shipping = 0.0 if subtotal >= 75 else 6.5
    tax = round(subtotal * 0.07, 2)
    total = round(subtotal + shipping + tax, 2)

    brand = "Amex" if digits.startswith(("34", "37")) else "Visa" if digits.startswith("4") else "Mastercard" if digits.startswith(("5", "2")) else "Card"

    order = Order(
        user_id=user.id, total=total, status="Confirmed",
        full_name=full_name, address=address, city=city, postal_code=postal_code,
        card_brand=brand, card_last4=digits[-4:],
    )
    db.add(order)
    db.flush()
    for i in items:
        db.add(OrderItem(order_id=order.id, product_id=i.product_id,
                          product_name=i.product.name, quantity=i.quantity, price=i.product.price))
        db.delete(i)
    db.commit()
    return RedirectResponse(f"/orders/{order.id}?success=1", status_code=303)


# ---------- Orders ----------

@app.get("/orders", response_class=HTMLResponse)
def orders_list(request: Request, db: Session = Depends(get_db)):
    user = current_user(request, db)
    if not user:
        return RedirectResponse("/login?next=/orders", status_code=303)
    orders = db.query(Order).filter(Order.user_id == user.id).order_by(Order.created_at.desc()).all()
    ctx = base_context(request, db, orders=orders)
    return templates.TemplateResponse("orders.html", ctx)


@app.get("/orders/{order_id}", response_class=HTMLResponse)
def order_detail(order_id: int, request: Request, db: Session = Depends(get_db)):
    user = current_user(request, db)
    if not user:
        return RedirectResponse("/login", status_code=303)
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == user.id).first()
    if not order:
        return RedirectResponse("/orders", status_code=303)
    ctx = base_context(request, db, order=order, success=request.query_params.get("success"))
    return templates.TemplateResponse("order_detail.html", ctx)
