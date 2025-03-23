# File: analysis_script.py
# Mục đích: Phân tích dữ liệu thị trường chứng khoán Việt Nam
# Tác giả: AI Assistant
# Ngày tạo: 2024-03-23

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import os
from data_utils import load_market_data, analyze_data_quality, calculate_technical_indicators, plot_technical_analysis

def main():
    # Thiết lập style cho đồ thị
    plt.style.use('default')
    sns.set_theme()
    
    # Đường dẫn đến thư mục dữ liệu và output
    current_dir = Path(os.getcwd())
    DATA_DIR = current_dir / 'data' / 'stock-market-behavior-analysis' / 'raw' / 'market_data'
    OUTPUT_DIR = current_dir / 'src' / 'output'
    print(f"Thư mục dữ liệu: {DATA_DIR}")
    print(f"Thư mục output: {OUTPUT_DIR}")
    
    # Tạo thư mục output nếu chưa tồn tại
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    print("1. Đọc và kiểm tra dữ liệu")
    print("-" * 50)
    
    # Đọc dữ liệu
    data_dict = load_market_data(DATA_DIR)
    
    # Hiển thị thông tin cơ bản về các DataFrame
    for name, df in data_dict.items():
        print(f"\nThông tin về {name}:")
        print("-" * 30)
        print(f"Shape: {df.shape}")
        print("\nCác cột:")
        print(df.columns.tolist())
        print("\nMẫu dữ liệu:")
        print(df.head())
        
    print("\n2. Phân tích chất lượng dữ liệu")
    print("-" * 50)
    
    # Phân tích chất lượng dữ liệu cho từng DataFrame
    quality_stats = {}
    for name, df in data_dict.items():
        quality_stats[name] = analyze_data_quality(df, name)
        
    # Hiển thị kết quả phân tích
    for name, stats in quality_stats.items():
        print(f"\nKết quả phân tích chất lượng dữ liệu - {name}")
        print("-" * 30)
        print(f"Kích thước: {stats['shape']}")
        print(f"\nTỷ lệ dữ liệu thiếu (%):\n{pd.Series(stats['missing']).sort_values(ascending=False).head()}")
        print(f"\nSố lượng bản ghi trùng lặp: {stats['duplicates']}")
        
        if 'outliers' in stats:
            print("\nThông tin về outliers:")
            for col, out_stats in stats['outliers'].items():
                print(f"{col}: {out_stats['n_outliers']} outliers")
                
    print("\n3. Phân tích thống kê mô tả")
    print("-" * 50)
    
    # Phân tích thống kê cho dữ liệu giá
    price_stats = data_dict['pricing'].describe()
    print("\nThống kê mô tả cho dữ liệu giá:")
    print(price_stats)
    
    # Vẽ biểu đồ phân phối giá cho một số mã chứng khoán phổ biến
    top_stocks = ['VNM', 'VIC', 'VCB', 'FPT', 'MBB']
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.ravel()
    
    for i, stock in enumerate(top_stocks):
        if stock in data_dict['pricing'].columns:
            sns.histplot(data=data_dict['pricing'][stock].dropna(), ax=axes[i])
            axes[i].set_title(f'Phân phối giá - {stock}')
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'price_distribution.png')
    plt.close()
    
    print("\n4. Tính toán và phân tích các chỉ số kỹ thuật")
    print("-" * 50)
    
    # Chọn một số mã chứng khoán để phân tích
    selected_stocks = ['VNM', 'VIC', 'VCB']
    
    for stock in selected_stocks:
        if stock in data_dict['pricing'].columns:
            # Tính toán các chỉ số kỹ thuật
            tech_data = calculate_technical_indicators(data_dict['pricing'], stock)
            
            # Vẽ đồ thị phân tích kỹ thuật
            plt.figure()
            plot_technical_analysis(tech_data, stock)
            plt.savefig(OUTPUT_DIR / f'technical_analysis_{stock}.png')
            plt.close()
            
    print("\n5. Phân tích xu hướng thị trường")
    print("-" * 50)
    
    # Phân tích xu hướng tỷ suất sinh lời thị trường
    market_returns = data_dict['returns']
    
    plt.figure(figsize=(12, 6))
    plt.plot(market_returns['Date'], market_returns['market_return'], marker='o')
    plt.title('Tỷ suất sinh lời thị trường theo thời gian')
    plt.xlabel('Thời gian')
    plt.ylabel('Tỷ suất sinh lời (%)')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'market_returns.png')
    plt.close()
    
    # Thống kê mô tả về tỷ suất sinh lời
    print("\nThống kê về tỷ suất sinh lời thị trường:")
    print(market_returns['market_return'].describe())

if __name__ == "__main__":
    main() 