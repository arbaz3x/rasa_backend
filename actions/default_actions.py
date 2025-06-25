# default_actions.py
from typing import List, Dict, Any, Text
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionDefaultFallback(Action):
    def name(self) -> str:
        return "action_default_fallback"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        dispatcher.utter_message(text="Sorry, I didn't understand that. Can you please rephrase your question or ask about shipping, returns, or contact information?")
        return []

class ActionHandoffToHuman(Action):
    def name(self) -> str:
        return "action_handoff_to_human"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        dispatcher.utter_message(text="Let me connect you to a human agent. Please wait... (This is a demo; in a real app, you would notify your support team here.)")
        return []
