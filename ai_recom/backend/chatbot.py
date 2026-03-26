import os
from dotenv import load_dotenv
from groq import Groq
from ai_recom.backend.recommender import get_recommendations

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

# ✅ check if key exists
if not api_key:
    raise ValueError("GROQ_API_KEY not found in .env file")

client = Groq(api_key=api_key)


def get_chatbot_response(user_input: str, user_id: int = 0):

    try:
        query = user_input.lower()

        # 🛍️ PRODUCT KEYWORDS
        product_keywords = [
            "soap", "shampoo", "lotion", "cream",
            "face wash", "perfume", "cosmetics"
        ]

        # 🔥 PRODUCT INTENT
        if any(word in query for word in product_keywords):

            print("🛒 Product intent detected")

            # 🔹 Get recommendations
            products = get_recommendations(user_id, query, top_n=20)

            # 🔹 Convert to list if dataframe
            if hasattr(products, "to_dict"):
                products = products.to_dict("records")

            # 🔥 SMART FILTER
            keywords = query.split()

            filtered = [
                p for p in products
                if any(k in p.get("Name", "").lower() for k in keywords)
            ]

            # 🔹 fallback if nothing found
            if not filtered:
                filtered = products[:5]

            # 🔹 return only product names (for your current UI)
            product_names = [p.get("Name", "Unknown") for p in filtered[:5]]

            return {
                "type": "text",
                "data": "Here are some products:\n\n" + "\n".join(product_names)
            }

        # 💬 NORMAL CHAT → LLM
        chat = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful shopping assistant. "
                        "Do NOT generate fake product names. "
                        "Keep answers short and useful."
                    )
                },
                {"role": "user", "content": user_input}
            ],
            model="llama-3.1-8b-instant"
        )

        return {
            "type": "text",
            "data": chat.choices[0].message.content or "No response"
        }

    except Exception as e:
        print("Chatbot Error:", e)

        return {
            "type": "text",
            "data": "Sorry, something went wrong."
        }