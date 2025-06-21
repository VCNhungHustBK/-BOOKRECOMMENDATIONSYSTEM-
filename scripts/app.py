from flask import Flask, render_template, request, jsonify
import pandas as pd
import sys
import os

# Thêm thư mục hiện tại vào PYTHONPATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from recommendation_system import recommend_books, book_similarity_df, combined_books

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    book_title = request.form.get('book_title')
    if not book_title:
        return jsonify({'error': 'Vui lòng nhập tên sách'})
    
    # Lấy gợi ý sách
    recommendations = recommend_books(book_title, book_similarity_df, combined_books)
    
    if recommendations.empty:
        return jsonify({'error': f'Không tìm thấy sách tương tự với "{book_title}"'})
    
    # Chuyển đổi DataFrame thành list để trả về JSON
    result = recommendations.to_dict('records')
    return jsonify({'recommendations': result})

if __name__ == '__main__':
    app.run(debug=True) 