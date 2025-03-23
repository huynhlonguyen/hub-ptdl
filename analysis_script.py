"""
Tác giả: Huỳnh Long Uyển (Học viên Cao học HUB)
Mô tả: Script phân tích dữ liệu thị trường chứng khoán
- Phân tích thống kê cơ bản
- Vẽ biểu đồ xu hướng giá
- Tính toán ma trận tương quan
- Phân tích độ biến động
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

# Create output directory if not exists
output_dir = "output"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Read the data
df = pd.read_csv('data/stock-market-behavior-analysis/raw/market_data/pricing.csv')

# Convert date column to datetime
df['date'] = pd.to_datetime(df['date'])

# Basic data exploration
def analyze_data():
    # Get basic statistics
    stats = {
        'Number of stocks': len(df.columns) - 1,  # Excluding date column
        'Date range': f"From {df['date'].min()} to {df['date'].max()}",
        'Number of trading days': len(df),
    }
    
    # Calculate missing values
    missing_values = df.isnull().sum()
    stocks_with_missing = missing_values[missing_values > 0]
    
    # Calculate basic statistics for each stock
    stock_stats = df.drop('date', axis=1).describe()
    
    # Save results to text file
    with open(os.path.join(output_dir, 'analysis_report.txt'), 'w') as f:
        f.write("Basic Statistics:\n")
        for key, value in stats.items():
            f.write(f"{key}: {value}\n")
        
        f.write("\nStocks with missing values:\n")
        f.write(stocks_with_missing.to_string())
        
        f.write("\n\nStock Statistics:\n")
        f.write(stock_stats.to_string())

def plot_price_trends():
    # Select some major stocks for visualization
    major_stocks = ['VNM', 'VCB', 'BID', 'CTG', 'HPG']
    
    plt.figure(figsize=(15, 8))
    for stock in major_stocks:
        if stock in df.columns:
            plt.plot(df['date'], df[stock], label=stock)
    
    plt.title('Price Trends of Major Stocks')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'price_trends.png'))
    plt.close()

def calculate_returns():
    # Calculate daily returns
    returns = df.drop('date', axis=1).pct_change()
    
    # Calculate correlation matrix
    correlation = returns.corr()
    
    # Plot correlation heatmap
    plt.figure(figsize=(12, 8))
    sns.heatmap(correlation, cmap='coolwarm', center=0)
    plt.title('Stock Returns Correlation')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'correlation_heatmap.png'))
    plt.close()
    
    # Calculate volatility (standard deviation of returns)
    volatility = returns.std().sort_values(ascending=False)
    
    # Save volatility to file
    with open(os.path.join(output_dir, 'volatility_report.txt'), 'w') as f:
        f.write("Stock Volatility (Standard Deviation of Returns):\n")
        f.write(volatility.to_string())

def main():
    analyze_data()
    plot_price_trends()
    calculate_returns()
    print("Analysis completed. Check the output directory for results.")

if __name__ == "__main__":
    main() 