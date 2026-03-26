import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from ai_recom.backend.cleaning_data import load_data, clean_data

df_raw = load_data("clean_data.csv")
df = clean_data(df_raw)

df["Tags"] = df["Tags"].fillna("").astype(str)
df["Description"] = df["Description"].fillna("").astype(str)
df["Category"] = df["Category"].fillna("").astype(str)
df["Brand"] = df["Brand"].fillna("").astype(str)
df["Name"] = df["Name"].fillna("").astype(str)

df["content"] = (
    df["Name"] + " " +
    df["Brand"] + " " +
    df["Category"] + " " +
    df["Tags"] + " " +
    df["Description"]
)

tfidf = TfidfVectorizer(
    stop_words="english",
    ngram_range=(1, 2),
    min_df=2
)

tfidf_matrix = tfidf.fit_transform(df["content"])

similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)


def recommend_products(product_name, top_n=10):

    product_name = product_name.lower()

    matches = df[
        df["Name"].str.contains(product_name, na=False) |
        df["Tags"].str.contains(product_name, na=False)
    ]

    if matches.empty:
        print("Product not found!")
        return pd.DataFrame()

    index = matches.index[0]

    query_category = df.loc[index, "Category"]

    similarity_scores = list(enumerate(similarity_matrix[index]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

    filtered_indices = []
    for i, score in similarity_scores:
        if i == index:
            continue

        if df.loc[i, "Category"] == query_category:
            filtered_indices.append(i)

        if len(filtered_indices) == top_n:
            break

    if len(filtered_indices) == 0:
        filtered_indices = [
            i for i, score in similarity_scores
            if i != index
        ][:top_n]
        
    return df.iloc[filtered_indices][["Name", "Brand", "ReviewCount"]]

if __name__ == "__main__":

    result = recommend_products("LIPSTICK", top_n=5)
    print(result)

def get_content_recommendations(product_id, top_n=10):

    try:
        # Find product using ProductID
        match = df[df["ProductID"] == product_id]

        if match.empty:
            return []

        product_name = match.iloc[0]["Name"]

        # Call your original function
        result_df = recommend_products(product_name, top_n)

        if result_df.empty:
            return []

        # Convert Names → ProductIDs
        rec_ids = []

        for name in result_df["Name"]:
            temp = df[df["Name"] == name]
            if not temp.empty:
                rec_ids.append(int(temp.iloc[0]["ProductID"]))

        return rec_ids

    except Exception as e:
        print("Error in content recommendations:", e)
        return []