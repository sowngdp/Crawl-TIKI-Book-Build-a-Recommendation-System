# Import modules
import pandas as pd

df_product = pd.read_csv('crawled_data.csv', index_col=0)

print('Number of products loaded: %s ' % (len(df_product)), '\n')

# Display the data
df_product.head()


import nltk
nltk.download('punkt')
import re
from nltk.stem.snowball import SnowballStemmer
#nltk.download('punkt')

# Create an English language SnowballStemmer object
stemmer = SnowballStemmer("english")

# Define a function to perform both stemming and tokenization
def tokenize_and_stem(text):

    # Tokenize by sentence, then by word - thực hiện tokenization (spliting token)
    tokens = [word for sent in nltk.sent_tokenize(text)
              for word in nltk.word_tokenize(sent)]

    # Filter out raw tokens to remove noise - Chuẩn hóa các token (token normalization)
    filtered_tokens = [token for token in tokens if re.search('[a-zA-Z]', token)]

    # Stem the filtered_tokens
    stems = [stemmer.stem(word) for word in filtered_tokens]

    return stems

# kỹ thuật extract features từ input text
# create input features to train NLP models
# Transform token into features
from sklearn.feature_extraction.text import TfidfVectorizer

# Instantiate TfidfVectorizer object with stopwords and tokenizer
tfidf_vectorizer = TfidfVectorizer(max_df=0.8, max_features=200000,
                                 min_df=0.2, stop_words='english',
                                 use_idf=True, tokenizer=tokenize_and_stem,
                                 ngram_range=(1,3))

# Fit and transform the tfidf_vectorizer
tfidf_matrix = tfidf_vectorizer.fit_transform([x for x in df_product["short_description"]])

# ==================================KMeans==================================================================

from sklearn.cluster import KMeans

km = KMeans(n_clusters=7)

# Fit the k-means object with tfidf_matrix
km.fit(tfidf_matrix)

clusters = km.labels_.tolist()

df_product["cluster"] = clusters
df_product['cluster'].value_counts()

# =================================Hierarchy===================================================================

# Import matplotlib.pyplot for plotting graphs
from sklearn.metrics.pairwise import cosine_similarity
from scipy.cluster.hierarchy import linkage, dendrogram
import matplotlib.pyplot as plt

# Calculate the similarity distance
similarity_distance = 1 - cosine_similarity(tfidf_matrix)

# Create mergings matrix
mergings = linkage(similarity_distance, method='complete')


# ==========Plot the dendrogram, using name as label column
dendrogram_ = dendrogram(mergings,
               labels=[x for x in df_product["name"]],
               leaf_rotation=90,
               leaf_font_size=16,
)

# Adjust the plot
#fig = plt.gcf()
#_ = [lbl.set_color('r') for lbl in plt.gca().get_xmajorticklabels()]
#fig.set_size_inches(108, 21)

#plt.savefig('dendo.png', dpi=100)
#plt.show()


# ===========Create a dataframe from the similarity matrix to export
vals = df_product.name.tolist()
similarity_df = pd.DataFrame(similarity_distance, columns=vals, index=vals)
# Export
similarity_df.to_csv('matrix.csv')

# ======================Recommendation example
name = 'Kỷ Luật Tự Giác (Tặng Kèm Bookmark )'

matches = similarity_df[name].sort_values()[1:6]
matches = matches.index.tolist()

df_product.loc[df_product['name'].isin(matches)]
df_product.set_index('name').loc[matches]
print(df_product.set_index('name').loc[matches])

