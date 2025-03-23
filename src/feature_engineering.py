# File: feature_engineering.py
# Mục đích: Tính toán các chỉ báo kỹ thuật và chuẩn bị dữ liệu cho mô hình
# Tác giả: Huỳnh Long Uyển (Học viên Cao học HUB)


import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Tuple, List
from sklearn.preprocessing import StandardScaler
from scipy import stats

def clean_stock_data(df: pd.DataFrame, missing_threshold: float = 0.5) -> pd.DataFrame:
    """
    Làm sạch dữ liệu cổ phiếu
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame chứa dữ liệu cổ phiếu
    missing_threshold : float, optional
        Ngưỡng tỷ lệ missing cho phép, mặc định 0.5
        
    Returns
    -------
    pd.DataFrame
        DataFrame đã được làm sạch
    """
    print("Bắt đầu làm sạch dữ liệu...")
    
    # Tạo bản sao để tránh warning
    df = df.copy()
    
    # Loại bỏ cột có quá nhiều missing
    missing_ratio = df.isnull().mean()
    cols_to_drop = missing_ratio[missing_ratio > missing_threshold].index
    if len(cols_to_drop) > 0:
        print(f"Loại bỏ {len(cols_to_drop)} cột có tỷ lệ missing > {missing_threshold}")
        df = df.drop(columns=cols_to_drop)
    
    # Xử lý outliers bằng winsorization
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    for col in numeric_cols:
        # Áp dụng winsorization 1%
        lower, upper = np.percentile(df[col].dropna(), [1, 99])
        df[col] = df[col].clip(lower=lower, upper=upper)
    
    # Điền missing values
    # 1. Dùng linear interpolation cho các khoảng trống ngắn
    df = df.interpolate(method='linear', limit_direction='both', axis=0)
    
    # 2. Dùng forward fill và backward fill cho các khoảng trống còn lại
    df = df.ffill()
    df = df.bfill()
    
    print("Hoàn thành làm sạch dữ liệu")
    return df

def calculate_momentum_indicators(df: pd.DataFrame, windows: List[int] = [5, 10, 20]) -> pd.DataFrame:
    """
    Tính toán các chỉ báo momentum
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame chứa dữ liệu giá
    windows : List[int], optional
        Danh sách các khoảng thời gian, mặc định [5, 10, 20]
        
    Returns
    -------
    pd.DataFrame
        DataFrame chứa các chỉ báo momentum
    """
    print("Tính toán chỉ báo momentum...")
    
    # Tạo dictionary chứa features
    features = {}
    
    # Chọn cột giá đóng cửa
    close_col = None
    for col in df.columns:
        if col.endswith('_Close'):
            close_col = col
            break
    
    if close_col is None:
        print("Warning: Không tìm thấy cột giá đóng cửa (kết thúc bằng _Close)")
        return pd.DataFrame(index=df.index)
    
    # Rate of Change (ROC)
    for window in windows:
        features[f'ROC_{window}'] = df[close_col].pct_change(window)
    
    # Moving Average Convergence Divergence (MACD)
    exp1 = df[close_col].ewm(span=12, adjust=False).mean()
    exp2 = df[close_col].ewm(span=26, adjust=False).mean()
    features['MACD'] = exp1 - exp2
    features['MACD_Signal'] = features['MACD'].ewm(span=9, adjust=False).mean()
    
    # Relative Strength Index (RSI)
    delta = df[close_col].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    features['RSI'] = 100 - (100 / (1 + rs))
    
    return pd.DataFrame(features, index=df.index)

def calculate_volume_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Tính toán các chỉ báo khối lượng
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame chứa dữ liệu giá và khối lượng
        
    Returns
    -------
    pd.DataFrame
        DataFrame chứa các chỉ báo khối lượng
    """
    print("Tính toán chỉ báo khối lượng...")
    
    # Tạo dictionary chứa features
    features = {}
    
    # Tìm cột giá đóng cửa và khối lượng
    close_col = None
    volume_col = None
    
    for col in df.columns:
        if col.endswith('_Close'):
            close_col = col
        elif col.endswith('_Volume'):
            volume_col = col
    
    if close_col is None or volume_col is None:
        print(f"Warning: Thiếu cột cần thiết (Close hoặc Volume)")
        return pd.DataFrame(index=df.index)
    
    # On-Balance Volume (OBV)
    price_change = df[close_col].diff()
    volume_pos = df[volume_col].where(price_change > 0, 0)
    volume_neg = df[volume_col].where(price_change < 0, 0)
    features['OBV'] = (volume_pos - volume_neg).cumsum()
    
    # Volume Price Trend (VPT)
    features['VPT'] = df[volume_col] * df[close_col].pct_change()
    features['VPT'] = features['VPT'].cumsum()
    
    # Price Volume Trend (PVT)
    features['PVT'] = df[volume_col] * (df[close_col] - df[close_col].shift(1)) / df[close_col].shift(1)
    features['PVT'] = features['PVT'].cumsum()
    
    return pd.DataFrame(features, index=df.index)

def calculate_volatility_indicators(df: pd.DataFrame, windows: List[int] = [20]) -> pd.DataFrame:
    """
    Tính toán các chỉ báo biến động
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame chứa dữ liệu giá
    windows : List[int], optional
        Danh sách các khoảng thời gian, mặc định [20]
        
    Returns
    -------
    pd.DataFrame
        DataFrame chứa các chỉ báo biến động
    """
    print("Tính toán chỉ báo biến động...")
    
    # Tạo dictionary chứa features
    features = {}
    
    # Tìm các cột giá
    close_col = None
    high_col = None
    low_col = None
    
    for col in df.columns:
        if col.endswith('_Close'):
            close_col = col
        elif col.endswith('_High'):
            high_col = col
        elif col.endswith('_Low'):
            low_col = col
    
    if any(col is None for col in [close_col, high_col, low_col]):
        print(f"Warning: Thiếu một số cột cần thiết (Close, High, Low)")
        return pd.DataFrame(index=df.index)
    
    # Bollinger Bands
    for window in windows:
        rolling_mean = df[close_col].rolling(window=window).mean()
        rolling_std = df[close_col].rolling(window=window).std()
        features[f'BB_Upper_{window}'] = rolling_mean + (2 * rolling_std)
        features[f'BB_Lower_{window}'] = rolling_mean - (2 * rolling_std)
        features[f'BB_Width_{window}'] = (features[f'BB_Upper_{window}'] - features[f'BB_Lower_{window}']) / rolling_mean
    
    # Average True Range (ATR)
    high_low = df[high_col] - df[low_col]
    high_close = np.abs(df[high_col] - df[close_col].shift())
    low_close = np.abs(df[low_col] - df[close_col].shift())
    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = np.max(ranges, axis=1)
    features['ATR'] = true_range.rolling(14).mean()
    
    # Historical Volatility
    for window in windows:
        log_return = np.log(df[close_col] / df[close_col].shift(1))
        features[f'Volatility_{window}'] = log_return.rolling(window).std() * np.sqrt(252)
    
    return pd.DataFrame(features, index=df.index)

def prepare_model_data(df: pd.DataFrame, target_col: str, test_size: float = 0.2) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Chuẩn bị dữ liệu cho mô hình
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame chứa features và target
    target_col : str
        Tên cột target
    test_size : float, optional
        Tỷ lệ dữ liệu test, mặc định 0.2
        
    Returns
    -------
    Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]
        X_train, X_test, y_train, y_test
    """
    print("Chuẩn bị dữ liệu cho mô hình...")
    
    # Tách features và target
    if target_col not in df.columns:
        raise ValueError(f"Không tìm thấy cột target {target_col}")
    
    X = df.drop(columns=[target_col])
    y = df[target_col]
    
    # Chuẩn hóa features
    scaler = StandardScaler()
    X_scaled = pd.DataFrame(
        scaler.fit_transform(X),
        columns=X.columns,
        index=X.index
    )
    
    # Chia train/test theo thời gian
    train_size = int(len(df) * (1 - test_size))
    X_train = X_scaled.iloc[:train_size]
    X_test = X_scaled.iloc[train_size:]
    y_train = y.iloc[:train_size]
    y_test = y.iloc[train_size:]
    
    print(f"Kích thước dữ liệu train: {X_train.shape}")
    print(f"Kích thước dữ liệu test: {X_test.shape}")
    
    return X_train, X_test, y_train, y_test

def process_and_save_data(
    data_dict: Dict[str, pd.DataFrame],
    output_dir: str,
    missing_threshold: float = 0.5
) -> None:
    """
    Xử lý và lưu dữ liệu đã xử lý
    
    Parameters
    ----------
    data_dict : Dict[str, pd.DataFrame]
        Dictionary chứa các DataFrame
    output_dir : str
        Đường dẫn thư mục output
    missing_threshold : float, optional
        Ngưỡng tỷ lệ missing cho phép, mặc định 0.5
    """
    print("Bắt đầu xử lý dữ liệu...")
    
    # Tạo thư mục output nếu chưa tồn tại
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Xử lý từng loại dữ liệu
    for name, df in data_dict.items():
        print(f"\nXử lý {name}...")
        
        # Làm sạch dữ liệu
        df_clean = clean_stock_data(df, missing_threshold)
        
        # Tính toán các chỉ báo
        momentum_features = calculate_momentum_indicators(df_clean)
        volume_features = calculate_volume_indicators(df_clean)
        volatility_features = calculate_volatility_indicators(df_clean)
        
        # Kết hợp tất cả features
        features = pd.concat(
            [df_clean, momentum_features, volume_features, volatility_features],
            axis=1
        )
        
        # Lưu dữ liệu đã xử lý
        output_file = output_dir / f"{name}_processed.csv"
        features.to_csv(output_file)
        print(f"Đã lưu dữ liệu đã xử lý vào {output_file}")
        print(f"Kích thước dữ liệu: {features.shape}")
        print("Các cột trong dữ liệu:")
        print(features.columns.tolist()) 