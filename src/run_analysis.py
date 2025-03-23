"""
File: run_analysis.py
Chức năng: Script chính để chạy toàn bộ quy trình phân tích
"""

import os
import logging
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
from config import *
from feature_engineering import calculate_technical_indicators
from model_training import TwoLayerModel
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import warnings
warnings.filterwarnings('ignore')

# Thiết lập logging với encoding UTF-8
logging.basicConfig(
    filename='analysis.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

def validate_data(df, name):
    """Kiểm tra tính hợp lệ của dữ liệu"""
    # Kiểm tra dữ liệu trống
    if df is None or df.empty:
        raise ValueError(f"Dữ liệu {name} trống")
    
    # Kiểm tra index là datetime
    if not isinstance(df.index, pd.DatetimeIndex):
        raise ValueError(f"Index của {name} phải là datetime")
    
    # Kiểm tra các cột cần thiết
    required_patterns = ['_open', '_high', '_low', '_close', '_volume']
    for pattern in required_patterns:
        if not any(col.endswith(pattern) for col in df.columns):
            raise ValueError(f"Thiếu các cột kết thúc bằng {pattern} trong {name}")

def load_data():
    """Đọc và chuẩn bị dữ liệu"""
    try:
        # Đọc dữ liệu từ file CSV
        df = pd.read_csv(os.path.join(OUTPUT_DIR, 'stock_data.csv'))
        
        # Chuyển cột date thành datetime và đặt làm index
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)
        
        # Kiểm tra tính hợp lệ của dữ liệu
        validate_data(df, 'stock_data')
        
        logging.info(f"Đã đọc dữ liệu: {df.shape}")
        logging.info(f"Khoảng thời gian: {df.index.min()} đến {df.index.max()}")
        
        return df
    except Exception as e:
        logging.error(f"Lỗi khi đọc dữ liệu: {str(e)}")
        raise

def evaluate_model(model, X_test, y_test):
    """Đánh giá hiệu suất của mô hình"""
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
    
    # Dự đoán
    y_pred = model.predict(X_test)
    
    # Tính các metrics
    metrics = {
        'accuracy': accuracy_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred, average='weighted'),
        'recall': recall_score(y_test, y_pred, average='weighted'),
        'f1': f1_score(y_test, y_pred, average='weighted')
    }
    
    # Log kết quả
    for metric, value in metrics.items():
        logging.info(f"{metric.capitalize()}: {value:.4f}")
    
    return metrics

def setup_logging():
    """
    Thiết lập logging
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('analysis.log', encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )

def prepare_features(df):
    """
    Chuẩn bị features cho mô hình
    """
    # Tính toán các chỉ báo kỹ thuật
    features = calculate_technical_indicators(df)
    
    # Xóa các dòng có giá trị NaN
    features = features.dropna()
    
    return features

def create_labels(df, features_index, threshold=0.01):
    """
    Tạo nhãn cho dữ liệu dựa trên biến động giá
    1: tăng mạnh (> threshold)
    0: đi ngang (-threshold <= x <= threshold)
    -1: giảm mạnh (< -threshold)
    """
    # Chỉ lấy dữ liệu cho các ngày có trong features
    df = df.loc[features_index]
    
    labels = pd.DataFrame(index=df.index)
    
    for symbol in ['ACB', 'BID', 'BVH', 'CTG', 'FPT', 'GAS', 'HPG', 'MBB', 'MSN', 
                  'MWG', 'NVL', 'PLX', 'POW', 'SAB', 'SSI', 'STB', 'TCB', 'TPB', 
                  'VCB', 'VHM', 'VIC', 'VJC', 'VNM', 'VPB', 'VRE']:
        close_col = f'{symbol}_close'
        if close_col in df.columns:
            # Tính phần trăm thay đổi
            pct_change = df[close_col].pct_change()
            
            # Tạo nhãn
            labels[symbol] = 0  # Giá trị mặc định: đi ngang
            labels.loc[pct_change > threshold, symbol] = 1  # Tăng
            labels.loc[pct_change < -threshold, symbol] = -1  # Giảm
    
    return labels

def split_data(features, labels, test_size=0.2):
    """
    Chia dữ liệu thành tập train và test
    """
    # Lấy ngày cuối cùng cho tập test
    test_start_date = features.index[-int(len(features) * test_size)]
    
    # Chia dữ liệu
    train_features = features[features.index < test_start_date]
    test_features = features[features.index >= test_start_date]
    train_labels = labels[labels.index < test_start_date]
    test_labels = labels[labels.index >= test_start_date]
    
    return train_features, test_features, train_labels, test_labels

def find_best_params(X_train, y_train):
    """
    Tìm hyperparameters tối ưu cho Random Forest
    """
    param_grid = {
        'n_estimators': [50, 100, 200],
        'max_depth': [5, 10, 15, None],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4]
    }
    
    model = TwoLayerModel()
    grid_search = GridSearchCV(
        estimator=model.rf,
        param_grid=param_grid,
        cv=5,
        n_jobs=-1,
        scoring='f1_macro'
    )
    
    grid_search.fit(X_train, y_train)
    
    print("\nKết quả tìm hyperparameters tối ưu:")
    print(f"Best parameters: {grid_search.best_params_}")
    print(f"Best cross-validation score: {grid_search.best_score_:.3f}")
    
    return grid_search.best_params_

def analyze_feature_importance(model, feature_names):
    """
    Phân tích và vẽ biểu đồ độ quan trọng của features
    """
    # Lấy độ quan trọng của features
    importance_dict = model.get_feature_importance(feature_names)
    
    # Vẽ biểu đồ
    plt.figure(figsize=(12, 6))
    plt.bar(importance_dict.keys(), importance_dict.values())
    plt.xticks(rotation=45, ha='right')
    plt.title('Feature Importance')
    plt.tight_layout()
    plt.savefig('output/feature_importance.png')
    plt.close()
    
    # In ra top 5 features quan trọng nhất
    print("\nTop 5 features quan trọng nhất:")
    for feature, importance in list(importance_dict.items())[:5]:
        print(f"{feature}: {importance:.4f}")

def main():
    """Hàm chính để chạy toàn bộ quy trình phân tích"""
    try:
        logging.info("Thiết lập môi trường...")
        
        # Thiết lập logging
        setup_logging()
        logging.info("Bắt đầu phân tích...")
        
        # 1. Đọc dữ liệu
        print("\n1. Đọc dữ liệu")
        print("-" * 40)
        df = load_data()
        print(f"Đã đọc dữ liệu từ {df.index.min()} đến {df.index.max()}")
        
        # 2. Chuẩn bị features
        print("\n2. Chuẩn bị features")
        print("-" * 40)
        features = prepare_features(df)
        print(f"Số features: {features.shape[1]}")
        
        # 3. Tạo nhãn
        print("\n3. Tạo nhãn")
        print("-" * 40)
        labels = create_labels(df, features.index)
        print(f"Số nhãn: {labels.shape[1]}")
        
        # In thông tin về dữ liệu
        print("\nThông tin chi tiết về dữ liệu:")
        print(f"Features shape: {features.shape}")
        print(f"Labels shape: {labels.shape}")
        print("\nMẫu features:")
        print(features.head())
        print("\nMẫu labels:")
        print(labels.head())
        
        # 4. Chia dữ liệu
        X_train, X_test, y_train, y_test = split_data(features, labels)
        print(f"\nKích thước tập train: {X_train.shape}")
        print(f"Kích thước tập test: {X_test.shape}")
        
        # Kiểm tra kích thước dữ liệu huấn luyện
        print("\nKiểm tra kích thước dữ liệu huấn luyện:")
        print(f"X_train shape: {X_train.shape}")
        print(f"y_train shape: {y_train.shape}")
        print(f"X_test shape: {X_test.shape}")
        print(f"y_test shape: {y_test.shape}")
        
        # Chọn một cổ phiếu để huấn luyện (ví dụ: VCB)
        symbol = 'VCB'
        y_train_symbol = y_train[symbol]
        y_test_symbol = y_test[symbol]
        
        # 5. Tìm hyperparameters tối ưu
        print(f"\n4. Tìm hyperparameters tối ưu cho {symbol}")
        print("-" * 40)
        best_params = find_best_params(X_train, y_train_symbol)
        
        # 6. Huấn luyện mô hình với hyperparameters tối ưu
        print(f"\n5. Huấn luyện mô hình cho {symbol}")
        print("-" * 40)
        model = TwoLayerModel(
            n_estimators=best_params['n_estimators'],
            max_depth=best_params['max_depth'],
            min_samples_split=best_params['min_samples_split'],
            min_samples_leaf=best_params['min_samples_leaf']
        )
        print("Bắt đầu huấn luyện Random Forest...")
        model.fit(X_train, y_train_symbol)
        
        # 7. Phân tích độ quan trọng của features
        print("\n6. Phân tích độ quan trọng của features")
        print("-" * 40)
        analyze_feature_importance(model, features.columns)
        
        # 8. Đánh giá mô hình
        print("\n7. Đánh giá mô hình")
        print("-" * 40)
        y_pred = model.predict(X_test)
        
        # In báo cáo phân loại
        print(f"\nBáo cáo phân loại cho {symbol}:")
        print(classification_report(y_test_symbol, y_pred))
        
        # Vẽ confusion matrix
        plt.figure(figsize=(10, 8))
        cm = confusion_matrix(y_test_symbol, y_pred)
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
        plt.title(f'Confusion Matrix - {symbol}')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.savefig('output/confusion_matrix.png')
        plt.close()
        
        logging.info("Phân tích hoàn tất")
        
    except Exception as e:
        logging.error(f"Lỗi: {str(e)}")
        raise

if __name__ == "__main__":
    main() 