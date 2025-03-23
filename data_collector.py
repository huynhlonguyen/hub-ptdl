"""
File: data_collector.py
Chức năng: Tải và tổ chức dữ liệu cho dự án phân tích hành vi đầu tư chứng khoán
Các thư mục liên quan:
- data/stock-market-behavior-analysis/raw/: Lưu dữ liệu thô
- data/stock-market-behavior-analysis/processed/: Lưu dữ liệu đã xử lý
"""

import os
import pandas as pd
import requests
from pathlib import Path

# Định nghĩa đường dẫn cơ sở
BASE_DIR = Path("data/stock-market-behavior-analysis")
RAW_DIR = BASE_DIR / "raw"
PROCESSED_DIR = BASE_DIR / "processed"

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
    dirs = [
        RAW_DIR / "market_data",
        RAW_DIR / "company_info",
        PROCESSED_DIR / "features"
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)

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
            if category == 'market_data':
                save_path = RAW_DIR / "market_data" / f"{name}{file_ext}"
            else:
                save_path = RAW_DIR / "company_info" / f"{name}{file_ext}"
            download_file(url, save_path)

def process_data():
    """Xử lý dữ liệu thô thành features"""
    # Đọc dữ liệu
    pricing_data = pd.read_csv(RAW_DIR / "market_data/pricing.csv")
    trading_value = pd.read_csv(RAW_DIR / "market_data/trading_value.csv")
    market_return = pd.read_csv(RAW_DIR / "market_data/market_return.csv")
    company_info = pd.read_csv(RAW_DIR / "company_info/descriptive.csv")
    
    # Tính toán các features cơ bản
    features = pd.DataFrame()
    
    # 1. Tính toán khối lượng giao dịch trung bình
    features['avg_trading_value'] = trading_value.mean()
    
    # 2. Tính toán biến động giá
    features['price_volatility'] = pricing_data.std()
    
    # 3. Tính toán tương quan với thị trường
    features['market_correlation'] = pricing_data.corrwith(market_return['VNIndex'])
    
    # 4. Thêm thông tin công ty
    features = features.join(company_info.set_index('ticker'))
    
    # Lưu features
    output_path = PROCESSED_DIR / "features/basic_features.csv"
    features.to_csv(output_path, index=True)
    print(f"Đã xử lý và lưu features tại: {output_path}")

if __name__ == "__main__":
    collect_data()
    process_data() 