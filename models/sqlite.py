from pydantic import BaseModel
import aiosqlite
from typing import List
import asyncio

class User(BaseModel):
    id: int
    name: str
    email: str


DATABASE_URL = 'sqlite.db'

async def init_db():
    async with aiosqlite.connect(DATABASE_URL) as db:
        await db.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT,
            email TEXT
        )
        ''')
        await db.commit()

async def create_user(user: User):
    async with aiosqlite.connect(DATABASE_URL) as db:
        await db.execute('''
        INSERT INTO users (id, name, email)
        VALUES (?, ?, ?)
        ''', (user.id, user.name, user.email))
        await db.commit()

async def get_user(user_id: int) -> User:
    async with aiosqlite.connect(DATABASE_URL) as db:
        async with db.execute('SELECT id, name, email FROM users WHERE id = ?', (user_id,)) as cursor:
            row = await cursor.fetchone()
            if row:
                return User(id=row[0], name=row[1], email=row[2])
            return None

async def get_users() -> List[User]:
    async with aiosqlite.connect(DATABASE_URL) as db:
        async with db.execute('SELECT id, name, email FROM users') as cursor:
            rows = await cursor.fetchall()
            return [User(id=row[0], name=row[1], email=row[2]) for row in rows]


# // Product

class Product(BaseModel):
    id: int
    name: str
    price: float

async def init_db_product():
    async with aiosqlite.connect(DATABASE_URL) as db:
        await db.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT,
            price REAL
        )
        ''')
        await db.commit()



async def create_product(product: Product):
    async with aiosqlite.connect(DATABASE_URL) as db:
        await db.execute('''
        INSERT INTO products (id, name, price)
        VALUES (?, ?, ?)
        ''', (product.id, product.name, product.price))
        await db.commit()

async def get_product(product_id: int) -> Product:
    async with aiosqlite.connect(DATABASE_URL) as db:
        async with db.execute('SELECT id, name, price FROM products WHERE id = ?', (product_id,)) as cursor:
            row = await cursor.fetchone()
            if row:
                return Product(id=row[0], name=row[1], price=row[2])
            return None

async def get_products() -> List[Product]:
    async with aiosqlite.connect(DATABASE_URL) as db:
        async with db.execute('SELECT id, name, price FROM products') as cursor:
            rows = await cursor.fetchall()
            return [Product(id=row[0], name=row[1], price=row[2]) for row in rows]