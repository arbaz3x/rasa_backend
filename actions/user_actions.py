from typing import List, Dict, Any, Text
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from db.user import  get_user_profile

class ActionUpdateProfile(Action):
    def name(self) -> Text:
        return "action_update_profile"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Example: Update user profile based on slots or entities
        user_id = tracker.sender_id
        # Get profile data from slots or entities
        # update_user_profile(user_id, ...)
        dispatcher.utter_message(text="Your profile has been updated.")
        return []

class ActionShowProfile(Action):
    def name(self) -> Text:
        return "action_show_profile"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_id = tracker.sender_id
        profile = get_user_profile(user_id)
        if profile:
            dispatcher.utter_message(text=f"Your profile: {profile}")
        else:
            dispatcher.utter_message(text="No profile found.")
        return []
