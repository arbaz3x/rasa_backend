from typing import List, Dict, Any, Text
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
# cart_actions.py
from db.product import get_product_info
from db.connection import get_connection
from shared_data import carts

class ActionOfferToAddToCart(Action):
    def name(self) -> Text:
        return "action_offer_to_add_to_cart"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        product_name = next(tracker.get_latest_entity_values("product"), None)
        if product_name:
            product_info = get_product_info(product_name)
            if product_info:
                dispatcher.utter_message(
                    text=f"Here is {product_info['name']}, priced at ${product_info['price']}.\n"
                         "Would you like to add this to your cart?",
                    buttons=[
                        {"title": "Yes", "payload": f'/add_to_cart{{"product": "{product_info["name"]}"}}'},
                        {"title": "No", "payload": "/deny"}
                    ]
                )
                return []
            else:
                dispatcher.utter_message(text=f"Sorry, we don't have {product_name} in our product list.")
        else:
            dispatcher.utter_message(text="Please specify which product you want to buy.")
        return []

class ActionAddToCart(Action):
    def name(self) -> Text:
        return "action_add_to_cart"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        product_name = next(tracker.get_latest_entity_values("product"), None)
        guest_id = tracker.get_slot("guest_id")
        if not guest_id:
         dispatcher.utter_message(text="Please start a guest session first.")
        
        print(f"[AddToCart] guest_id={guest_id} cart={carts.get(guest_id)}") 
        add_more = tracker.get_slot("add_more")
        if product_name:
            product_info = get_product_info(product_name)
            if product_info:
                cart = carts.setdefault(guest_id, [])
                for item in cart:
                    if item['id'] == product_info['id']:
                        if add_more:
                            item['quantity'] += 1
                            print(f"[AddToCart] after quantity update: guest_id={guest_id} cart={carts.get(guest_id)}")
                            dispatcher.utter_message(
                                text=f"Added another {product_info['name']} to your cart. Now you have {item['quantity']}."
                            )
                        else:
                            dispatcher.utter_message(
                                text=f"{product_info['name']} is already in your cart. Would you like to add another?",
                                buttons=[
                                    {"title": "Yes, add one more", "payload": f'/add_to_cart{{"product": "{product_info["name"]}", "add_more": true}}'},
                                    {"title": "No, view cart", "payload": "/show_cart"}
                                ]
                            )
                        return [SlotSet("product", None), SlotSet("add_more", None)]
                # Not in cart: add new
                cart.append({
                    "id": product_info["id"],
                    "name": product_info["name"],
                    "price": product_info["price"],
                    "quantity": 1
                })
                print(f"[AddToCart] after update: guest_id={guest_id} cart={carts.get(guest_id)}")
                dispatcher.utter_message(
                    text=f"{product_info['name']} has been added to your cart.",
                    buttons=[
                        {"title": "Shop more", "payload": "/ask_products"},
                        {"title": "View cart", "payload": "/show_cart"},
                        {"title": "Checkout", "payload": "/checkout"}
                    ]
                )
                return [SlotSet("product", None), SlotSet("add_more", None)]
            else:
                dispatcher.utter_message(text=f"Sorry, we don't have {product_name} in our product list.")
        else:
            dispatcher.utter_message(text="Please specify which product you want to add to your cart.")
        return []



class ActionShowCart(Action):
    def name(self) -> Text:
        return "action_show_cart"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        guest_id = tracker.get_slot("guest_id")
        print(f"[ACTIONshowCART] guest_id={guest_id} cart={carts.get(guest_id)}") 
        if guest_id in carts and carts[guest_id]:
            cart_items = [f"{item['name']} (${item['price']})" for item in carts[guest_id]]
            dispatcher.utter_message(text="Your cart:\n" + "\n".join(cart_items))
        else:
            dispatcher.utter_message(text="Your cart is empty.")
        return []

class ActionRemoveFromCart(Action):
    def name(self) -> Text:
        return "action_remove_from_cart"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        product_name = next(tracker.get_latest_entity_values("product"), None)
        guest_id = tracker.get_slot("guest_id")
        if product_name and guest_id in carts:
            cart = carts[guest_id]
            new_cart = [item for item in cart if item['name'].lower() != product_name.lower()]
            carts[guest_id] = new_cart
            dispatcher.utter_message(text=f"{product_name} has been removed from your cart.")
        else:
            dispatcher.utter_message(text="That product is not in your cart.")
        return []

class ActionUpdateCartQuantity(Action):
    def name(self) -> Text:
        return "action_update_cart_quantity"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Implementation for updating quantity
        # You can prompt user for quantity and update the cart accordingly
        dispatcher.utter_message(text="Feature coming soon: update cart quantities.")
        return []

class ActionDefaultFallback(Action):
    def name(self) -> Text:
        return "action_default_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            text="Sorry, I didn't understand that. You can ask to see products, view your cart, or get help.",
            buttons=[
                {"title": "Show products", "payload": "/ask_products"},
                {"title": "View cart", "payload": "/show_cart"},
                {"title": "Help", "payload": "/faq_contact"}
            ]
        )
        return []

