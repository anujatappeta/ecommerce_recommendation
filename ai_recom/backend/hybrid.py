import pandas as pd

from ai_recom.backend.content_based import get_content_recommendations
from ai_recom.backend.collaborative_based import get_collaborative_recommendations


# -------------------------
# HYBRID FUNCTION
# -------------------------
def get_hybrid_recommendations(user_id, product_id, top_n=10):
    try:
        # 🔥 Get content-based recommendations
        content_ids = get_content_recommendations(product_id, top_n)

        # 🔥 Get collaborative recommendations
        collab_ids = get_collaborative_recommendations(user_id, top_n)

        # -------------------------
        # COMBINE RESULTS
        # -------------------------
        combined = []

        # Priority: content first (more relevant)
        for pid in content_ids:
            if pid not in combined:
                combined.append(pid)

        for pid in collab_ids:
            if pid not in combined:
                combined.append(pid)

        # Limit results
        return combined[:top_n]

    except Exception as e:
        print("Error in hybrid:", e)
        return []