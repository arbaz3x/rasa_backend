from db.connection import get_connection
from typing import List, Dict, Any
import uuid

def create_order(guest_id: str, items: List[Dict[str, Any]], status: str) -> str:
    conn = None
    cur = None
    order_id = str(uuid.uuid4())
    try:
        conn = get_connection()
        cur = conn.cursor()
        # Insert order header
        cur.execute(
            "INSERT INTO orders (order_id, guest_id, order_date, status) VALUES (%s, %s, CURRENT_DATE, %s)",
            (order_id, guest_id, status)
        )
        # Insert order items
        for item in items:
            cur.execute(
                "INSERT INTO order_items (order_id, product_name, price, quantity) VALUES (%s, %s, %s, %s)",
                (order_id, item['name'], item['price'], item.get('quantity', 1))
            )
        conn.commit()
    except Exception as e:
        print(f"Error creating order: {e}")
        if conn:
            conn.rollback()
        raise
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
    return order_id

def get_user_orders(user_id: str) -> List[Dict[str, Any]]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT o.order_id, o.order_date, o.status, oi.product_name, oi.price, oi.quantity
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        WHERE o.user_id = %s
        ORDER BY o.order_date DESC
        """,
        (user_id,)
    )
    rows = cur.fetchall()
    orders = {}
    for row in rows:
        order_id, order_date, status, product_name, price, quantity = row
        if order_id not in orders:
            orders[order_id] = {
                "order_id": order_id,
                "order_date": order_date.strftime("%Y-%m-%d"),
                "status": status,
                "items": []
            }
        orders[order_id]["items"].append({
            "product_name": product_name,
            "price": price,
            "quantity": quantity
        })
    cur.close()
    conn.close()
    return list(orders.values())
from typing import List, Dict, Any

def get_guest_orders(guest_id: str) -> List[Dict[str, Any]]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT o.order_id, o.order_date, o.status, oi.product_name, oi.price, oi.quantity
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        WHERE o.guest_id = %s
        ORDER BY o.order_date DESC
        """,
        (guest_id,)
    )
    rows = cur.fetchall()
    orders = {}
    for row in rows:
        order_id, order_date, status, product_name, price, quantity = row
        if order_id not in orders:
            orders[order_id] = {
                "order_id": order_id,
                "order_date": order_date.strftime("%Y-%m-%d"),
                "status": status,
                "items": []
            }
        orders[order_id]["items"].append({
            "product_name": product_name,
            "price": price,
            "quantity": quantity
        })
    cur.close()
    conn.close()
    return list(orders.values())
