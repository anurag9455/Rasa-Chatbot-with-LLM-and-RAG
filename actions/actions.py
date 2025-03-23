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


#################################################################################################################################################################
## Using lallma3


# 🔽 Import the vector store
# from retrieval.vector_store import ProductVectorStore

# # 🔽 Initialize it globally to avoid rebuilding every time
# vector_store = ProductVectorStore()

# class ActionRespondWithCatalog(Action):
#     def name(self) -> Text:
#         return "action_respond_with_catalog"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         user_query = tracker.latest_message.get("text")

#         try:
#             # 🔍 Use vector DB to fetch related product info
#             matches = vector_store.search(user_query, top_k=1)
#             context = ""

#             if matches:
#                 product = matches[0]
#                 context = f"""
#                 Product Name: {product['product_name']}
#                 Brand: {product['brand']}
#                 Price: ${product['price']}
#                 Features: {product['features']}
#                                 """.strip()
#             else:
#                 context = "No matching product was found in the catalog."
#             # 👇 Get preferred language (default: English)
#             preferred_language = tracker.get_slot("language") or "english"
#             # 🧠 Send to LLaMA3 with context
#             prompt = f"""You are an expert product assistant. Also Respond in {preferred_language.title()}.Use the product info below to answer the user's question. 

#             Product Info:
#             {context}

#             User Question:
#             {user_query}

#             Answer:"""

#             payload = {
#                 "model": "llama3",
#                 "prompt": prompt
#             }

#             response = requests.post(
#                 "http://localhost:11434/api/generate",
#                 json=payload,
#                 stream=True
#             )
#             response.raise_for_status()

#             output = ""
#             for line in response.iter_lines():
#                 if line:
#                     data = json.loads(line.decode("utf-8"))
#                     output += data.get("response", "")

#             dispatcher.utter_message(text=output.strip())

#         except Exception as e:
#             print(f"\n❌ Error in action_respond_with_catalog: {e}\n")
#             dispatcher.utter_message(text="Oops! Something went wrong while fetching the catalog info.")

#         return []


# # class ActionSetLanguage(Action):
# #     def name(self) -> Text:
# #         return "action_set_language"

# #     def run(self, dispatcher: CollectingDispatcher,
# #             tracker: Tracker,
# #             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

# #         user_text = tracker.latest_message.get("text")
# #         response = f"Okay! I will now respond in your preferred language. [🔤 Multilingual mode coming soon 🚀]"

# #         dispatcher.utter_message(text=response)
# #         return []
# class ActionSetLanguage(Action):
#     def name(self) -> Text:
#         return "action_set_language"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         user_text = tracker.latest_message.get("text")
#         language = None

#         # Simple detection from keywords (could use entities later)
#         language_keywords = ["hindi", "tamil", "marathi", "bengali", "gujarati", "kannada", "english"]
#         for lang in language_keywords:
#             if lang in user_text.lower():
#                 language = lang
#                 break

#         if language:
#             dispatcher.utter_message(text=f"Got it! I’ll respond in {language.title()} from now on.")
#             return [{"event": "slot", "name": "language", "value": language}]
#         else:
#             dispatcher.utter_message(text="Sorry, I couldn’t detect the language you want to switch to.")
#             return []

############################################################################################################################################################
#Using SarvamLLM
import json
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

# 🧠 RAG vector store
from retrieval.vector_store import ProductVectorStore

# 🌐 Sarvam-1 LLM (Hugging Face)
from llm.sarvam_llm import SarvamLLM

# 🔁 Initialize once globally
vector_store = ProductVectorStore()
sarvam = SarvamLLM()

def clean_response(text: str):
    # Stop generation if it starts giving weird output
    cutoffs = ["User Question:","Q:","Question:", "A:", "Quiz", "###", "Options:", "Choose:"]
    for marker in cutoffs:
        if marker in text:
            text = text.split(marker)[0]
    return text.strip()


class ActionRespondWithCatalog(Action):
    def name(self) -> Text:
        return "action_respond_with_catalog"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_query = tracker.latest_message.get("text")
        preferred_language = tracker.get_slot("language") or "english"

        try:
            # Search the product catalog
            matches = vector_store.search(user_query, top_k=1)
            if not matches:
                dispatcher.utter_message(text="Sorry, I couldn’t find any matching product.")
                return []
            print(f"[DEBUG] vector matches: {matches}")
            print(f"[DEBUG] type of match[0]: {type(matches[0])}")

            product = matches[0]
            context = f"{product['product_name']} by {product['brand']}, priced at ${product['price']}. Features: {product['features']}."

            # 🧠 Clean prompt format
            prompt = (
            f"Context: {context}\n\n"
            f"Question: {user_query}\n"
            f"Answer in {preferred_language.title()}:"
        )
        #     prompt = (
        #     f"You're a helpful assistant. Use the product information to answer clearly in {preferred_language.title()}.\n\n"
        #     f"Product Information: {context}\n\n"
        #     f"User Question: {user_query}\n"
        #     f"Answer:"
        # )



            # # Get model response
            # raw_response = sarvam.generate_response(prompt)
            # cleaned_response = raw_response.replace(prompt, "").strip()

            # Final output
            #dispatcher.utter_message(text=cleaned_response)
            
            response_text = sarvam.generate_response(prompt)
            print(f"[DEBUG] Raw LLM response:\n{response_text}\n")

            # Ensure it's a string
            if not isinstance(response_text, str):
                print("[DEBUG] Unexpected response type from Sarvam:", type(response_text))
                dispatcher.utter_message(text="Unexpected model response format.")
                return []

            # Optional: strip prompt echo if it happens
            cleaned_response = response_text.replace(prompt, "").strip()
            cleaned_response = clean_response(cleaned_response)
            dispatcher.utter_message(text=cleaned_response)


        except Exception as e:
            print(f"❌ Error in action_respond_with_catalog: {e}")
            dispatcher.utter_message(text="Something went wrong while answering your question.")
        
        return []


class ActionSetLanguage(Action):
    def name(self) -> Text:
        return "action_set_language"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_text = tracker.latest_message.get("text")
        language = None

        language_keywords = ["hindi", "tamil", "marathi", "bengali", "gujarati", "kannada", "english"]
        for lang in language_keywords:
            if lang in user_text.lower():
                language = lang
                break

        if language:
            dispatcher.utter_message(text=f"Got it! I’ll respond in {language.title()} from now on.")
            return [{"event": "slot", "name": "language", "value": language}]
        else:
            dispatcher.utter_message(text="Sorry, I couldn’t detect the language you want to switch to.")
            return []
