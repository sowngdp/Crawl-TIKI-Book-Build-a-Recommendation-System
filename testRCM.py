import nltk
import re
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.snowball import SnowballStemmer
# ===========Create a dataframe from the similarity matrix to export
df_product = pd.read_csv('crawled_data.csv', index_col=0)
vals = df_product.name.tolist()
stemmer = SnowballStemmer("english")
def tokenize_and_stem(text):

    # Tokenize by sentence, then by word - thực hiện tokenization (spliting token)
    tokens = [word for sent in nltk.sent_tokenize(text)
              for word in nltk.word_tokenize(sent)]

    # Filter out raw tokens to remove noise - Chuẩn hóa các token (token normalization)
    filtered_tokens = [token for token in tokens if re.search('[a-zA-Z]', token)]

    # Stem the filtered_tokens
    stems = [stemmer.stem(word) for word in filtered_tokens]

    return stems

# Instantiate TfidfVectorizer object with stopwords and tokenizer
tfidf_vectorizer = TfidfVectorizer(max_df=0.8, max_features=200000,
                                 min_df=0.2, stop_words='english',
                                 use_idf=True, tokenizer=tokenize_and_stem,
                                 ngram_range=(1,3))
tfidf_matrix = tfidf_vectorizer.fit_transform([x for x in df_product["short_description"]])
similarity_distance = 1 - cosine_similarity(tfidf_matrix)

similarity_df = pd.DataFrame(similarity_distance, columns=vals, index=vals)
# Export
similarity_df.to_csv('matrix.csv')

# ======================Recommendation example
name = 'Thiên Tài Bên Trái, Kẻ Điên Bên Phải (Tái Bản)'

matches = similarity_df[name].sort_values()[1:6]
print(df_product.columns)

matches = matches.index.tolist()
df_product.loc[df_product['name'].isin(matches)]
df_product.set_index('name').loc[matches]
print(df_product.set_index('name').loc[matches])