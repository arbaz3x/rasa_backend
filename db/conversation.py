from db.connection import get_connection
import json
from typing import Optional, Dict, Any, List

def insert_conversation(user_id: str, session_id: str, user_message: str, bot_response: str, intent: str, entities: Dict[str, Any]):
    """Insert a conversation record."""
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO conversations (user_id, session_id, user_message, bot_response, intent, entities) VALUES (%s, %s, %s, %s, %s, %s)",
                (user_id, session_id, user_message, bot_response, intent, json.dumps(entities))
            )
        conn.commit()

def get_conversation_history(user_id: str) -> List[Dict[str, Any]]:
    """Retrieve conversation history for a user."""
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT user_message, bot_response, intent, entities FROM conversations WHERE user_id = %s ORDER BY created_at DESC LIMIT 10",
                (user_id,)
            )
            rows = cursor.fetchall()
            return [
                {
                    "user_message": row[0],
                    "bot_response": row[1],
                    "intent": row[2],
                    "entities": json.loads(row[3]) if row[3] else {}
                }
                for row in rows
            ]
