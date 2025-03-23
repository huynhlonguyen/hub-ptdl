"""
File: sentiment_analysis.py
Mục đích: Phân tích sentiment thị trường chứng khoán
Tác giả: Huỳnh Long Uyển (Học viên Cao học HUB)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

class SentimentAnalyzer:
    def __init__(self, data_dir: str = 'data/stock-market-behavior-analysis/raw/market_data'):
        """
        Khởi tạo SentimentAnalyzer

        Parameters:
        -----------
        data_dir : str
            Đường dẫn đến thư mục chứa dữ liệu
        """
        self.data_dir = Path(data_dir)
        self.output_dir = Path('output/sentiment')
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Thiết lập style cho đồ thị
        plt.style.use('default')  # Sử dụng style mặc định của matplotlib
        sns.set_theme(style='whitegrid')  # Sử dụng theme của seaborn
        
        # Cấu hình matplotlib
        plt.rcParams.update({
            'figure.figsize': (15, 10),
            'font.size': 12,
            'axes.grid': True,
            'grid.alpha': 0.3
        })
        
    def load_data(self):
        """
        Đọc dữ liệu từ các file csv
        """
        # Đọc dữ liệu
        self.pricing = pd.read_csv(self.data_dir / 'pricing.csv', parse_dates=['date'], index_col='date')
        self.trading_value = pd.read_csv(self.data_dir / 'trading_value.csv', parse_dates=['date'], index_col='date')
        
        print(f"Đã đọc dữ liệu từ {self.data_dir}")
        print(f"Khoảng thời gian: {self.pricing.index.min()} đến {self.pricing.index.max()}")
        
    def calculate_market_turnover(self):
        """
        Tính toán Market Turnover
        """
        # Tính tổng giá trị giao dịch hàng ngày
        daily_value = self.trading_value.sum(axis=1)
        
        # Tính Market Turnover (tỷ lệ so với trung bình 20 ngày)
        market_turnover = daily_value / daily_value.rolling(window=20, min_periods=1).mean()
        
        return market_turnover
    
    def calculate_advance_decline_ratio(self):
        """
        Tính toán Advance/Decline Ratio
        """
        # Tính số lượng cổ phiếu tăng/giảm
        price_change = self.pricing.pct_change()
        advances = (price_change > 0).sum(axis=1)
        declines = (price_change < 0).sum(axis=1)
        
        # Tính ADR
        adr = advances / declines.replace(0, 1)  # Tránh chia cho 0
        
        return adr
    
    def calculate_share_turnover(self):
        """
        Tính toán Share Turnover
        """
        # Tính Share Turnover cho từng cổ phiếu
        share_turnover = self.trading_value.div(self.pricing)
        
        # Lấy trung bình của toàn thị trường
        market_share_turnover = share_turnover.mean(axis=1)
        
        return market_share_turnover
    
    def collect_market_data(self):
        """
        Thu thập và tính toán các chỉ số thị trường
        """
        print("Bắt đầu thu thập dữ liệu thị trường...")
        
        try:
            # Tính các chỉ số
            market_turnover = self.calculate_market_turnover()
            adr = self.calculate_advance_decline_ratio()
            share_turnover = self.calculate_share_turnover()
            
            # Gộp các chỉ số
            market_indicators = pd.DataFrame({
                'Market_Turnover': market_turnover,
                'ADR': adr,
                'Share_Turnover': share_turnover
            })
            
            # Lưu kết quả
            market_indicators.to_csv(self.output_dir / 'market_indicators.csv')
            print(f"Đã lưu chỉ số thị trường vào {self.output_dir / 'market_indicators.csv'}")
            
            # Vẽ đồ thị
            self.plot_trends(market_indicators)
            
            # In thống kê
            self._print_statistics(market_indicators)
            
            return market_indicators
            
        except Exception as e:
            print(f"Lỗi khi thu thập dữ liệu: {str(e)}")
            return None
    
    def _print_statistics(self, df):
        """
        In thống kê về các chỉ số
        """
        print("\nThống kê chỉ số thị trường:")
        print("-" * 40)
        print(f"Số lượng bản ghi: {len(df)}")
        print(f"\nADR trung bình: {df['ADR'].mean():.2f}")
        print(f"ADR cao nhất: {df['ADR'].max():.2f}")
        print(f"ADR thấp nhất: {df['ADR'].min():.2f}")
        print(f"Độ lệch chuẩn ADR: {df['ADR'].std():.2f}")
        
    def plot_trends(self, df):
        """
        Vẽ đồ thị xu hướng các chỉ số
        """
        fig, axes = plt.subplots(3, 1, figsize=(15, 12))
        fig.suptitle('Chỉ số Sentiment Thị trường', fontsize=14)
        
        # Plot Market Turnover
        df['Market_Turnover'].plot(ax=axes[0], color='blue')
        axes[0].set_title('Market Turnover')
        axes[0].set_ylabel('Tỷ lệ')
        axes[0].grid(True)
        
        # Plot ADR
        df['ADR'].plot(ax=axes[1], color='green')
        axes[1].axhline(y=1, color='r', linestyle='--', alpha=0.5)
        axes[1].set_title('Advance/Decline Ratio')
        axes[1].set_ylabel('Tỷ lệ')
        axes[1].grid(True)
        
        # Plot Share Turnover
        df['Share_Turnover'].plot(ax=axes[2], color='purple')
        axes[2].set_title('Share Turnover')
        axes[2].set_ylabel('Tỷ lệ')
        axes[2].grid(True)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'market_trends.png', dpi=300, bbox_inches='tight')
        print(f"Đã lưu biểu đồ xu hướng vào {self.output_dir / 'market_trends.png'}")
        plt.close()

def main():
    """
    Hàm chính để chạy phân tích
    """
    analyzer = SentimentAnalyzer()
    analyzer.load_data()
    analyzer.collect_market_data()

if __name__ == "__main__":
    main() 