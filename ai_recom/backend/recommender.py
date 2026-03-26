from ai_recom.backend.content_based import recommend_products as content_recommend
from ai_recom.backend.collaborative_based import recommend_products as collaborative_recommend
from ai_recom.backend.rating_based import recommend_top_rated
import pandas as pd


def get_recommendations(user_id: int, product_name: str, top_n=10):

    try:
        # 🔹 NEW USER → TOP RATED
        if user_id == 0 or not product_name:
            result = recommend_top_rated(top_n)

            # ✅ ENSURE DATAFRAME
            if isinstance(result, list):
                result = pd.DataFrame(result)

            return result.head(top_n)

        # 🔹 CONTENT BASED
        content_df = content_recommend(product_name, top_n)

        # 🔹 COLLABORATIVE
        collab_df = collaborative_recommend(user_id, top_n)

        # ✅ FORCE DATAFRAME (IMPORTANT FIX)
        if isinstance(content_df, list):
            content_df = pd.DataFrame(content_df)

        if isinstance(collab_df, list):
            collab_df = pd.DataFrame(collab_df)

        # 🔥 ADD SOURCE TAG
        if not content_df.empty:
            content_df["source"] = "content"

        if not collab_df.empty:
            collab_df["source"] = "collab"

        # 🔥 COMBINE
        combined = pd.concat([content_df, collab_df], ignore_index=True)

        # 🔥 REMOVE DUPLICATES
        if "ProductID" in combined.columns:
            combined = combined.drop_duplicates(subset=["ProductID"])
        else:
            combined = combined.drop_duplicates()

        # 🔥 SORT BY RATING
        if "Rating" in combined.columns:
            combined["Rating"] = pd.to_numeric(combined["Rating"], errors="coerce")
            combined = combined.sort_values(by="Rating", ascending=False)

        # 🔥 PRIORITY LOGIC
        if "source" in combined.columns:
            combined["priority"] = combined["source"].map({
                "content": 2,
                "collab": 1
            })
            combined = combined.sort_values(by=["priority", "Rating"], ascending=False)

        # 🔥 FINAL LIMIT
        combined = combined.head(top_n)

        return combined

    except Exception as e:
        print("Recommender error:", e)
        return pd.DataFrame()