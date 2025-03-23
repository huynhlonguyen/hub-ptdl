"""
File: model_training.py
Mục đích: Huấn luyện mô hình dự đoán xu hướng thị trường chứng khoán
Tác giả: Huỳnh Long Uyển (Học viên Cao học HUB)

"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
import warnings
warnings.filterwarnings('ignore')

# Thiết lập style cho đồ thị
plt.style.use('default')  # Sử dụng style mặc định của matplotlib
sns.set_theme(style='whitegrid')  # Sử dụng theme của seaborn

# Cấu hình matplotlib
plt.rcParams.update({
    'figure.figsize': (12, 8),
    'font.size': 12,
    'axes.grid': True,
    'grid.alpha': 0.3
})

class TwoLayerModel:
    def __init__(self, n_estimators=100, max_depth=10, min_samples_split=2, min_samples_leaf=1):
        self.rf = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            min_samples_split=min_samples_split,
            min_samples_leaf=min_samples_leaf,
            random_state=42
        )
        self.lr = LogisticRegression(random_state=42)
        self.scaler = StandardScaler()
        
        # Tạo thư mục output
        self.output_dir = Path('output/models')
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def fit(self, X, y):
        """
        Huấn luyện mô hình hai lớp cho một cổ phiếu
        X: features
        y: nhãn (-1: giảm, 0: đi ngang, 1: tăng)
        """
        # Huấn luyện Random Forest
        self.rf.fit(X, y)
        
        # Lấy xác suất dự đoán từ Random Forest
        rf_probs = self.rf.predict_proba(X)
        
        # Chuẩn hóa xác suất
        self.scaler.fit(rf_probs)
        scaled_probs = self.scaler.transform(rf_probs)
        
        # Huấn luyện Logistic Regression với xác suất đã chuẩn hóa
        self.lr.fit(scaled_probs, y)
        
        # Lưu feature importance
        self._save_feature_importance(X.columns)
        
    def predict(self, X):
        """
        Dự đoán nhãn cho dữ liệu mới
        """
        # Lấy xác suất từ Random Forest
        rf_probs = self.rf.predict_proba(X)
        
        # Chuẩn hóa xác suất
        scaled_probs = self.scaler.transform(rf_probs)
        
        # Dự đoán với Logistic Regression
        return self.lr.predict(scaled_probs)
    
    def predict_proba(self, X):
        """
        Dự đoán xác suất cho dữ liệu mới
        """
        # Lấy xác suất từ Random Forest
        rf_probs = self.rf.predict_proba(X)
        
        # Chuẩn hóa xác suất
        scaled_probs = self.scaler.transform(rf_probs)
        
        # Lấy xác suất từ Logistic Regression
        return self.lr.predict_proba(scaled_probs)
    
    def _save_feature_importance(self, feature_names):
        """
        Lưu và vẽ biểu đồ feature importance
        """
        # Lấy feature importance từ Random Forest
        importance = self.rf.feature_importances_
        
        # Tạo DataFrame
        feat_imp = pd.DataFrame({
            'feature': feature_names,
            'importance': importance
        })
        feat_imp = feat_imp.sort_values('importance', ascending=False)
        
        # Lưu vào file
        feat_imp.to_csv(self.output_dir / 'feature_importance.csv', index=False)
        
        # Vẽ biểu đồ
        plt.figure(figsize=(12, 6))
        sns.barplot(data=feat_imp.head(10), x='importance', y='feature')
        plt.title('Top 10 Feature Importance')
        plt.tight_layout()
        plt.savefig(self.output_dir / 'feature_importance.png', dpi=300, bbox_inches='tight')
        plt.close()

    def get_feature_importance(self, feature_names=None):
        """
        Lấy độ quan trọng của các features từ Random Forest
        """
        importances = self.rf.feature_importances_
        if feature_names is None:
            return importances
        
        # Tạo dictionary feature_name: importance
        importance_dict = dict(zip(feature_names, importances))
        
        # Sắp xếp theo độ quan trọng giảm dần
        return dict(sorted(importance_dict.items(), key=lambda x: x[1], reverse=True))

def prepare_data():
    """
    Chuẩn bị dữ liệu cho mô hình
    """
    # Đọc dữ liệu
    data_dir = Path('data/stock-market-behavior-analysis/raw/market_data')
    pricing = pd.read_csv(data_dir / 'pricing.csv', parse_dates=['date'], index_col='date')
    trading_value = pd.read_csv(data_dir / 'trading_value.csv', parse_dates=['date'], index_col='date')
    market_indicators = pd.read_csv(Path('output/sentiment/market_indicators.csv'), parse_dates=['date'], index_col='date')
    
    # Tính các đặc trưng
    features = pd.DataFrame(index=pricing.index)
    
    # Thêm chỉ số thị trường
    features = pd.concat([features, market_indicators], axis=1)
    
    # Tính returns
    returns = pricing.pct_change()
    features['mean_return'] = returns.mean(axis=1)
    features['std_return'] = returns.std(axis=1)
    
    # Tính volume features
    features['total_value'] = trading_value.sum(axis=1)
    features['value_change'] = features['total_value'].pct_change()
    
    # Tạo nhãn (1: tăng, 0: giảm)
    features['target'] = (features['mean_return'].shift(-1) > 0).astype(int)
    
    # Xóa các dòng có giá trị NaN
    features = features.dropna()
    
    return features

def evaluate_model(model, X_test, y_test):
    """
    Đánh giá mô hình và lưu kết quả
    """
    # Dự đoán
    y_pred = model.predict(X_test)
    
    # Tính các metrics
    report = classification_report(y_test, y_pred, output_dict=True)
    conf_matrix = confusion_matrix(y_test, y_pred)
    
    # Lưu kết quả
    output_dir = Path('output/models')
    
    # Lưu classification report
    pd.DataFrame(report).transpose().to_csv(output_dir / 'classification_report.csv')
    
    # Vẽ confusion matrix
    plt.figure(figsize=(8, 6))
    sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues')
    plt.title('Confusion Matrix')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    plt.savefig(output_dir / 'confusion_matrix.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # In kết quả
    print("\nKết quả đánh giá mô hình:")
    print("-" * 40)
    print(f"Accuracy: {report['accuracy']:.4f}")
    print(f"Precision: {report['weighted avg']['precision']:.4f}")
    print(f"Recall: {report['weighted avg']['recall']:.4f}")
    print(f"F1-score: {report['weighted avg']['f1-score']:.4f}")

def main():
    """
    Hàm chính để huấn luyện và đánh giá mô hình
    """
    print("Bắt đầu huấn luyện mô hình...")
    
    # Chuẩn bị dữ liệu
    print("\n1. Chuẩn bị dữ liệu")
    print("-" * 40)
    data = prepare_data()
    print(f"Shape của dữ liệu: {data.shape}")
    print("\nCác cột trong dữ liệu:")
    print(data.columns.tolist())
    print("\nThống kê mô tả:")
    print(data.describe())
    
    # Chia features và target
    print("\n2. Chia features và target")
    print("-" * 40)
    X = data.drop(['target'], axis=1)
    y = data['target']
    print(f"Shape của features (X): {X.shape}")
    print(f"Shape của target (y): {y.shape}")
    print(f"\nPhân phối nhãn:\n{y.value_counts(normalize=True)}")
    
    # Chia train/test
    print("\n3. Chia tập train/test")
    print("-" * 40)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, shuffle=False
    )
    print(f"Shape của X_train: {X_train.shape}")
    print(f"Shape của X_test: {X_test.shape}")
    
    # Khởi tạo và huấn luyện mô hình
    print("\n4. Huấn luyện mô hình")
    print("-" * 40)
    model = TwoLayerModel()
    print("Bắt đầu huấn luyện Random Forest...")
    model.fit(X_train, y_train)
    print("Đã hoàn thành huấn luyện Random Forest")
    
    # Đánh giá mô hình
    print("\n5. Đánh giá mô hình")
    print("-" * 40)
    evaluate_model(model, X_test, y_test)
    
    print("\nĐã hoàn thành huấn luyện và đánh giá mô hình!")
    print(f"Kết quả đã được lưu trong thư mục: {Path('output/models')}")

if __name__ == "__main__":
    main() 