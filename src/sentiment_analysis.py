"""
Tác giả: Huỳnh Long Uyển (Học viên Cao học HUB)
Mô tả: Script thu thập và phân tích dữ liệu sentiment của nhà đầu tư
- Thu thập dữ liệu từ các nguồn trực tuyến
- Tính toán chỉ số sentiment
- Phân tích mối quan hệ với biến động giá
"""

import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import requests
from bs4 import BeautifulSoup
import datetime
import os
import matplotlib.pyplot as plt
import seaborn as sns

class SentimentAnalyzer:
    def __init__(self):
        self.output_dir = "output/sentiment"
        self.data_dir = "data/stock-market-behavior-analysis/raw/market_data"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            
    def collect_market_data(self):
        """Thu thập và tính toán các chỉ số sentiment từ dữ liệu thị trường"""
        try:
            # Đọc dữ liệu giá và giá trị giao dịch
            price_df = pd.read_csv(os.path.join(self.data_dir, "pricing.csv"))
            value_df = pd.read_csv(os.path.join(self.data_dir, "trading_value.csv"))
            
            # Chuyển đổi cột date sang datetime
            price_df['date'] = pd.to_datetime(price_df['date'])
            value_df['date'] = pd.to_datetime(value_df['date'])
            
            # Lọc dữ liệu 5 năm gần nhất
            five_years_ago = datetime.datetime.now() - datetime.timedelta(days=5*365)
            price_df = price_df[price_df['date'] >= five_years_ago]
            value_df = value_df[value_df['date'] >= five_years_ago]
            
            print(f"Phân tích dữ liệu từ {price_df['date'].min()} đến {price_df['date'].max()}")
            
            # Tính Market Turnover (MT) - sử dụng giá trị giao dịch thay vì khối lượng
            def calculate_market_turnover(price_df, value_df):
                """Tính tỷ lệ Market Turnover = Trading Value / Total Market Cap"""
                mt = pd.DataFrame()
                mt['date'] = price_df['date']
                total_value = value_df.drop('date', axis=1).sum(axis=1)
                total_market_cap = (price_df.drop('date', axis=1)).sum(axis=1)
                mt['market_turnover'] = total_value / total_market_cap
                return mt
                
            # Tính Advance-Decline Ratio (ADR)
            def calculate_adr(price_df):
                """Tính tỷ lệ số mã tăng/giảm"""
                price_changes = price_df.drop('date', axis=1).pct_change()
                advances = (price_changes > 0).sum(axis=1)
                declines = (price_changes < 0).sum(axis=1)
                adr = pd.DataFrame()
                adr['date'] = price_df['date']
                adr['adr'] = advances / declines
                return adr
                
            # Tính Share Turnover
            def calculate_share_turnover(price_df, value_df):
                """Tính Share Turnover = Trading Value / Market Cap cho từng cổ phiếu"""
                st = pd.DataFrame()
                st['date'] = price_df['date']
                
                # Tính tổng giá trị giao dịch và vốn hóa
                trading_value = value_df.drop('date', axis=1).sum(axis=1)
                market_cap = price_df.drop('date', axis=1).sum(axis=1)
                
                # Tính share turnover trung bình
                st['share_turnover'] = trading_value / market_cap
                return st
                
            # Thu thập và tổng hợp các chỉ số
            market_turnover = calculate_market_turnover(price_df, value_df)
            adr = calculate_adr(price_df)
            share_turnover = calculate_share_turnover(price_df, value_df)
            
            # Gộp các chỉ số
            market_indicators = pd.merge(market_turnover, adr, on='date')
            market_indicators = pd.merge(market_indicators, share_turnover, on='date')
            
            # Lưu kết quả
            market_indicators.to_csv(os.path.join(self.output_dir, 'market_indicators.csv'), index=False)
            print(f"Đã lưu các chỉ số thị trường vào {self.output_dir}/market_indicators.csv")
            
            # Vẽ biểu đồ xu hướng
            self.plot_trends(market_indicators)
            
            return market_indicators
            
        except Exception as e:
            print(f"Lỗi khi tính toán chỉ số thị trường: {str(e)}")
            return None
        
    def collect_social_sentiment(self):
        """Thu thập dữ liệu sentiment từ mạng xã hội"""
        # Vietstock forum
        # Cafef
        # Facebook groups
        pass
        
    def calculate_sentiment_index(self):
        """Tính toán chỉ số sentiment tổng hợp"""
        # Chuẩn hóa dữ liệu
        # PCA analysis
        # Tính trọng số
        pass
        
    def analyze_relationships(self):
        """Phân tích mối quan hệ giữa sentiment và giá"""
        # Tương quan
        # GARCH model
        # Granger causality
        pass
        
    def save_results(self):
        """Lưu kết quả phân tích"""
        pass

    def plot_trends(self, df):
        """Vẽ biểu đồ xu hướng các chỉ số thị trường"""
        # Set style
        plt.rcParams['figure.figsize'] = [12, 12]
        plt.rcParams['figure.dpi'] = 100
        
        fig, axes = plt.subplots(3, 1)
        fig.suptitle('Xu hướng các chỉ số thị trường', fontsize=16)
        
        # Market Turnover
        axes[0].plot(df['date'], df['market_turnover'], color='blue')
        axes[0].set_title('Market Turnover')
        axes[0].set_xlabel('Thời gian')
        axes[0].set_ylabel('Tỷ lệ')
        axes[0].tick_params(axis='x', rotation=45)
        axes[0].grid(True, alpha=0.3)
        
        # Advance-Decline Ratio
        axes[1].plot(df['date'], df['adr'], color='green')
        axes[1].set_title('Advance-Decline Ratio')
        axes[1].set_xlabel('Thời gian')
        axes[1].set_ylabel('Tỷ lệ')
        axes[1].tick_params(axis='x', rotation=45)
        axes[1].axhline(y=1, color='r', linestyle='--', alpha=0.3)
        axes[1].grid(True, alpha=0.3)
        
        # Share Turnover
        axes[2].plot(df['date'], df['share_turnover'], color='purple')
        axes[2].set_title('Share Turnover')
        axes[2].set_xlabel('Thời gian')
        axes[2].set_ylabel('Tỷ lệ')
        axes[2].tick_params(axis='x', rotation=45)
        axes[2].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'market_trends.png'))
        plt.close()
        print(f"Đã lưu biểu đồ xu hướng vào {self.output_dir}/market_trends.png")

def main():
    analyzer = SentimentAnalyzer()
    market_indicators = analyzer.collect_market_data()
    if market_indicators is not None:
        print("\nThống kê các chỉ số thị trường:")
        print(market_indicators.describe())
    
if __name__ == "__main__":
    main() 