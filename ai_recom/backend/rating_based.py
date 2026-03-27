import pandas as pd


def recommend_top_rated(top_n=20, min_reviews=5):
    try:
        #  LOAD ONLY WHEN FUNCTION CALLED
        df = pd.read_csv("final_clean_data.csv")

        # Basic cleaning
        df.columns = df.columns.str.strip()

        if "ProdID" in df.columns:
            df = df.rename(columns={"ProdID": "ProductID"})

        df = df.dropna(subset=["ProductID", "Rating"])

        df["ProductID"] = pd.to_numeric(df["ProductID"], errors="coerce")
        df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")

        if "ReviewCount" not in df.columns:
            df["ReviewCount"] = 0

        df["ReviewCount"] = pd.to_numeric(
            df["ReviewCount"], errors="coerce"
        ).fillna(0)

        # GROUP
        product_stats = (
            df.groupby("ProductID")
            .agg({
                "Rating": "mean",
                "ReviewCount": "sum"
            })
            .reset_index()
        )

        #  FILTER
        filtered = product_stats[
            product_stats["ReviewCount"] >= min_reviews
        ]

        if filtered.empty:
            filtered = product_stats

        #  SORT
        top_products = filtered.sort_values(
            by=["Rating", "ReviewCount"],
            ascending=False
        ).head(top_n)

        return top_products["ProductID"].astype(int).tolist()

    except Exception as e:
        print("Rating error:", e)
        return []

def get_top_rated(top_n=20):
    return recommend_top_rated(top_n)