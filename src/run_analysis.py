# File: run_analysis.py
# Mục đích: Chạy phân tích dữ liệu thị trường chứng khoán
#Tác giả: Huỳnh Long Uyển (Học viên Cao học HUB)


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import sys
import traceback
from data_utils import load_market_data, analyze_data_quality, calculate_technical_indicators, plot_technical_analysis

def main():
    try:
        # Thiết lập môi trường
        print("Thiết lập môi trường...")
        sns.set_style("whitegrid")  # Thay thế plt.style.use('seaborn')
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', 100)
        plt.rcParams['figure.figsize'] = (12, 8)
        plt.rcParams['font.size'] = 12

        # Đọc dữ liệu
        print("\n1. Đọc dữ liệu...")
        data_dir = Path('..') / 'data' / 'stock-market-behavior-analysis' / 'raw' / 'market_data'
        if not data_dir.exists():
            raise FileNotFoundError(f"Không tìm thấy thư mục dữ liệu: {data_dir}")
            
        market_data = load_market_data(data_dir)
        print("Đã đọc xong dữ liệu!")

        # Phân tích chất lượng dữ liệu
        print("\n2. Phân tích chất lượng dữ liệu...")
        quality_stats = {}
        for name, df in market_data.items():
            print(f"\n=== {name.upper()} DATA ===")
            print(f"Shape: {df.shape}")
            print("\nMẫu dữ liệu:")
            print(df.head())
            
            # Phân tích chất lượng
            quality_stats[name] = analyze_data_quality(df, name)
            print(f"\nDữ liệu thiếu (%):")
            for col, pct in quality_stats[name]['missing'].items():
                if pct > 0:
                    print(f"{col}: {pct:.2f}%")
            
            print(f"\nSố dòng trùng lặp: {quality_stats[name]['duplicates']}")
            
            if 'outliers' in quality_stats[name]:
                print("\nThống kê giá trị ngoại lai:")
                for col, stats in quality_stats[name]['outliers'].items():
                    print(f"\n{col}:")
                    print(f"  - Giới hạn dưới: {stats['lower_bound']:.2f}")
                    print(f"  - Giới hạn trên: {stats['upper_bound']:.2f}")
                    print(f"  - Số giá trị ngoại lai: {stats['n_outliers']}")

        # Phân tích xu hướng thời gian
        print("\n3. Phân tích xu hướng thời gian...")
        for name, df in market_data.items():
            print(f"\n=== {name.upper()} DATA ===")
            print(f"Thời gian bắt đầu: {df['Date'].min()}")
            print(f"Thời gian kết thúc: {df['Date'].max()}")
            print(f"Số ngày dữ liệu: {len(df['Date'].unique())}")

        # Lấy danh sách mã chứng khoán
        symbols = market_data['pricing']['Symbol'].unique()
        print(f"\nTổng số mã chứng khoán: {len(symbols)}")
        print("\nMẫu một số mã chứng khoán:")
        print(symbols[:10])

        # Vẽ biểu đồ xu hướng giá
        print("\n4. Vẽ biểu đồ xu hướng giá...")
        sample_symbols = symbols[:5]
        plt.figure(figsize=(15, 8))
        
        for symbol in sample_symbols:
            symbol_data = market_data['pricing'][market_data['pricing']['Symbol'] == symbol]
            plt.plot(symbol_data['Date'], symbol_data['Close'], label=symbol)

        plt.title('Xu hướng giá của các mã chứng khoán mẫu')
        plt.xlabel('Thời gian')
        plt.ylabel('Giá đóng cửa')
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Tạo thư mục output nếu chưa tồn tại
        output_dir = Path('output')
        output_dir.mkdir(exist_ok=True)
        
        plt.savefig(output_dir / 'price_trends.png')
        plt.close()

        # Phân tích kỹ thuật
        print("\n5. Phân tích kỹ thuật...")
        sample_symbol = symbols[0]
        tech_data = calculate_technical_indicators(market_data['pricing'], sample_symbol)
        
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(15, 12))
        fig.suptitle(f'Phân tích kỹ thuật - {sample_symbol}', fontsize=16)
        
        # Plot 1: Giá và Bollinger Bands
        ax1.plot(tech_data['Date'], tech_data['Close'], label='Giá đóng cửa')
        ax1.plot(tech_data['Date'], tech_data['BB_middle'], label='BB Middle')
        ax1.plot(tech_data['Date'], tech_data['BB_upper'], label='BB Upper')
        ax1.plot(tech_data['Date'], tech_data['BB_lower'], label='BB Lower')
        ax1.set_title('Giá và Bollinger Bands')
        ax1.legend()
        
        # Plot 2: MACD
        ax2.plot(tech_data['Date'], tech_data['MACD'], label='MACD')
        ax2.plot(tech_data['Date'], tech_data['Signal'], label='Signal')
        ax2.axhline(y=0, color='r', linestyle='--')
        ax2.set_title('MACD')
        ax2.legend()
        
        # Plot 3: RSI
        ax3.plot(tech_data['Date'], tech_data['RSI'])
        ax3.axhline(y=70, color='r', linestyle='--')
        ax3.axhline(y=30, color='g', linestyle='--')
        ax3.set_title('RSI')
        
        plt.tight_layout()
        plt.savefig(output_dir / 'technical_analysis.png')
        plt.close()

        # Tạo báo cáo phân tích
        print("\n6. Tạo báo cáo phân tích...")
        with open(output_dir / 'analysis_report.md', 'w', encoding='utf-8') as f:
            f.write("# Báo cáo phân tích dữ liệu thị trường chứng khoán\n\n")
            
            # Thông tin cơ bản
            f.write("## 1. Thông tin cơ bản\n")
            for name, df in market_data.items():
                f.write(f"\n### {name.upper()} DATA\n")
                f.write(f"- Kích thước: {df.shape}\n")
                f.write(f"- Các cột: {', '.join(df.columns)}\n")
                f.write(f"- Thời gian: {df['Date'].min()} đến {df['Date'].max()}\n")
            
            # Vấn đề về chất lượng dữ liệu
            f.write("\n## 2. Vấn đề về chất lượng dữ liệu\n")
            for name, stats in quality_stats.items():
                f.write(f"\n### {name.upper()} DATA\n")
                
                # Dữ liệu thiếu
                f.write("\n#### Dữ liệu thiếu\n")
                missing_cols = {col: pct for col, pct in stats['missing'].items() if pct > 0}
                if missing_cols:
                    for col, pct in missing_cols.items():
                        f.write(f"- {col}: {pct:.2f}%\n")
                else:
                    f.write("- Không có dữ liệu thiếu\n")
                
                # Giá trị ngoại lai
                if 'outliers' in stats:
                    f.write("\n#### Giá trị ngoại lai\n")
                    for col, out_stats in stats['outliers'].items():
                        if out_stats['n_outliers'] > 0:
                            f.write(f"- {col}:\n")
                            f.write(f"  + Số lượng: {out_stats['n_outliers']}\n")
                            f.write(f"  + Giới hạn: [{out_stats['lower_bound']:.2f}, {out_stats['upper_bound']:.2f}]\n")
            
            # Đề xuất xử lý
            f.write("\n## 3. Đề xuất xử lý\n")
            f.write("\n### Xử lý dữ liệu thiếu\n")
            f.write("1. Đối với dữ liệu giá:\n")
            f.write("   - Sử dụng phương pháp forward fill cho dữ liệu thiếu\n")
            f.write("   - Loại bỏ các mã có quá nhiều dữ liệu thiếu (>20%)\n")
            
            f.write("\n### Xử lý giá trị ngoại lai\n")
            f.write("1. Đối với giá và khối lượng:\n")
            f.write("   - Kiểm tra và xác nhận các giá trị ngoại lai\n")
            f.write("   - Sử dụng winsorization để xử lý ngoại lai\n")
            
            f.write("\n### Tạo thêm đặc trưng\n")
            f.write("1. Đặc trưng kỹ thuật:\n")
            f.write("   - Momentum indicators\n")
            f.write("   - Volatility indicators\n")
            f.write("   - Volume indicators\n")
            
            f.write("\n2. Đặc trưng thống kê:\n")
            f.write("   - Rolling statistics\n")
            f.write("   - Return metrics\n")
            f.write("   - Correlation features\n")

        print("\nPhân tích hoàn tất! Kết quả đã được lưu vào thư mục output:")
        print("1. price_trends.png - Biểu đồ xu hướng giá")
        print("2. technical_analysis.png - Biểu đồ phân tích kỹ thuật")
        print("3. analysis_report.md - Báo cáo phân tích chi tiết")

    except Exception as e:
        print("\nLỗi trong quá trình phân tích:")
        print(f"Type: {type(e).__name__}")
        print(f"Message: {str(e)}")
        print("\nChi tiết lỗi:")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main() 