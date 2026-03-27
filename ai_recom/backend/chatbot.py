import os
from dotenv import load_dotenv
from groq import Groq
import pandas as pd

from ai_recom.backend.recommender import get_recommendations

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    print("❌ GROQ_API_KEY missing")
else:
    print("✅ GROQ API Loaded")

client = Groq(api_key=api_key)


def get_chatbot_response(user_input: str, user_id: int = 0):

    try:
        query = user_input.lower()

        #  PRODUCT KEYWORDS
        product_keywords = [
            "soap", "shampoo", "lotion", "cream",
            "face wash", "perfume", "cosmetics"
        ]

        #  PRODUCT INTENT
        if any(word in query for word in product_keywords):

            print("🛒 Product intent detected")

            try:
                # STEP 1: get product IDs
                ids = get_recommendations(user_id, query, top_n=20)

                #  STEP 2: load dataset
                df = pd.read_csv("final_clean_data.csv")

                # STEP 3: filter products by IDs
                products = df[df["ProductID"].isin(ids)]

                #  STEP 4: convert to dict
                products = products.to_dict("records")

            except Exception as e:
                print("❌ Recommendation Error:", e)
                return {
                    "type": "text",
                    "data": "Error loading products"
                }

            #  FILTER BASED ON USER QUERY
            keywords = query.split()

            filtered = [
                p for p in products
                if any(k in p.get("Name", "").lower() for k in keywords)
            ]

            # fallback
            if not filtered:
                filtered = products[:5]

            product_names = [p.get("Name", "Unknown") for p in filtered[:5]]

            return {
                "type": "text",
                "data": "Here are some products:\n\n" + "\n".join(product_names)
            }

        #  NORMAL CHAT → LLM
        try:
            chat = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful shopping assistant. Keep answers short."
                    },
                    {"role": "user", "content": user_input}
                ],
                model="llama-3.1-8b-instant"
            )

            response_text = chat.choices[0].message.content

            if not response_text:
                return {
                    "type": "text",
                    "data": "No response from AI"
                }

            return {
                "type": "text",
                "data": response_text
            }

        except Exception as e:
            print("❌ GROQ API Error:", e)
            return {
                "type": "text",
                "data": "AI service not working"
            }

    except Exception as e:
        print("❌ Chatbot Full Error:", e)

        return {
            "type": "text",
            "data": f"Error: {str(e)}"
        }