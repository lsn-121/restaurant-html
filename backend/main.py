import os
from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, Field, Session, create_engine, select

engine = create_engine(os.getenv("DATABASE_URL"))
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins="https://lsn-121.github.io",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Product(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    price: float

class CartItem(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    product_id: int
    quantity: int = 1

class Receipt(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    total: float
    items: str
    created_at: datetime = Field(default_factory=datetime.now)


@app.on_event("startup")
def startup():
    SQLModel.metadata.create_all(engine)

    with Session(engine) as db:
        if not db.exec(select(Product)).first():
            db.add_all([
                Product(id=1, name="Наушники", price=2990),
                Product(id=2, name="Губозакаточная машинка", price=222),
                Product(id=3, name="Робот-пылесос XIAOMI", price=240),
            ])
            db.commit()


@app.get("/cart")
def get_cart():
    with Session(engine) as db:
        result = []
        for item in db.exec(select(CartItem)).all():
            product = db.get(Product, item.product_id)
            if product:
                result.append({
                    "product_id": product.id,
                    "name": product.name,
                    "price": product.price,
                    "quantity": item.quantity
                })
        return result


@app.post("/cart/{product_id}")
def update_cart(product_id: int, quantity: int):
    with Session(engine) as db:
        if not db.get(Product, product_id):
            raise HTTPException(404, "Товар не найден")

        item = db.exec(
            select(CartItem).where(CartItem.product_id == product_id)
        ).first()

        if quantity <= 0:
            if item:
                db.delete(item)
        elif item:
            item.quantity = quantity
        else:
            db.add(CartItem(
                product_id=product_id, quantity=quantity
            ))

        db.commit()
        return {"message": "Сохранено"}


