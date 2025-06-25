from typing import List, Dict, Any, Text
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from db.conversation import insert_conversation, get_conversation_history

class ActionLogConversation(Action):
    def name(self) -> Text:
        return "action_log_conversation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_id = tracker.sender_id
        session_id = tracker.sender_id  # or use a session ID if you generate one
        user_message = tracker.latest_message.get("text", "")
        intent = tracker.latest_message.get("intent", {}).get("name", "")
        entities = tracker.latest_message.get("entities", {})
        # Get the last bot response from the tracker
        bot_response = ""
        for event in reversed(tracker.events):
            if event.get("event") == "bot":
                bot_response = event.get("text", "")
                break
        insert_conversation(user_id, session_id, user_message, bot_response, intent, entities)
        return []

class ActionShowConversationHistory(Action):
    def name(self) -> Text:
        return "action_show_conversation_history"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_id = tracker.sender_id
        history = get_conversation_history(user_id)
        if history:
            history_list = [f"Q: {h['user_message']}\nA: {h['bot_response']}" for h in history]
            dispatcher.utter_message(text="Your conversation history:\n" + "\n\n".join(history_list))
        else:
            dispatcher.utter_message(text="No conversation history found.")
        return []
