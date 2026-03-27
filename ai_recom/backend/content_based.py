import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_content_recommendations(product_id, top_n=10):
    try:
        #  LOAD SMALL DATA ONLY
        df = pd.read_csv("final_clean_data.csv").head(300)

        df.columns = df.columns.str.strip()

        if "ProdID" in df.columns:
            df = df.rename(columns={"ProdID": "ProductID"})

        if df.empty:
            return []
        # CLEAN
        df["Tags"] = df.get("Tags", "").fillna("").astype(str)
        df["Description"] = df.get("Description", "").fillna("").astype(str)
        df["Category"] = df.get("Category", "").fillna("").astype(str)
        df["Brand"] = df.get("Brand", "").fillna("").astype(str)
        df["Name"] = df.get("Name", "").fillna("").astype(str)

        df["content"] = (
            df["Name"] + " " +
            df["Brand"] + " " +
            df["Category"] + " " +
            df["Tags"] + " " +
            df["Description"]
        )

        # TF-IDF (LIGHT)
        tfidf = TfidfVectorizer(
            stop_words="english",
            max_features=2000   #  LIMIT FEATURES
        )

        tfidf_matrix = tfidf.fit_transform(df["content"])

        similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)
        # FIND PRODUCT
        match = df[df["ProductID"] == product_id]

        if match.empty:
            return []

        index = match.index[0]
        query_category = df.loc[index, "Category"]

        similarity_scores = list(enumerate(similarity_matrix[index]))
        similarity_scores = sorted(
            similarity_scores,
            key=lambda x: x[1],
            reverse=True
        )

        filtered_indices = []

        for i, score in similarity_scores:
            if i == index:
                continue

            if df.loc[i, "Category"] == query_category:
                filtered_indices.append(i)

            if len(filtered_indices) == top_n:
                break

        if not filtered_indices:
            filtered_indices = [
                i for i, _ in similarity_scores if i != index
            ][:top_n]

        return df.iloc[filtered_indices]["ProductID"].astype(int).tolist()

    except Exception as e:
        print("Content error:", e)
        return []
