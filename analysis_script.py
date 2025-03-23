"""
File: analysis_script.py
Chức năng: Phân tích kỹ thuật và trực quan hóa dữ liệu chứng khoán
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import logging
from src.config import (
    VN30_SYMBOLS, OUTPUT_DIR, PLOT_STYLE,
    LOG_FILE, LOG_FORMAT
)

# Thiết lập logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format=LOG_FORMAT
)

# Thiết lập style cho matplotlib
for key, value in PLOT_STYLE.items():
    plt.rcParams[key] = value

def load_data():
    """Đọc dữ liệu đã thu thập"""
    try:
        df = pd.read_csv(OUTPUT_DIR / "stock_data.csv")
        df['date'] = pd.to_datetime(df['date'])
        logging.info("Đã đọc dữ liệu thành công")
        return df
    except Exception as e:
        logging.error(f"Lỗi khi đọc dữ liệu: {str(e)}")
        return None

def calculate_technical_indicators(df, symbol):
    """Tính toán các chỉ báo kỹ thuật cho một mã cổ phiếu"""
    try:
        # Chuẩn bị dữ liệu
        data = pd.DataFrame()
        data['date'] = df['date']
        data['close'] = df[f'{symbol}_close']
        data['high'] = df[f'{symbol}_high']
        data['low'] = df[f'{symbol}_low']
        data['volume'] = df[f'{symbol}_volume']
        
        # Tính MA20, MA50
        data['MA20'] = data['close'].rolling(window=20).mean()
        data['MA50'] = data['close'].rolling(window=50).mean()
        
        # Tính RSI
        delta = data['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        data['RSI'] = 100 - (100 / (1 + rs))
        
        # Tính MACD
        exp1 = data['close'].ewm(span=12, adjust=False).mean()
        exp2 = data['close'].ewm(span=26, adjust=False).mean()
        data['MACD'] = exp1 - exp2
        data['Signal'] = data['MACD'].ewm(span=9, adjust=False).mean()
        
        # Tính Bollinger Bands
        data['BB_middle'] = data['close'].rolling(window=20).mean()
        std = data['close'].rolling(window=20).std()
        data['BB_upper'] = data['BB_middle'] + (std * 2)
        data['BB_lower'] = data['BB_middle'] - (std * 2)
        
        return data
    except Exception as e:
        logging.error(f"Lỗi khi tính chỉ báo kỹ thuật cho {symbol}: {str(e)}")
        return None

def plot_technical_analysis(df, symbol):
    """Vẽ biểu đồ phân tích kỹ thuật cho một mã cổ phiếu"""
    try:
        data = calculate_technical_indicators(df, symbol)
        if data is None:
            return
        
        # Tạo subplot
        fig = plt.figure(figsize=(15, 12))
        gs = fig.add_gridspec(3, 1, height_ratios=[2, 1, 1])
        
        # Plot 1: Giá và các đường MA, Bollinger Bands
        ax1 = fig.add_subplot(gs[0])
        ax1.plot(data.index, data['close'], label='Giá đóng cửa', color='blue')
        ax1.plot(data.index, data['MA20'], label='MA20', color='orange')
        ax1.plot(data.index, data['MA50'], label='MA50', color='red')
        ax1.plot(data.index, data['BB_upper'], label='BB Upper', color='gray', linestyle='--')
        ax1.plot(data.index, data['BB_lower'], label='BB Lower', color='gray', linestyle='--')
        ax1.fill_between(data.index, data['BB_upper'], data['BB_lower'], alpha=0.1)
        ax1.set_title(f'Phân tích kỹ thuật {symbol}')
        ax1.legend()
        ax1.grid(True)
        
        # Plot 2: RSI
        ax2 = fig.add_subplot(gs[1])
        ax2.plot(data.index, data['RSI'], color='purple')
        ax2.axhline(y=70, color='r', linestyle='--')
        ax2.axhline(y=30, color='g', linestyle='--')
        ax2.set_title('RSI (14)')
        ax2.grid(True)
        
        # Plot 3: MACD
        ax3 = fig.add_subplot(gs[2])
        ax3.plot(data.index, data['MACD'], label='MACD')
        ax3.plot(data.index, data['Signal'], label='Signal')
        ax3.bar(data.index, data['MACD'] - data['Signal'], alpha=0.3)
        ax3.set_title('MACD')
        ax3.legend()
        ax3.grid(True)
        
        # Định dạng chung
        plt.tight_layout()
        plt.savefig(OUTPUT_DIR / f'technical_analysis_{symbol}.png')
        plt.close()
        
        logging.info(f"Đã tạo biểu đồ phân tích kỹ thuật cho {symbol}")
    except Exception as e:
        logging.error(f"Lỗi khi vẽ biểu đồ cho {symbol}: {str(e)}")

def analyze_market():
    """Phân tích tổng thể thị trường"""
    try:
        df = load_data()
        if df is None:
            return
        
        # Tạo ma trận tương quan giữa các mã
        close_cols = [col for col in df.columns if col.endswith('_close')]
        correlation = df[close_cols].corr()
        
        plt.figure(figsize=(15, 12))
        sns.heatmap(correlation, 
                   cmap='coolwarm', 
                   center=0,
                   annot=True, 
                   fmt='.2f', 
                   square=True)
        plt.title('Tương quan giữa các mã VN30')
        plt.tight_layout()
        plt.savefig(OUTPUT_DIR / 'correlation_heatmap.png')
        plt.close()
        
        # Phân tích phân phối lợi nhuận
        returns = pd.DataFrame()
        for col in close_cols:
            symbol = col.replace('_close', '')
            returns[symbol] = df[col].pct_change()
        
        plt.figure(figsize=(15, 8))
        for symbol in VN30_SYMBOLS[:5]:  # Chỉ vẽ 5 mã để tránh rối
            if symbol in returns.columns:
                sns.kdeplot(returns[symbol].dropna(), label=symbol)
        plt.title('Phân phối lợi nhuận các mã VN30')
        plt.xlabel('Lợi nhuận')
        plt.ylabel('Mật độ')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(OUTPUT_DIR / 'returns_distribution.png')
        plt.close()
        
        logging.info("Đã hoàn thành phân tích thị trường")
    except Exception as e:
        logging.error(f"Lỗi khi phân tích thị trường: {str(e)}")

def main():
    """Hàm chính"""
    df = load_data()
    if df is None:
        return
    
    # Phân tích từng mã
    for symbol in VN30_SYMBOLS:
        plot_technical_analysis(df, symbol)
    
    # Phân tích thị trường
    analyze_market()
    
    logging.info("Đã hoàn thành toàn bộ phân tích")

if __name__ == "__main__":
    main() 