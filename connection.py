import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


async def connection_db():
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        return conn
    except Exception as error:
        print(f"Connection error: {error}")
        return None
    
async def create_table():
    conn = await connection_db()
    try:
        await conn.execute("""
    create table if not exists products (
        products_id serial primary key,
        telegram_id varchar(200),
        name varchar(255) not null,
        price int check (price > 0),
        description text,
        photo_file_id text,
        status varchar(10) default 'active' check (status = 'active' or status = 'sold'),
        created_at timestamp default now()
    );
    create table if not exists saved_products (
        saved_products_id serial primary key,
        user_id varchar(200) not null,
        product_id int references products(products_id),
        saved_at timestamp default now(),
        unique (user_id, product_id)
    );
""")

        print("Create table successfully!")
        return conn
    except Exception as error:
        print(f"Create table error: {error}")
    finally:
        await conn.close()