from typing import Optional, Tuple,Dict,Any
from psycopg2 import Error
from db.connection import get_connection

def create_user(username: str, password_hash: str, email: str) -> int:
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO users (username, password_hash, email) VALUES (%s, %s, %s) RETURNING id;",
            (username, password_hash, email)
        )
        user_id = cur.fetchone()[0]
        conn.commit()
        return user_id
    except Error as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()

def get_user_by_username(username: str) -> Optional[Tuple]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s;", (username,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user

def get_user_profile(user_id: int) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT id, username, email FROM users WHERE id = %s;",
            (user_id,)
        )
        user = cur.fetchone()
        if user:
            return {
                "id": user[0],
                "username": user[1],
                "email": user[2]
            }
        return None
    except Error as e:
        raise e
    finally:
        cur.close()
        conn.close()

