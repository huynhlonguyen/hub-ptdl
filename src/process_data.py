# File: process_data.py
# Mục đích: Xử lý và chuẩn hóa dữ liệu thô
# Tác giả: Huỳnh Long Uyển (Học viên Cao học HUB)


import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

from data_utils import load_market_data
from feature_engineering import process_and_save_data

def main():
    """
    Hàm chính để xử lý dữ liệu và tạo báo cáo
    """
    # Thiết lập đường dẫn
    current_dir = Path(__file__).parent.parent
    data_dir = current_dir / 'data' / 'stock-market-behavior-analysis' / 'raw' / 'market_data'
    output_dir = current_dir / 'output'
    
    print(f"Thư mục dữ liệu: {data_dir}")
    print(f"Thư mục output: {output_dir}")
    
    # Tạo thư mục output nếu chưa tồn tại
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Đọc dữ liệu
    data_dict = load_market_data(data_dir)
    
    # Xử lý và lưu dữ liệu
    process_and_save_data(
        data_dict=data_dict,
        output_dir=output_dir,
        missing_threshold=0.5
    )

if __name__ == "__main__":
    # Thiết lập style cho matplotlib
    plt.style.use('default')
    sns.set_theme()
    
    # Chạy chương trình chính
    main() 