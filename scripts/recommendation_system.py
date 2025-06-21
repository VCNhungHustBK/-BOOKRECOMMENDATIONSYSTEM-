# scripts/recommendation_system.py
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from difflib import get_close_matches
import os
from scipy import sparse

# Lấy đường dẫn thư mục gốc của dự án
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

def find_book_id_by_title(title, books_df, threshold=0.6):
    """
    Tìm book_id dựa trên tên sách, sử dụng fuzzy matching
    
    Parameters:
    -----------
    title : str
        Tên sách cần tìm
    books_df : pandas.DataFrame
        DataFrame chứa thông tin sách
    threshold : float, default=0.6
        Ngưỡng độ tương đồng tối thiểu
    """
    # Chuyển tất cả về chữ thường để so sánh
    title = title.lower()
    all_titles = books_df['title'].str.lower().tolist()
    
    # Tìm các kết quả tương đồng
    matches = get_close_matches(title, all_titles, n=1, cutoff=threshold)
    
    if matches:
        # Lấy book_id của kết quả đầu tiên
        book_id = books_df[books_df['title'].str.lower() == matches[0]]['book_id'].iloc[0]
        return book_id, matches[0]
    return None, None

def recommend_books(book_input, book_similarity_df, books_df, k=5):
    """
    Gợi ý k sách tương tự với sách được chỉ định
    
    Parameters:
    -----------
    book_input : int or str
        ID hoặc tên của sách cần gợi ý
    book_similarity_df : pandas.DataFrame
        Ma trận độ tương đồng giữa các sách
    books_df : pandas.DataFrame
        DataFrame chứa thông tin sách
    k : int, default=5
        Số lượng sách gợi ý
    """
    try:
        # Nếu book_input là string, tìm book_id tương ứng
        if isinstance(book_input, str):
            book_id, matched_title = find_book_id_by_title(book_input, books_df)
            if book_id is None:
                print(f"Không tìm thấy sách có tên tương tự với '{book_input}'")
                return pd.DataFrame(columns=['book_id', 'title'])
            print(f"Đã tìm thấy sách: {matched_title}")
        else:
            book_id = book_input
            
        similar_scores = book_similarity_df[book_id]
        similar_books = similar_scores.sort_values(ascending=False).index
        similar_books = similar_books[similar_books != book_id][:k]
        recommendations = books_df[books_df['book_id'].isin(similar_books)][['book_id', 'title']]
        return recommendations
    except KeyError:
        print(f"BookID {book_id} không tồn tại trong dữ liệu.")
        return pd.DataFrame(columns=['book_id', 'title'])

# Bước 1: Đọc dữ liệu đã được xử lý
print("Đang đọc dữ liệu...")
try:
    combined_ratings = pd.read_csv(os.path.join(DATA_DIR, 'combined_ratings.csv'))
    combined_books = pd.read_csv(os.path.join(DATA_DIR, 'combined_books.csv'))
except FileNotFoundError:
    print("Lỗi: Không tìm thấy file dữ liệu đã xử lý.")
    print("Vui lòng chạy data_preprocessing.py trước.")
    exit(1)

# Bước 2: Lọc dữ liệu để giảm kích thước
print("Đang lọc dữ liệu...")
min_ratings = 50  # Giảm số lượng đánh giá tối thiểu xuống 50
book_counts = combined_ratings['book_id'].value_counts()
popular_books = book_counts[book_counts >= min_ratings].index
filtered_ratings = combined_ratings[combined_ratings['book_id'].isin(popular_books)]

# Bước 3: Tạo ma trận người dùng-sách với kiểu dữ liệu tối ưu
print("Đang tạo ma trận người dùng-sách...")
# Tạo ma trận thưa (sparse matrix) để tiết kiệm bộ nhớ
user_ids = pd.Categorical(filtered_ratings['user_id']).codes
book_ids = pd.Categorical(filtered_ratings['book_id']).codes
ratings = filtered_ratings['rating'].astype('float32')

user_book_matrix = sparse.csr_matrix(
    (ratings, (user_ids, book_ids)),
    shape=(len(pd.unique(filtered_ratings['user_id'])), len(pd.unique(filtered_ratings['book_id'])))
)

print(f"Kích thước ma trận: {user_book_matrix.shape}")

# Bước 4: Tính độ tương đồng theo từng phần
print("Đang tính độ tương đồng...")
# Chia nhỏ ma trận để tính toán
chunk_size = 500  # Giảm kích thước chunk
n_books = user_book_matrix.shape[1]
book_similarity = np.zeros((n_books, n_books), dtype='float32')

for i in range(0, n_books, chunk_size):
    end_i = min(i + chunk_size, n_books)
    chunk = user_book_matrix[:, i:end_i].T
    similarity_chunk = cosine_similarity(chunk, user_book_matrix.T)
    book_similarity[i:end_i, :] = similarity_chunk

# Tạo DataFrame với book_id gốc
book_id_map = dict(enumerate(pd.unique(filtered_ratings['book_id'])))
book_similarity_df = pd.DataFrame(
    book_similarity,
    index=[book_id_map[i] for i in range(n_books)],
    columns=[book_id_map[i] for i in range(n_books)]
)

# Export các biến cần thiết cho web app
__all__ = ['recommend_books', 'book_similarity_df', 'combined_books'] 