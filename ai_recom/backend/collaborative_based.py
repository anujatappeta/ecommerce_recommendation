import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
#from cleaning_data import load_data, clean_data
from ai_recom.backend.cleaning_data import load_data, clean_data
df_raw = load_data("clean_data.csv")
df = clean_data(df_raw)

user_item_matrix = df.pivot_table(
    index="UserID",
    columns="ProductID",
    values="Rating"
)

user_item_matrix = user_item_matrix.fillna(0)

user_similarity = cosine_similarity(user_item_matrix)

user_similarity_df = pd.DataFrame(
    user_similarity,
    index=user_item_matrix.index,
    columns=user_item_matrix.index
)

def recommend_products(user_id, top_n=10):

    if user_id not in user_item_matrix.index:
        print("User not found!")
        return pd.DataFrame()

    similar_users = user_similarity_df[user_id].sort_values(ascending=False)
    similar_users = similar_users.drop(user_id)
    top_similar_users = similar_users.head(5).index

    similar_users_ratings = user_item_matrix.loc[top_similar_users]

    recommendation_scores = similar_users_ratings.mean(axis=0)

    user_rated_products = user_item_matrix.loc[user_id]
    recommendation_scores = recommendation_scores[user_rated_products == 0]

    top_products = recommendation_scores.sort_values(ascending=False).head(top_n)

    recommended_products = df[df["ProductID"].isin(top_products.index)]

    return recommended_products[["Name", "Brand", "ReviewCount"]].drop_duplicates()

if __name__ == "__main__":

    result = recommend_products(user_id=1, top_n=5)

    print(result)


def get_collaborative_recommendations(user_id, top_n=10):

    try:
        # Call your existing function
        result_df = recommend_products(user_id, top_n)

        if result_df.empty:
            return []

        rec_ids = []

        for name in result_df["Name"]:
            temp = df[df["Name"] == name]
            if not temp.empty:
                rec_ids.append(int(temp.iloc[0]["ProductID"]))

        return rec_ids

    except Exception as e:
        print("Error in collaborative:", e)
        return []