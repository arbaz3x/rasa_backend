from typing import List, Dict, Any, Text
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from shared_data import carts
from db import create_order,get_guest_orders
from shared_data import carts
import random
import string

def generate_guest_id() -> str:
    # Generate a 5-character random string (letters + digits)
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=5))

# --- Guest Session Action ---
class ActionStartGuestSession(Action):
    def name(self) -> Text:
        return "action_start_guest_session"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        guest_id = generate_guest_id()
        dispatcher.utter_message(
            text=f"Your Guest ID is: {guest_id}\n"
                 "Please save this ID to access your orders later.\n"
                 "This is a retail store, we have accessories and clothing"
        )
        return [SlotSet("guest_id", guest_id)]
class ActionCheckout(Action):
    def name(self) -> Text:
        return "action_checkout"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        guest_id = tracker.get_slot("guest_id")
        if not guest_id:
            dispatcher.utter_message(text="Please start a guest session first.")
            return []

        if guest_id in carts and carts[guest_id]:
            order_items = carts[guest_id].copy()  # Save a copy before clearing
            order_id = create_order(guest_id, order_items, "Processing")  # Use guest_id here
            carts[guest_id] = []  # Clear cart after saving order
            cart_items = [f"{item['name']} (${item['price']})" for item in order_items]
            total = sum(float(item['price']) for item in order_items)
            dispatcher.utter_message(
                text="Your order has been placed!\n" +
                     "Order #" + order_id + "\n" +
                     "Items:\n" + "\n".join(cart_items) +
                     f"\nTotal: ${total:.2f}\nThank you for shopping with us!"
            )
        else:
            dispatcher.utter_message(text="Your cart is empty.")
        return []



class ActionTrackOrder(Action):
    def name(self) -> Text:
        return "action_track_order"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        guest_id = tracker.get_slot("guest_id")
        if not guest_id:
            dispatcher.utter_message(text="Please provide your Guest ID.")
            return []

        user_orders = get_guest_orders(guest_id)  # Use get_guest_orders, not get_user_orders
        if user_orders:
            order_list = []
            for order in user_orders:
                items = ", ".join([f"{item['product_name']} (x{item['quantity']})" for item in order['items']])
                order_list.append(
                    f"Order #{order['order_id']} ({order['order_date']}): {items} - Status: {order['status']}"
                )
            dispatcher.utter_message(text="Your orders:\n" + "\n".join(order_list))
        else:
            dispatcher.utter_message(text="You have no orders yet.")
        return []

