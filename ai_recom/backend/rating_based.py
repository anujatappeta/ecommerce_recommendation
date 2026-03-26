import pandas as pd
#from cleaning_data import load_data, clean_data
from ai_recom.backend.cleaning_data import load_data, clean_data
df_raw = load_data("clean_data.csv")
df = clean_data(df_raw)

product_stats = df.groupby("ProductID").agg({
    "Rating": "mean",
    "ReviewCount": "sum",
    "Name": "first",
    "Brand": "first"
}).reset_index()

product_stats.rename(columns={
    "Rating": "AverageRating",
    "ReviewCount": "TotalReviews"
}, inplace=True)

def recommend_top_rated(top_n=10, min_reviews=5):

    filtered = product_stats[product_stats["TotalReviews"] >= min_reviews]

    top_products = filtered.sort_values(
        by=["AverageRating", "TotalReviews"],
        ascending=False
    ).head(top_n)

    return top_products[["Name", "Brand", "AverageRating", "TotalReviews"]]


if __name__ == "__main__":

    result = recommend_top_rated(top_n=5)

    print(result)


def get_top_rated(top_n=10):
    try:
        result_df = recommend_top_rated(top_n)

        if result_df.empty:
            return pd.DataFrame()

        # 🔥 MERGE WITH ORIGINAL DATA (IMPORTANT)
        final_df = df.merge(
            result_df[["Name"]],
            on="Name",
            how="inner"
        )

        return final_df

    except Exception as e:
        print("Error in rating-based:", e)
        return pd.DataFrame()