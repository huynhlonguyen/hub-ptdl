# File: process_data.py
# Mục đích: Xử lý dữ liệu thị trường chứng khoán và tạo báo cáo
# Tác giả: AI Assistant
# Ngày tạo: 2024-03-23

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
    # Thiết lập thư mục
    current_dir = Path.cwd()
    data_dir = current_dir / 'data' / 'stock-market-behavior-analysis' / 'raw' / 'market_data'
    output_dir = current_dir / 'src' / 'output'
    
    print(f"Thư mục dữ liệu: {data_dir}")
    print(f"Thư mục output: {output_dir}")
    
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