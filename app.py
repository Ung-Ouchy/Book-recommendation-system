import streamlit as st
import pickle
import pandas as pd

# Load data
books = pickle.load(open("books.pkl", 'rb'))
similarity = pickle.load(open("similarity.pkl", 'rb'))

book_name = books['title'].values
category_list = books['categories'].unique()



def recommend_by_description(book, n):
    index=books[books['title']==book].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector:vector[1])
    recommend_book=[]
    cover=[]
    for i in distance[1:n+1]:
        recommend_book.append(books.iloc[i[0]].title)
        cover.append(books.iloc[i[0]].thumbnail)
    return recommend_book,cover

def recommend_by_rate(rate, n):
    Index = books[books['average_rating'] <= float(rate)]['average_rating'].sort_values(ascending=False).index
    # Ensure that the number of recommendations does not exceed the available indices
    num_recommendations = min(len(Index), n-2)  # Ensure we do not go out of bounds
    recommend_books = [books.iloc[Index[i]]['title'] for i in range(num_recommendations)]
    cover = [books.iloc[Index[i]]['thumbnail'] for i in range(num_recommendations)]
    return recommend_books, cover


    return recommend_books,cover

def recommend_by_category(category, n):
    recommend_books = books[books['categories'] == category]['title'].tolist()[:n]
    cover = books[books['categories'] == category]['thumbnail'].tolist()[:n]
    return recommend_books, cover

   
def display_books(book, cover):
    col1, col2, col3 = st.columns(3)
    for i in range(len(book)):
        book_index = books[books['title'] == book[i]].index[0]
        col = col1 if i % 2 == 0 else col3
        with col:
            st.write(f"**{i+1}. {book[i]}**")
            st.write(f"ISBN: {books['isbn10'][book_index]}")
            st.write(f"Author: {books['authors'][book_index]}")
            st.write(f"Publish Year: {(books['published_year'][book_index])}")
            st.write(f"Pages: {(books['num_pages'][book_index])}")
            st.write(f"Rating: {(books['average_rating'][book_index])}")
            cover_url = "https://via.placeholder.com/128x198.png?text=No+Cover" if pd.isna(cover[i]) or cover[i] == '' else cover[i]
            st.image(cover_url, width=200 if i % 2 == 0 else 300)

# Pages for the app
def page_1():
    st.title("Book Recommendation System")
    st.write("**Recommend Books by Description**")
    selected_book = st.selectbox("Select Book", book_name)
    if st.checkbox("Select All"):
        num_recommendations =len(books)
    else:
        num_recommendations = st.number_input("Number of recommendations", value=5, min_value=1)    
    if st.button("Show Recommendations"):
        recommended_books, covers = recommend_by_description(selected_book, num_recommendations)
        display_books(recommended_books, covers)

def page_2():
    st.title("Book Recommendation System")
    st.write("**Recommend Books by Rating**")
    
    rating_input = st.slider("Select a rating (1 to 5):", 1, 5)
    if st.checkbox("Select All"):
        num_recommendations =len(books)
    else:
        num_recommendations = st.number_input("Number of recommendations", value=5, min_value=1)    
    if st.button("Show Recommendations"):
        recommended_books, covers = recommend_by_rate(rating_input, num_recommendations)
        display_books(recommended_books, covers)

def page_3():
    st.title("Book Recommendation System")
    st.write("**Recommend Books by Category**")
    
    selected_category = st.selectbox("Select Category", category_list)
    if st.checkbox("Select All"):
        num_recommendations =len(books)
    else:
        num_recommendations = st.number_input("Number of recommendations", value=5, min_value=1)    
    if st.button("Show Recommendations"):
        recommended_books, covers = recommend_by_category(selected_category, num_recommendations)
        display_books(recommended_books, covers)

# Multi-page navigation
def main():
    st.sidebar.title("Navigation")
    pages = {
        "Recommend by Description": page_1,
        "Recommend by Rating": page_2,
        "Recommend by Category": page_3
    }
    
    choice = st.sidebar.radio("Go to", list(pages.keys()))
    pages[choice]()  # Call the selected page function

if __name__ == "__main__":
    main()
