from typing import List, Dict, Any, Text
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from db.product import get_all_products_price, get_product_info,get_all_categories,get_products_by_category

class ActionFetchProducts(Action):
    def name(self) -> Text:
        return "action_fetch_products"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        products = get_all_products_price()
        if not products:
            dispatcher.utter_message(text="No products found.")
            return []
        dispatcher.utter_message(text="Here are all our products:")
        for product in products:
            message = f"Name: {product['name']}\nPrice: ${product['price']}\nCategory: {product['category']}\n"
            dispatcher.utter_message(text=message)
        return []

class ActionShowAllProducts(Action):
    def name(self) -> Text:
        return "action_show_all_products"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        products = get_all_products_price()
        if products:
            dispatcher.utter_message(text="Here are our products:")
            for product in products:
                message = f"Name: {product['name']}\nPrice: ${product['price']}\nCategory: {product['category']}"
                dispatcher.utter_message(text=message)
        else:
            dispatcher.utter_message(text="No products found.")
        return []

class ActionFetchProductInfo(Action):
    def name(self) -> str:
        return "action_fetch_product_info"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        product = next(tracker.get_latest_entity_values("product"), None)
        if product is None:
            product = "the product you mentioned"
        dispatcher.utter_message(text=f"Here is information about {product}.")
        return []

class ActionGetRecommendation(Action):
    def name(self) -> Text:
        return "action_get_recommendation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        product_name = next(tracker.get_latest_entity_values("product"), None)
        if product_name:
            product_info = get_product_info(product_name)
            if product_info:
                recommendation = (
                    f"We have {product_info['name']} in our collection! "
                    f"It is a {product_info['category']}."
                )
            else:
                recommendation = f"Sorry, we don't have {product_name} in our product list."
        else:
            recommendation = "Here are some of our top recommendations!"
        dispatcher.utter_message(text=recommendation)
        return []
    
class ActionFetchProductsByCategory(Action):
    def name(self) -> Text:
        return "action_fetch_products_by_category"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Get the category entity from the user input
        category = next(tracker.get_latest_entity_values("category"), None)

        # Standardize category value for matching (lowercase, strip spaces)
        if category:
            category = category.strip().lower()

        # Get all available categories from the database, standardized
        categories = get_all_categories()
        standardized_categories = [c.strip().lower() for c in categories]

        # If no category provided, list available categories
        if not category:
            if categories:
                dispatcher.utter_message(
                    text=f"We have products in these categories: {', '.join(categories)}. Which category would you like to explore?"
                )
            else:
                dispatcher.utter_message(
                    text="Sorry, we don't have any product categories defined."
                )
            return []

        # If category provided but not found, provide a fallback
        if category not in standardized_categories:
            dispatcher.utter_message(
                text=f"Sorry, we don't have a category called '{category}'. Available categories are: {', '.join(categories)}."
            )
            return []

        # If category found, fetch and list products in that category
        # (Pass the original category name as stored in the DB for display)
        matched_category = categories[standardized_categories.index(category)]
        products = get_products_by_category(matched_category)
        if products:
            dispatcher.utter_message(
                text=f"Here are our products in the {matched_category} category:"
            )
            for product in products:
                message = f"Name: {product['name']}\nPrice: ${product['price']}\nCategory: {product['category']}\n"
                dispatcher.utter_message(text=message)
        else:
            dispatcher.utter_message(
                text=f"Sorry, we don't have any products in the {matched_category} category."
            )
        return []


