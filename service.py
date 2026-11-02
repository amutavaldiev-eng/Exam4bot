from connection import connection_db




async def add_product(telegram_id, name, price, description, photo_file_id):
    conn = await connection_db()
    try:
        await conn.execute("""
            insert into products (telegram_id, name, price, description, photo_file_id)
            values ($1, $2, $3, $4, $5)
        """, str(telegram_id), name, price, description, photo_file_id)
        return True
    except Exception as error:
        print(f"Add product error: {error}")
        return False
    finally:
        await conn.close()

        
        
        
async def get_all_products():
    conn = await connection_db()
    try:
        products = await conn.fetch("""
            select * from products
            where status = 'active'
        """)
        return products
    except Exception as error:
        print(f"Get all products error: {error}")
    finally:
        await conn.close()
        
    
    
async def get_product_by_id(product_id):
    conn = await connection_db()
    try:
        product = await conn.fetchrow("""
            select * from products
            where products_id = $1
        """, product_id)
        return product
    except Exception as error:
        print(f"get product error: {error}")
    finally:
        await conn.close()
        



async def get_my_products(user_id):
    conn = await connection_db()
    try:
        products = await conn.fetch("""
            select * from products
            where telegram_id = $1 and status = 'active'
        """, str(user_id))
        return products
    except Exception as error:
        print(f"Get my products error: {error}")
    finally:
        await conn.close()
        
async def save_product(user_id, product_id):
    conn = await connection_db()
    try:
        product = await conn.fetchrow("""
            select * from products
            where products_id = $1 and status = 'active'
        """, product_id)
        if not product:
            return "not_found"


        if str(user_id) == product["telegram_id"]:
            return "own_product"

        exists = await conn.fetchrow("""
            select * from saved_products
            where user_id = $1 and product_id = $2
        """, str(user_id), product_id)
        
        if exists:
            return "already_saved"
        
        
        await conn.execute("""
            insert into saved_products (user_id, product_id)
            values ($1, $2)
        """, str(user_id), product_id)
        return "success"
    except Exception as error:
        print(f"Save product error: {error}")
        return "error"
    finally:
        await conn.close()
        
        
        
async def get_saved_products(user_id):
    conn = await connection_db()
    try:
        products = await conn.fetch("""
            select products.* from products
            join saved_products on saved_products.product_id = products.products_id
            where saved_products.user_id = $1
        """, str(user_id))
        return products
    except Exception as error:
        print(f"Get saved products error: {error}")
    finally:
        await conn.close()
        
        



async def mark_product_sold(user_id, product_id):
    conn = await connection_db()
    try:
        result = await conn.execute("""
            update products
            set status = 'sold'
            where products_id = $1 and telegram_id = $2
        """, product_id, str(user_id))
        return result
    except Exception as error:
        print(f"Mark product {error}")
    finally:
        await conn.close()
        
        
async def delete_saved_product(user_id, product_id):
    conn = await connection_db()
    try:
        result = await conn.execute("""
            delete from saved_products
            where user_id = $1 and product_id = $2
        """, str(user_id), product_id)
        
        return result == "DELETE 1"
    except Exception as error:
        print(f"Delete saved product error: {error}")   
    finally:
        await conn.close()