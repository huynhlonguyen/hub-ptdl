"""
File: model_training.py
Mục đích: Huấn luyện mô hình dự đoán xu hướng thị trường chứng khoán
Tác giả: AI Assistant
Ngày tạo: 2024-03-23
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
import warnings
warnings.filterwarnings('ignore')

# Thiết lập style cho đồ thị
plt.style.use('seaborn')
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 12

class TwoStagePredictor:
    def __init__(self, n_estimators=100, max_depth=10):
        self.rf_model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=42
        )
        self.lr_model = LogisticRegression(
            multi_class='multinomial',
            random_state=42
        )
        self.scaler = StandardScaler()
        
    def fit(self, X, y):
        self.rf_model.fit(X, y)
        rf_probs = self.rf_model.predict_proba(X)
        rf_probs_scaled = self.scaler.fit_transform(rf_probs)
        self.lr_model.fit(rf_probs_scaled, y)
        
    def predict_proba(self, X):
        rf_probs = self.rf_model.predict_proba(X)
        rf_probs_scaled = self.scaler.transform(rf_probs)
        return self.lr_model.predict_proba(rf_probs_scaled)
    
    def predict(self, X):
        probas = self.predict_proba(X)
        return np.argmax(probas, axis=1)

def load_and_prepare_data():
    """Load và chuẩn bị dữ liệu"""
    # Đọc dữ liệu từ các file
    pricing_df = pd.read_csv('data/stock-market-behavior-analysis/raw/market_data/pricing.csv')
    trading_value_df = pd.read_csv('data/stock-market-behavior-analysis/raw/market_data/trading_value.csv')
    market_return_df = pd.read_csv('data/stock-market-behavior-analysis/raw/market_data/market_return.csv')
    
    # Kết hợp dữ liệu
    df = pd.merge(pricing_df, trading_value_df, on=['Date', 'Symbol'], how='inner')
    df = pd.merge(df, market_return_df, on=['Date', 'Symbol'], how='inner')
    
    # Chuyển đổi cột Date sang định dạng datetime
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Sắp xếp dữ liệu theo thời gian
    df = df.sort_values('Date')
    
    # Tính toán các đặc trưng kỹ thuật
    df['Returns'] = df['Close'].pct_change()
    df['SMA_20'] = df['Close'].rolling(window=20).mean()
    df['SMA_50'] = df['Close'].rolling(window=50).mean()
    df['RSI'] = calculate_rsi(df['Close'])
    df['MACD'] = calculate_macd(df['Close'])
    
    # Xác định xu hướng (target)
    df['Trend'] = np.where(df['Returns'] > 0.01, 2,  # Tăng
                          np.where(df['Returns'] < -0.01, 0, 1))  # Giảm, Đi ngang
    
    # Chuẩn bị features
    features = ['SMA_20', 'SMA_50', 'RSI', 'MACD', 'Volume']
    X = df[features].dropna()
    y = df['Trend'].loc[X.index]
    
    return X, y, df

def calculate_rsi(prices, periods=14):
    """Tính RSI"""
    returns = prices.diff()
    up = returns.clip(lower=0)
    down = -1 * returns.clip(upper=0)
    ma_up = up.rolling(window=periods).mean()
    ma_down = down.rolling(window=periods).mean()
    rsi = ma_up / (ma_up + ma_down) * 100
    return rsi

def calculate_macd(prices, slow=26, fast=12):
    """Tính MACD"""
    exp1 = prices.ewm(span=fast, adjust=False).mean()
    exp2 = prices.ewm(span=slow, adjust=False).mean()
    macd = exp1 - exp2
    return macd

def plot_results(model, X_test, y_test, df):
    """Vẽ đồ thị kết quả"""
    # Tạo thư mục để lưu đồ thị
    import os
    os.makedirs('tieu-luan/figures', exist_ok=True)
    
    # 1. Confusion Matrix
    plt.figure(figsize=(10, 8))
    y_pred = model.predict(X_test)
    cm = confusion_matrix(y_test, y_pred)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title('Ma trận nhầm lẫn')
    plt.xlabel('Dự đoán')
    plt.ylabel('Thực tế')
    plt.savefig('tieu-luan/figures/confusion_matrix.png')
    plt.close()
    
    # 2. Feature Importance
    plt.figure(figsize=(12, 6))
    importances = model.rf_model.feature_importances_
    feature_names = X_test.columns
    indices = np.argsort(importances)[::-1]
    plt.title('Tầm quan trọng của các đặc trưng')
    plt.bar(range(X_test.shape[1]), importances[indices])
    plt.xticks(range(X_test.shape[1]), [feature_names[i] for i in indices], rotation=45)
    plt.tight_layout()
    plt.savefig('tieu-luan/figures/feature_importance.png')
    plt.close()
    
    # 3. Phân phối xu hướng
    plt.figure(figsize=(10, 6))
    trend_counts = pd.Series(y_test).value_counts().sort_index()
    trend_names = ['Giảm', 'Đi ngang', 'Tăng']
    plt.bar(trend_names, trend_counts)
    plt.title('Phân phối xu hướng thị trường')
    plt.ylabel('Số lượng mẫu')
    plt.savefig('tieu-luan/figures/trend_distribution.png')
    plt.close()
    
    # 4. ROC Curve
    from sklearn.metrics import roc_curve, auc
    plt.figure(figsize=(10, 8))
    probas = model.predict_proba(X_test)
    for i, trend in enumerate(trend_names):
        fpr, tpr, _ = roc_curve(y_test == i, probas[:, i])
        roc_auc = auc(fpr, tpr)
        plt.plot(fpr, tpr, label=f'{trend} (AUC = {roc_auc:.2f})')
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curve cho từng xu hướng')
    plt.legend(loc="lower right")
    plt.savefig('tieu-luan/figures/roc_curves.png')
    plt.close()

def main():
    # Load và chuẩn bị dữ liệu
    X, y, df = load_and_prepare_data()
    
    # Chia dữ liệu
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, shuffle=False  # Không shuffle vì là dữ liệu chuỗi thời gian
    )
    
    # Huấn luyện mô hình
    model = TwoStagePredictor()
    model.fit(X_train, y_train)
    
    # Đánh giá mô hình
    y_pred = model.predict(X_test)
    print("\nKết quả đánh giá mô hình:")
    print(classification_report(y_test, y_pred, 
                             target_names=['Giảm', 'Đi ngang', 'Tăng']))
    
    # Vẽ đồ thị kết quả
    plot_results(model, X_test, y_test, df)
    
    print("\nĐã lưu các đồ thị vào thư mục tieu-luan/figures/")

if __name__ == "__main__":
    main() 