from ai_recom.backend.content_based import get_content_recommendations
from ai_recom.backend.collaborative_based import get_collaborative_recommendations
from ai_recom.backend.rating_based import get_top_rated

def get_recommendations(user_id: int, product_id: int, top_n=10):
    try:
        # 🔹 NEW USER → TOP RATED
        if user_id == 0 or product_id == 0:
            return get_top_rated(top_n)

        # 🔹 CONTENT BASED
        content_ids = get_content_recommendations(product_id, top_n)

        # 🔹 COLLABORATIVE
        collab_ids = get_collaborative_recommendations(user_id, top_n)

        #  HYBRID COMBINATION
        combined = []

        # Priority: content first
        for pid in content_ids:
            if pid not in combined:
                combined.append(pid)

        for pid in collab_ids:
            if pid not in combined:
                combined.append(pid)

        # 🔹 FALLBACK
        if not combined:
            return get_top_rated(top_n)

        return combined[:top_n]

    except Exception as e:
        print("Recommender error:", e)
        return []