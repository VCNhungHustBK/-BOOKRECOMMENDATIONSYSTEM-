# HỆ THỐNG GỢI Ý SÁCH (BOOK RECOMMENDATION SYSTEM)

## 1. Giới Thiệu
Hệ thống gợi Ý sách này được xây dựng dựa trên hai nguồn dữ liệu chính:
- Goodbooks-10k dataset
- Book-Crossing dataset

Hệ thống sử dụng thuật toán cosine similarity để tìm ra những cuốn sách có độ tương đồng cao với sách người dùng đang xem.

## 2. Cấu Trúc Dự Án
```
BOOKRECOMMENDATIONSYSTEM/
├── data/                  # Thư mục chứa dữ liệu
│   ├── ratings.csv       # Dữ liệu đánh giá từ Goodbooks-10k
│   ├── books.csv         # Dữ liệu sách từ Goodbooks-10k
│   ├── BX-Book-Ratings.csv  # Dữ liệu đánh giá từ Book-Crossing
│   ├── BX-Books.csv      # Dữ liệu sách từ Book-Crossing
│   ├── combined_ratings.csv  # Dữ liệu đánh giá đã gộp
│   ├── combined_books.csv    # Dữ liệu sách đã gộp
│   └── recommendations_for_book_1.csv  # Kết quả gợi Ý
├── scripts/              # Thư mục chứa mã nguồn
│   ├── data_preprocessing.py  # Script tiền xử lý dữ liệu
│   └── recommendation-system.py  # Script hệ thống gợi Ý
└── README.txt           # File hướng dẫn này

## 3. Yêu Cầu Hệ Thống
- Python 3.x
- Các thư viện cần thiết:
  - pandas
  - numpy
  - scikit-learn

## 4. Cài Đặt
1. Cài đặt Python 3.x từ https://www.python.org/downloads/
2. Cài đặt các thư viện cần thiết:
```bash
pip install pandas numpy scikit-learn
```

## 5. Cách Chạy

### Bước 1: Chuẩn Bị Dữ Liệu
- Tải dữ liệu Goodbooks-10k và Book-Crossing
- Đặt các file dữ liệu vào thư mục `data/`:
  - `ratings.csv`
  - `books.csv`
  - `BX-Book-Ratings.csv`
  - `BX-Books.csv`

### Bước 2: Tiền Xử Lý Dữ Liệu
Script này sẽ:
- Đọc và làm sạch dữ liệu từ cả hai nguồn
- Loại bỏ đánh giá trùng lặp và giá trị null
- Lọc sách phổ biến (ít nhất 100 đánh giá cho Goodbooks, 50 cho Book-Crossing)
- Chuẩn hóa thang đánh giá
- Gộp dữ liệu từ hai nguồn
- Lưu kết quả vào `combined_ratings.csv` và `combined_books.csv`

### Bước 3: Chạy Hệ Thống Gợi Ý
cd scripts
python app.py
http://localhost:5000 

### Bước 4: Chạy thử
Lấy tên sách trong file conbined_book.csv để chạy thử hệ thống ( vì dữ liệu dùng bằng trong file )

## 6. Kết Quả
Sau khi chạy, hệ thống sẽ tạo ra các file:
- `combined_ratings.csv`: Dữ liệu đánh giá đã gộp
- `combined_books.csv`: Dữ liệu sách đã gộp
## 7. Tùy Chỉnh
- Có thể thay đổi book_id mẫu trong file `recommendation-system.py`
- Điều chỉnh số lượng sách gợi Ý (k) trong hàm `recommend_books`
- Thay đổi ngưỡng lọc sách phổ biến trong `data_preprocessing.py`

