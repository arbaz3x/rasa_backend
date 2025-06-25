from typing import Optional
from db.connection import get_connection

def create_cart(user_id: int) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO carts (user_id) VALUES (%s) RETURNING id;",
        (user_id,)
    )
    cart_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return cart_id

def get_active_cart(user_id: int) -> Optional[int]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM carts WHERE user_id = %s ORDER BY created_at DESC LIMIT 1;", (user_id,))
    cart = cur.fetchone()
    cur.close()
    conn.close()
    return cart[0] if cart else None

def add_to_cart(cart_id: int, product_id: int, quantity: int = 1) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO cart_items (cart_id, product_id, quantity) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING;",
        (cart_id, product_id, quantity)
    )
    conn.commit()
    cur.close()
    conn.close()
