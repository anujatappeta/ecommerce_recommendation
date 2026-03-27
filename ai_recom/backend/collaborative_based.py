import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


def get_collaborative_recommendations(user_id, top_n=10):
    try:
        # LOAD SMALL DATA ONLY
        df = pd.read_csv("final_clean_data.csv").head(500)

        df.columns = df.columns.str.strip()

        if "ProdID" in df.columns:
            df = df.rename(columns={"ProdID": "ProductID"})

        if df.empty:
            return []

        # -------------------------
        # USER-ITEM MATRIX
        # -------------------------
        user_item_matrix = df.pivot_table(
            index="UserID",
            columns="ProductID",
            values="Rating"
        ).fillna(0)

        # If user not present → return empty
        if user_id not in user_item_matrix.index:
            return []

        # -------------------------
        # SIMILARITY
        # -------------------------
        user_similarity = cosine_similarity(user_item_matrix)

        user_similarity_df = pd.DataFrame(
            user_similarity,
            index=user_item_matrix.index,
            columns=user_item_matrix.index
        )

        # -------------------------
        # FIND SIMILAR USERS
        # -------------------------
        similar_users = user_similarity_df[user_id].sort_values(ascending=False)
        similar_users = similar_users.drop(user_id)

        top_similar_users = similar_users.head(5).index

        # -------------------------
        # RECOMMENDATION SCORE
        # -------------------------
        similar_users_ratings = user_item_matrix.loc[top_similar_users]

        recommendation_scores = similar_users_ratings.mean(axis=0)

        user_rated_products = user_item_matrix.loc[user_id]

        recommendation_scores = recommendation_scores[user_rated_products == 0]

        # -------------------------
        # TOP PRODUCTS
        # -------------------------
        top_products = recommendation_scores.sort_values(ascending=False).head(top_n)

        return top_products.index.astype(int).tolist()

    except Exception as e:
        print("Collaborative error:", e)
        return []