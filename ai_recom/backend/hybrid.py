import pandas as pd
from ai_recom.backend.content_based import recommend_products as content_recommend
from ai_recom.backend.collaborative_based import recommend_products as collaborative_recommend
from ai_recom.backend.content_based import df
def hybrid_recommend(user_id, product_name, top_n=10):

    content_results = content_recommend(product_name, top_n)
    collaborative_results = collaborative_recommend(user_id, top_n)

    combined = pd.concat([content_results, collaborative_results])
    combined = combined.drop_duplicates().head(top_n)

    return combined


if __name__ == "__main__":

    result = hybrid_recommend(user_id=1, product_name="LIPSTICK", top_n=5)

    print(result)
# ===== DO NOT MODIFY ABOVE CODE =====

from ai_recom.backend.content_based import df   

def get_hybrid_recommendations(user_id, product_id, top_n=10):

    try:
        match = df[df["ProductID"] == product_id]

        if match.empty:
            return []

        product_name = match.iloc[0]["Name"]

        result_df = hybrid_recommend(user_id, product_name, top_n)

        if result_df.empty:
            return []

        rec_ids = []

        for name in result_df["Name"]:
            temp = df[df["Name"] == name]
            if not temp.empty:
                rec_ids.append(int(temp.iloc[0]["ProductID"]))

        return rec_ids

    except Exception as e:
        print("Error in hybrid:", e)
        return []