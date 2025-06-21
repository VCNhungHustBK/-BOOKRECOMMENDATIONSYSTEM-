# scripts/data_preprocessing.py
import pandas as pd

# Đọc dữ liệu Goodbooks-10k
goodbooks_ratings = pd.read_csv('data/ratings.csv')
print("Goodbooks ratings đầu vào:")
print(goodbooks_ratings.head())
print(goodbooks_ratings.shape)

goodbooks_books = pd.read_csv('data/books.csv')
print("\nGoodbooks books đầu vào:")
print(goodbooks_books.head())
print(goodbooks_books.shape)

# Làm sạch Goodbooks ratings
goodbooks_ratings.drop_duplicates(['user_id', 'book_id'], inplace=True)
goodbooks_ratings.dropna(inplace=True)


rating_counts = goodbooks_ratings['book_id'].value_counts()
popular_books = rating_counts[rating_counts >= 100].index
goodbooks_ratings = goodbooks_ratings[goodbooks_ratings['book_id'].isin(popular_books)]
print("\nGoodbooks ratings sau khi làm sạch:")
print(goodbooks_ratings.shape)

# Làm sạch Goodbooks books
goodbooks_books.drop_duplicates('book_id', inplace=True)
goodbooks_books.dropna(subset=['title'], inplace=True)
print("\nGoodbooks books sau khi làm sạch:")
print(goodbooks_books.shape)

# Đọc dữ liệu Book-Crossing
bookcrossing_ratings = pd.read_csv('data/BX-Book-Ratings.csv', sep=';', encoding='latin-1')
print("\nBook-Crossing ratings đầu vào:")
print(bookcrossing_ratings.head())
print(bookcrossing_ratings.shape)

bookcrossing_books = pd.read_csv('data/BX-Books.csv', sep=';', encoding='latin-1')
print("\nBook-Crossing books đầu vào:")
print(bookcrossing_books.head())
print(bookcrossing_books.shape)

# Làm sạch Book-Crossing ratings
bookcrossing_ratings.drop_duplicates(['User-ID', 'ISBN'], inplace=True)
bookcrossing_ratings.dropna(inplace=True)
bookcrossing_ratings = bookcrossing_ratings[bookcrossing_ratings['Book-Rating'] != 0]
rating_counts = bookcrossing_ratings['ISBN'].value_counts()
popular_books = rating_counts[rating_counts >= 50].index
bookcrossing_ratings = bookcrossing_ratings[bookcrossing_ratings['ISBN'].isin(popular_books)]
print("\nBook-Crossing ratings sau khi làm sạch:")
print(bookcrossing_ratings.shape)

# Làm sạch Book-Crossing books
bookcrossing_books.drop_duplicates('ISBN', inplace=True)
bookcrossing_books.dropna(subset=['Book-Title'], inplace=True)
print("\nBook-Crossing books sau khi làm sạch:")
print(bookcrossing_books.shape)

# Chuẩn hóa Book-Crossing
bookcrossing_ratings.rename(columns={'User-ID': 'user_id', 'Book-Rating': 'rating'}, inplace=True)
bookcrossing_books.rename(columns={'Book-Title': 'title'}, inplace=True)

# Chuyển ISBN thành book_id
max_goodbooks_book_id = goodbooks_books['book_id'].max()
bookcrossing_books['book_id'] = range(max_goodbooks_book_id + 1, max_goodbooks_book_id + 1 + len(bookcrossing_books))
bookcrossing_ratings = bookcrossing_ratings.merge(bookcrossing_books[['ISBN', 'book_id']], on='ISBN')

# Chuẩn hóa rating từ 1-10 thành 1-5
bookcrossing_ratings['rating'] = bookcrossing_ratings['rating'].apply(lambda x: 1 + (x * 4 / 10))

# Gộp ratings
combined_ratings = pd.concat([
    goodbooks_ratings[['user_id', 'book_id', 'rating']],
    bookcrossing_ratings[['user_id', 'book_id', 'rating']]
], ignore_index=True)
combined_ratings.drop_duplicates(['user_id', 'book_id'], inplace=True)
print("\nCombined ratings sau khi gộp:")
print(combined_ratings.shape)
print(combined_ratings.head())

# Gộp books
combined_books = pd.concat([
    goodbooks_books[['book_id', 'title']],
    bookcrossing_books[['book_id', 'title']]
], ignore_index=True)
combined_books.drop_duplicates('book_id', inplace=True)
print("\nCombined books sau khi gộp:")
print(combined_books.shape)
print(combined_books.head())

# Lưu dữ liệu gộp
combined_ratings.to_csv('data/combined_ratings.csv', index=False)
combined_books.to_csv('data/combined_books.csv', index=False)
print("\nĐã lưu dữ liệu gộp thành công vào data/combined_ratings.csv và data/combined_books.csv")