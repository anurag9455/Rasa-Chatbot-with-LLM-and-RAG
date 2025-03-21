# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []





# from typing import Any, Text, Dict, List
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
# import requests

# class ActionRespondWithCatalog(Action):
#     def name(self) -> Text:
#         return "action_respond_with_catalog"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         user_query = tracker.latest_message.get("text")

#         # 👇 (Eventually: Query RAG system & LLM here)
#         # For now, we just return a mock response
#         response = f"You asked about: {user_query}. [Catalog response will go here 🔍📚]"

#         dispatcher.utter_message(text=response)
#         return []

# class ActionSetLanguage(Action):
#     def name(self) -> Text:
#         return "action_set_language"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         user_text = tracker.latest_message.get("text")
#         response = f"Okay! I will now respond in your preferred language. [🔤 Multilingual mode coming soon 🚀]"

#         dispatcher.utter_message(text=response)
#         return []



import json
import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from typing import Any, Text, Dict, List


# class ActionRespondWithCatalog(Action):
#     def name(self) -> Text:
#         return "action_respond_with_catalog"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         user_query = tracker.latest_message.get("text")

#         # Payload for Ollama
#         payload = {
#             "model": "llama3",
#             "prompt": f"You are a helpful assistant. Answer the following query clearly:\n\n{user_query}"
#         }

#         try:
#             response = requests.post(
#                 "http://localhost:11434/api/generate",
#                 json=payload,
#                 stream=True
#             )
#             response.raise_for_status()

#             # Process streamed response safely
#             output = ""
#             for line in response.iter_lines():
#                 if line:
#                     data = json.loads(line.decode("utf-8"))
#                     output += data.get("response", "")

#             dispatcher.utter_message(text=output.strip())

#         except Exception as e:
#             print(f"\n❌ Error calling Ollama: {e}\n")
#             dispatcher.utter_message(text="Sorry, I couldn’t fetch the catalog info at the moment.")

#         return []

# 🔽 Import the vector store
from retrieval.vector_store import ProductVectorStore

# 🔽 Initialize it globally to avoid rebuilding every time
vector_store = ProductVectorStore()

class ActionRespondWithCatalog(Action):
    def name(self) -> Text:
        return "action_respond_with_catalog"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_query = tracker.latest_message.get("text")

        try:
            # 🔍 Use vector DB to fetch related product info
            matches = vector_store.search(user_query, top_k=1)
            context = ""

            if matches:
                product = matches[0]
                context = f"""
                Product Name: {product['product_name']}
                Brand: {product['brand']}
                Price: ${product['price']}
                Features: {product['features']}
                                """.strip()
            else:
                context = "No matching product was found in the catalog."

            # 🧠 Send to LLaMA3 with context
            prompt = f"""You are an expert product assistant. Use the product info below to answer the user's question.

            Product Info:
            {context}

            User Question:
            {user_query}

            Answer:"""

            payload = {
                "model": "llama3",
                "prompt": prompt
            }

            response = requests.post(
                "http://localhost:11434/api/generate",
                json=payload,
                stream=True
            )
            response.raise_for_status()

            output = ""
            for line in response.iter_lines():
                if line:
                    data = json.loads(line.decode("utf-8"))
                    output += data.get("response", "")

            dispatcher.utter_message(text=output.strip())

        except Exception as e:
            print(f"\n❌ Error in action_respond_with_catalog: {e}\n")
            dispatcher.utter_message(text="Oops! Something went wrong while fetching the catalog info.")

        return []


class ActionSetLanguage(Action):
    def name(self) -> Text:
        return "action_set_language"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_text = tracker.latest_message.get("text")
        response = f"Okay! I will now respond in your preferred language. [🔤 Multilingual mode coming soon 🚀]"

        dispatcher.utter_message(text=response)
        return []
