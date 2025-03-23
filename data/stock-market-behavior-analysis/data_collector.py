"""
File: data_collector.py
Chức năng: Tải và tổ chức dữ liệu cho dự án phân tích hành vi đầu tư chứng khoán
Các thư mục liên quan:
- raw/: Lưu dữ liệu thô
- processed/: Lưu dữ liệu đã xử lý
"""

import os
import pandas as pd
import requests
from pathlib import Path

# Định nghĩa URLs của dữ liệu
DATA_URLS = {
    'market_data': {
        'pricing': 'https://raw.githubusercontent.com/nkb36/AlphaResearchVietnamMarket/main/data/pricing_data.csv',
        'trading_value': 'https://raw.githubusercontent.com/nkb36/AlphaResearchVietnamMarket/main/data/trading_value_data.csv',
        'market_return': 'https://raw.githubusercontent.com/nkb36/AlphaResearchVietnamMarket/main/data/market_return.csv'
    },
    'company_info': {
        'descriptive': 'https://raw.githubusercontent.com/nkb36/AlphaResearchVietnamMarket/main/data/descriptive_info.csv',
        'financial': 'https://raw.githubusercontent.com/nkb36/AlphaResearchVietnamMarket/main/data/financial_data.txt'
    }
}

def create_directories():
    """Tạo cấu trúc thư mục cần thiết"""
    dirs = ['raw/market_data', 'processed/features']
    for d in dirs:
        Path(d).mkdir(parents=True, exist_ok=True)

def download_file(url, save_path):
    """Tải file từ URL và lưu vào đường dẫn chỉ định"""
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f"Đã tải thành công: {save_path}")
    except Exception as e:
        print(f"Lỗi khi tải {url}: {str(e)}")

def collect_data():
    """Thu thập và tổ chức dữ liệu"""
    create_directories()
    
    # Tải dữ liệu thị trường
    for category, urls in DATA_URLS.items():
        for name, url in urls.items():
            file_ext = '.csv' if url.endswith('.csv') else '.txt'
            save_path = f"raw/market_data/{name}{file_ext}"
            download_file(url, save_path)

def process_data():
    """Xử lý dữ liệu thô thành features"""
    # Đọc dữ liệu
    pricing_data = pd.read_csv('raw/market_data/pricing.csv')
    trading_value = pd.read_csv('raw/market_data/trading_value.csv')
    market_return = pd.read_csv('raw/market_data/market_return.csv')
    
    # Tính toán các features cơ bản
    features = pd.DataFrame()
    
    # 1. Tính toán khối lượng giao dịch trung bình
    features['avg_trading_value'] = trading_value.mean()
    
    # 2. Tính toán biến động giá
    features['price_volatility'] = pricing_data.std()
    
    # 3. Tính toán tương quan với thị trường
    features['market_correlation'] = pricing_data.corrwith(market_return['VNIndex'])
    
    # Lưu features
    features.to_csv('processed/features/basic_features.csv', index=True)
    print("Đã xử lý và lưu features")

if __name__ == "__main__":
    collect_data()
    process_data() 