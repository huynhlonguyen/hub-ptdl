"""
File: utils.py
Chức năng: Cung cấp các hàm tiện ích và cấu hình cho dự án
Các thành phần:
- Danh sách mã VN30
- Hàm kiểm tra và lọc dữ liệu
- Hàm logging
"""

import logging
from datetime import datetime, timedelta
import pandas as pd
import os

# Thiết lập logging
def setup_logging():
    logging.basicConfig(
        filename='analysis.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

# Danh sách mã VN30 (cập nhật 2024)
VN30_SYMBOLS = [
    'ACB', 'BCM', 'BID', 'BVH', 'CTG', 'FPT', 'GAS', 'GVR', 'HDB', 'HPG',
    'MBB', 'MSN', 'MWG', 'NVL', 'PDR', 'PLX', 'PNJ', 'POW', 'SAB', 'SSI',
    'STB', 'TCB', 'TPB', 'VCB', 'VHM', 'VIB', 'VIC', 'VJC', 'VNM', 'VPB'
]

def filter_recent_data(df, years=3):
    """Lọc dữ liệu trong khoảng N năm gần nhất"""
    if 'date' not in df.columns:
        logging.error("Không tìm thấy cột date trong DataFrame")
        return df
    
    df['date'] = pd.to_datetime(df['date'])
    cutoff_date = datetime.now() - timedelta(days=years*365)
    return df[df['date'] >= cutoff_date]

def validate_stock_data(df, symbols=None):
    """Kiểm tra tính hợp lệ của dữ liệu chứng khoán"""
    if symbols is None:
        symbols = VN30_SYMBOLS
    
    missing_symbols = [sym for sym in symbols if sym not in df.columns]
    if missing_symbols:
        logging.warning(f"Thiếu dữ liệu cho các mã: {missing_symbols}")
    
    return {
        'valid_symbols': [sym for sym in symbols if sym in df.columns],
        'missing_symbols': missing_symbols,
        'has_missing_values': df[symbols].isnull().any().any()
    }

def ensure_output_dir():
    """Đảm bảo thư mục output tồn tại"""
    dirs = ['output', 'output/models', 'output/sentiment']
    for d in dirs:
        if not os.path.exists(d):
            os.makedirs(d)
            logging.info(f"Đã tạo thư mục {d}") 