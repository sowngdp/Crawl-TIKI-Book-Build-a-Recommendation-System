import streamlit as st
import pandas as pd
import textwrap

# Load and Cache the data
@st.cache_data(persist=True)
def getdata():
    books_df = pd.read_csv('./crawled_data.csv', index_col=0)
    similarity_df = pd.read_csv('./matrix.csv', index_col=0)
    return books_df, similarity_df

books_df, similarity_df = getdata()

# Sidebar
st.sidebar.markdown('__TIKI book recommender__  \nAn app by '
                    '[Frenkyy](https://www.facebook.com/sown.ne)')
st.sidebar.image('./tiki_banner.png', use_column_width=True)
st.sidebar.markdown('# Choose your BOOK!')
st.sidebar.markdown('')
ph = st.sidebar.empty()

selected_book = ph.selectbox('Select one among the 120 BOOKS '
                             'from the menu: (you can type it as well)',
                             [''] + books_df['name'].to_list(), key='default',
                             format_func=lambda x: 'Select a book' if x == '' else x)

# Hiển thị phần thông tin giới thiệu và liên hệ
# Cảnh báo rằng sách chưa được chọn
if selected_book == "Select a book" or selected_book == "":
    st.markdown('### Welcome to the TIKI Book Recommender App!')
    st.markdown('This app recommends books based on the content of the book. '
                'You can select a book from the dropdown menu, and the app will '
                'provide recommendations for similar books.')
    st.markdown('---')
    st.markdown('### About the app: ')
    st.markdown('This app is built to recommend books based on the '
                        'content of the book. The content is analyzed using '
                        'Natural Language Processing techniques to extract '
                        'features from the text. The features are then used to '
                        'calculate the similarity between books. The app is '
                        'built using Streamlit and deployed on Heroku. '
                        'The data is crawled from Tiki.vn using Scrapy. '
                        'The app is built by Frenkyy & lamnnhu. '
                        'The source code is available on '
                        '[Github](https://github.com/sowngdp/Crawl-TIKI-Book-Build-a-Recommendation-System.git))')
    
    st.markdown('---')
    st.markdown('### Contact: ')
    st.markdown('For any feedback or suggestion, '
                        'please contact me on [Facebook: Frenky](https://www.facebook.com/sown.ne)')
else:
    # Kiểm tra xem selected_book có giá trị không trống
    if selected_book:
        # Hiển thị kết quả khi đã chọn sách
        # Code hiển thị sách và thông tin kết quả ở đây

        # DF query
        matches = similarity_df[selected_book].sort_values()[1:6]
        matches = matches.index.tolist()
        matches = books_df.set_index('name').loc[matches]
        matches.reset_index(inplace=True)

        # Results
        cols = ['price', 'list_price', 'discount', 'discount_rate', 'review_count', 'inventory_status', 'stock_item_qty', 'stock_item_max_sale_qty']

        st.markdown("# The recommended books for [{}] are:".format(selected_book))
        for idx, row in matches.iterrows():
            st.markdown('### {} - {}'.format(str(idx + 1), row['name']))
            st.markdown(row['short_description'])
            st.table(pd.DataFrame(row[cols]).T)
