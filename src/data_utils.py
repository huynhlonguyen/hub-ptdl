# File: data_utils.py
# Mục đích: Cung cấp các hàm tiện ích để đọc và xử lý dữ liệu
# Tác giả: Huỳnh Long Uyển (Học viên Cao học HUB)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import Dict, List, Tuple, Union
from datetime import datetime, timedelta

def filter_recent_data(df: pd.DataFrame, years: int = 3) -> pd.DataFrame:
    """
    Lọc dữ liệu trong khoảng N năm gần nhất
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame cần lọc
    years : int
        Số năm dữ liệu cần giữ lại
        
    Returns
    -------
    pd.DataFrame
        DataFrame đã được lọc
    """
    if df.empty:
        return df
        
    if isinstance(df.index, pd.DatetimeIndex):
        end_date = df.index.max()
    else:
        end_date = pd.to_datetime(df.index).max()
        
    start_date = end_date - timedelta(days=years*365)
    return df[df.index >= start_date].copy()

def load_market_data(data_dir: Path) -> Dict[str, pd.DataFrame]:
    """
    Đọc dữ liệu thị trường từ các file CSV
    
    Parameters
    ----------
    data_dir : Path
        Đường dẫn đến thư mục chứa dữ liệu
        
    Returns
    -------
    Dict[str, pd.DataFrame]
        Dictionary chứa các DataFrame với key là tên file
    """
    data_files = {
        'pricing': 'pricing.csv',
        'trading_value': 'trading_value.csv',
        'market_return': 'market_return.csv'
    }
    
    data_dict = {}
    for name, filename in data_files.items():
        file_path = data_dir / filename
        try:
            print(f"Đọc file {filename}...")
            # Đọc dữ liệu với các tham số phù hợp
            if name == 'market_return':
                df = pd.read_csv(
                    file_path,
                    parse_dates=['month'],
                    thousands=','
                )
                # Chuẩn hóa tên cột ngày
                df = df.rename(columns={'month': 'Date'})
            else:
                df = pd.read_csv(
                    file_path,
                    parse_dates=['date'],
                    thousands=',',
                    na_values=['']  # Xử lý các ô trống
                )
                # Chuẩn hóa tên cột ngày
                df = df.rename(columns={'date': 'Date'})
            
            # Đặt Date làm index
            df.set_index('Date', inplace=True)
            
            # Chuyển các cột số sang kiểu float
            numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
            df[numeric_cols] = df[numeric_cols].astype(float)
            
            # Sắp xếp theo ngày
            df.sort_index(inplace=True)
            
            # Lọc dữ liệu 3 năm gần nhất
            df = filter_recent_data(df)
            
            # Lưu vào dictionary
            data_dict[name] = df
            print(f"Đã đọc {filename}: {df.shape}")
            print(f"Khoảng thời gian: {df.index.min()} đến {df.index.max()}")
            
        except Exception as e:
            print(f"Lỗi khi đọc {filename}: {str(e)}")
            print(f"Nội dung 5 dòng đầu của file:")
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    for i, line in enumerate(f):
                        if i < 5:
                            print(line.strip())
                        else:
                            break
            except Exception as e:
                print(f"Không thể đọc nội dung file: {str(e)}")
            continue
    
    return data_dict

def analyze_data_quality(df: pd.DataFrame, name: str) -> Dict[str, any]:
    """
    Phân tích chất lượng dữ liệu của một DataFrame
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame cần phân tích
    name : str
        Tên của dataset
        
    Returns:
    --------
    Dict[str, any]
        Dictionary chứa các thông số về chất lượng dữ liệu
    """
    quality_stats = {}
    
    # Thông tin cơ bản
    quality_stats['name'] = name
    quality_stats['shape'] = df.shape
    quality_stats['columns'] = list(df.columns)
    
    # Kiểm tra dữ liệu thiếu
    missing = df.isnull().sum()
    missing_pct = (missing / len(df)) * 100
    quality_stats['missing'] = dict(zip(df.columns, missing_pct))
    
    # Kiểm tra giá trị trùng lặp
    quality_stats['duplicates'] = df.duplicated().sum()
    
    # Thống kê cho các cột số
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        quality_stats['numeric_stats'] = df[numeric_cols].describe()
        
        # Kiểm tra giá trị ngoại lai
        outliers = {}
        for col in numeric_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            outliers[col] = {
                'lower_bound': Q1 - 1.5 * IQR,
                'upper_bound': Q3 + 1.5 * IQR,
                'n_outliers': len(df[(df[col] < Q1 - 1.5 * IQR) | (df[col] > Q3 + 1.5 * IQR)])
            }
        quality_stats['outliers'] = outliers
    
    return quality_stats

def calculate_technical_indicators(df: pd.DataFrame, symbol: str) -> pd.DataFrame:
    """
    Tính toán các chỉ báo kỹ thuật cho một mã cổ phiếu.

    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame chứa dữ liệu giá
    symbol : str
        Mã cổ phiếu cần tính toán

    Returns:
    --------
    pd.DataFrame
        DataFrame chứa các chỉ báo kỹ thuật đã tính toán
    """
    # Lấy dữ liệu của symbol và chuyển thành dạng time series
    data = pd.DataFrame(df[symbol])
    data.columns = ['Close']
    data = data.sort_index()
    
    # Tính SMA
    data['SMA_20'] = data['Close'].rolling(window=20).mean()
    data['SMA_50'] = data['Close'].rolling(window=50).mean()
    
    # Tính EMA
    data['EMA_12'] = data['Close'].ewm(span=12, adjust=False).mean()
    data['EMA_26'] = data['Close'].ewm(span=26, adjust=False).mean()
    
    # Tính MACD
    data['MACD'] = data['EMA_12'] - data['EMA_26']
    data['Signal'] = data['MACD'].ewm(span=9, adjust=False).mean()
    
    # Tính RSI
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))
    
    # Tính Bollinger Bands
    data['BB_middle'] = data['Close'].rolling(window=20).mean()
    bb_std = data['Close'].rolling(window=20).std()
    data['BB_upper'] = data['BB_middle'] + (bb_std * 2)
    data['BB_lower'] = data['BB_middle'] - (bb_std * 2)
    
    return data

def plot_technical_analysis(data: pd.DataFrame, symbol: str) -> None:
    """
    Vẽ đồ thị phân tích kỹ thuật cho một mã chứng khoán
    
    Parameters:
    -----------
    data : pd.DataFrame
        DataFrame chứa các chỉ báo kỹ thuật
    symbol : str
        Mã chứng khoán cần vẽ
    """
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(15, 12))
    fig.suptitle(f'Phân tích kỹ thuật - {symbol}', fontsize=16)
    
    # Plot 1: Giá và Bollinger Bands
    ax1.plot(data.index, data['Close'], label='Giá đóng cửa')
    ax1.plot(data.index, data['BB_middle'], label='BB Middle')
    ax1.plot(data.index, data['BB_upper'], label='BB Upper')
    ax1.plot(data.index, data['BB_lower'], label='BB Lower')
    ax1.set_title('Giá và Bollinger Bands')
    ax1.legend()
    ax1.grid(True)
    
    # Plot 2: MACD
    ax2.plot(data.index, data['MACD'], label='MACD')
    ax2.plot(data.index, data['Signal'], label='Signal')
    ax2.axhline(y=0, color='r', linestyle='--')
    ax2.set_title('MACD')
    ax2.legend()
    ax2.grid(True)
    
    # Plot 3: RSI
    ax3.plot(data.index, data['RSI'])
    ax3.axhline(y=70, color='r', linestyle='--')
    ax3.axhline(y=30, color='g', linestyle='--')
    ax3.set_title('RSI')
    ax3.grid(True)
    
    # Xoay label trục x để dễ đọc
    for ax in [ax1, ax2, ax3]:
        ax.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.show() 