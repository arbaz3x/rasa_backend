from db.connection import get_connection
from typing import Optional, Dict, Any, List


def get_all_products_price() -> List[Dict[str, Any]]:
    """Get all products for display or management."""
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT name, price, category FROM products")
            rows = cursor.fetchall()
            return [
                {"name": name, "price": price, "category": category}
                for (name, price, category) in rows
            ]



def get_product_info(product_name: str) -> Optional[Dict[str, Any]]:
    """Get product info by name."""
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM products WHERE LOWER(name) = LOWER(%s)", (product_name,))
            row = cursor.fetchone()
            if row:
                return {
                    "id": row[0],
                    "name": row[1],
                    "category": row[2],
                    "description": row[3],
                    "price": row[4],
                    "color": row[5],
                    "size": row[6],
                    "stock": row[7],
                    "image_url": row[8]
                }
    return None

def add_product(name: str, category: str, description: str, price: float, color: str, size: str, stock: int, image_url: str):
    """Add a new product to the database."""
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO products (name, category, description, price, color, size, stock, image_url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (name, category, description, price, color, size, stock, image_url)
            )
        conn.commit()

def get_all_product_names():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM products;")
    names = [row[0] for row in cursor.fetchall()]
    conn.close()
    # Return as a single string, comma-separated
    return ", ".join(names)

def get_products_by_category(category: str) -> List[Dict[str, Any]]:
    """Get all products in a specific category."""
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT name, price, category FROM products WHERE LOWER(category) = LOWER(%s)", (category,))
            rows = cursor.fetchall()
            return [
                {"name": name, "price": price, "category": category}
                for (name, price, category) in rows
            ]

def get_all_categories() -> List[str]:
    """Get all unique product categories."""
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT DISTINCT category FROM products")
            rows = cursor.fetchall()
            return [row[0] for row in rows]

