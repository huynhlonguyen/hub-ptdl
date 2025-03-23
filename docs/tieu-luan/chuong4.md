# Chương 4: Xây Dựng Mô Hình Học Máy Để Dự Đoán Xu Hướng Chứng Khoán

## 4.1. Thiết Kế Mô Hình

### 4.1.1. Phạm Vi và Dữ Liệu Nghiên Cứu
Nghiên cứu này tập trung vào việc phân tích và dự đoán xu hướng của các mã chứng khoán thuộc rổ VN30 trên sàn HOSE (Sở Giao dịch Chứng khoán TP.HCM) trong giai đoạn từ tháng 1/2021 đến tháng 3/2024. Các mã chứng khoán được phân tích bao gồm các cổ phiếu blue-chip như VCB (Vietcombank), TCB (Techcombank), MBB (MBBank), HPG (Hòa Phát), VNM (Vinamilk), và các mã khác trong VN30. Việc lựa chọn các mã này dựa trên tính thanh khoản cao và vai trò dẫn dắt thị trường của chúng.

### 4.1.2. Kiến Trúc Mô Hình
Để nâng cao độ chính xác trong dự đoán, chúng tôi đề xuất một mô hình học máy hai tầng. Tầng thứ nhất sử dụng Random Forest Classifier để phân tích các chỉ báo kỹ thuật, trong khi tầng thứ hai áp dụng Logistic Regression để tổng hợp và đưa ra dự đoán cuối cùng. Kiến trúc này cho phép mô hình vừa nắm bắt được các mối quan hệ phi tuyến trong dữ liệu thông qua Random Forest, vừa duy trì khả năng diễn giải kết quả thông qua Logistic Regression.

Cụ thể, mô hình được cài đặt như sau:

```python
class TwoLayerModel:
    def __init__(self, n_estimators=200, max_depth=10, 
                 min_samples_split=2, min_samples_leaf=1):
        """Khởi tạo mô hình hai tầng
        
        Tham số:
            n_estimators (int): Số lượng cây quyết định
            max_depth (int): Độ sâu tối đa của mỗi cây
            min_samples_split (int): Số mẫu tối thiểu để phân tách nút
            min_samples_leaf (int): Số mẫu tối thiểu tại mỗi nút lá
        """
        self.rf = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            min_samples_split=min_samples_split,
            min_samples_leaf=min_samples_leaf,
            random_state=42
        )
        self.lr = LogisticRegression(random_state=42)
        self.scaler = StandardScaler()
```

### 4.1.3. Đặc Trưng Đầu Vào
Mô hình sử dụng một tập hợp đa dạng các đặc trưng được tính toán từ dữ liệu giao dịch hàng ngày. Các chỉ báo kỹ thuật cơ bản bao gồm Moving Average (MA) với hai khung thời gian 20 và 50 ngày, giúp xác định xu hướng trung và dài hạn. Chỉ số RSI (Relative Strength Index) được sử dụng để đánh giá tình trạng quá mua hoặc quá bán, trong khi MACD (Moving Average Convergence Divergence) và đường Signal giúp xác định điểm đảo chiều tiềm năng. Bên cạnh đó, Bollinger Bands được áp dụng để đánh giá độ biến động và xác định các mức hỗ trợ/kháng cự động.

Ngoài các chỉ báo kỹ thuật, mô hình còn sử dụng dữ liệu về giá (đóng cửa, cao nhất, thấp nhất) và khối lượng giao dịch. Từ các dữ liệu gốc này, chúng tôi tính toán thêm các đặc trưng phái sinh như tỷ lệ thay đổi giá, độ biến động, và momentum để nắm bắt được động lực của thị trường.

Việc tính toán các đặc trưng được thực hiện như sau:

```python
def prepare_features(df):
    """Chuẩn bị các đặc trưng cho mô hình
    
    Tham số:
        df: DataFrame chứa dữ liệu gốc
    Trả về:
        DataFrame: Các đặc trưng đã tính toán
    """
    features = pd.DataFrame(index=df.index)
    
    # Tính các chỉ báo kỹ thuật
    for symbol in df.columns:
        if f'{symbol}_close' in df.columns:
            close = df[f'{symbol}_close']
            high = df[f'{symbol}_high']
            low = df[f'{symbol}_low']
            volume = df[f'{symbol}_volume']
            
            # Moving Averages
            features[f'{symbol}_MA20'] = close.rolling(window=20).mean()
            features[f'{symbol}_MA50'] = close.rolling(window=50).mean()
            
            # RSI
            features[f'{symbol}_RSI'] = calculate_rsi(close)
            
            # MACD
            macd, signal = calculate_macd(close)
            features[f'{symbol}_MACD'] = macd
            features[f'{symbol}_MACD_Signal'] = signal
            
            # Bollinger Bands
            bb_upper, bb_lower = calculate_bollinger_bands(close)
            features[f'{symbol}_BB_Upper'] = bb_upper
            features[f'{symbol}_BB_Lower'] = bb_lower
            
            # Momentum
            features[f'{symbol}_ROC_5'] = calculate_roc(close, 5)
            features[f'{symbol}_ROC_10'] = calculate_roc(close, 10)
            
            # Volatility
            features[f'{symbol}_ATR'] = calculate_atr(high, low, close)
            features[f'{symbol}_Volatility'] = calculate_volatility(close)
    
    return features.dropna()
```

## 4.2. Huấn Luyện và Tối Ưu Hóa

### 4.2.1. Quy Trình Xử Lý Dữ liệu
Dữ liệu giao dịch được thu thập từ Yahoo Finance thông qua thư viện yfinance, một API đáng tin cậy cung cấp dữ liệu lịch sử của thị trường chứng khoán Việt Nam. Quá trình chuẩn bị dữ liệu được thực hiện thông qua một pipeline tự động, bao gồm việc tính toán các chỉ báo kỹ thuật và chuẩn hóa các đặc trưng. Dữ liệu sau đó được chia thành ba tập: 70% cho huấn luyện, 15% cho validation, và 15% cho kiểm thử, đảm bảo tính liên tục về mặt thời gian.

Quy trình xử lý dữ liệu được cài đặt như sau:

```python
def prepare_data(df, features_index, threshold=0.01):
    """Chuẩn bị dữ liệu cho mô hình
    
    Tham số:
        df: DataFrame chứa dữ liệu gốc
        features_index: Index của các đặc trưng
        threshold: Ngưỡng phân loại xu hướng
    """
    # Tính toán các chỉ báo kỹ thuật
    features = calculate_technical_indicators(df)
    
    # Tạo nhãn dựa trên biến động giá
    labels = pd.DataFrame(index=df.index)
    
    for symbol in df.columns:
        if f'{symbol}_close' in df.columns:
            pct_change = df[f'{symbol}_close'].pct_change()
            labels[symbol] = 0  # Đi ngang
            labels.loc[pct_change > threshold, symbol] = 1  # Tăng
            labels.loc[pct_change < -threshold, symbol] = -1  # Giảm
    
    return features, labels
```

### 4.2.2. Quá Trình Huấn Luyện
Việc huấn luyện mô hình được thực hiện theo hai giai đoạn. Đầu tiên, Random Forest Classifier được huấn luyện với các tham số ban đầu gồm 100 cây quyết định, độ sâu tối đa 10 nút, và điều kiện tách nút tối thiểu 5 mẫu. Tiếp theo, Logistic Regression được huấn luyện với hệ số điều chỉnh C=1.0 và số vòng lặp tối đa 1000.

Quá trình huấn luyện được thực hiện thông qua phương thức fit:

```python
def fit(self, X, y):
    """Huấn luyện mô hình hai tầng
    
    Tham số:
        X: Ma trận đặc trưng đầu vào
        y: Nhãn (-1: giảm, 0: đi ngang, 1: tăng)
    """
    # Huấn luyện Rừng Ngẫu Nhiên
    self.rf.fit(X, y)
    
    # Lấy xác suất dự báo từ Rừng Ngẫu Nhiên
    rf_probs = self.rf.predict_proba(X)
    
    # Chuẩn hóa xác suất
    self.scaler.fit(rf_probs)
    scaled_probs = self.scaler.transform(rf_probs)
    
    # Huấn luyện Hồi Quy Logistic
    self.lr.fit(scaled_probs, y)
```

### 4.2.3. Tối Ưu Hóa Mô Hình
Để tìm ra cấu hình tối ưu, chúng tôi thực hiện grid search trên một không gian tham số đa chiều. Đối với Random Forest, các giá trị được thử nghiệm bao gồm số lượng cây (50, 100, 200), độ sâu tối đa (5, 10, 15), và số mẫu tối thiểu để tách nút (2, 5, 10). Với Logistic Regression, chúng tôi thử nghiệm các giá trị C (0.1, 1.0, 10.0) và số vòng lặp tối đa (500, 1000).

Quá trình tối ưu hóa được thực hiện thông qua grid search:

```python
def find_best_params(X_train, y_train):
    """Tìm siêu tham số tối ưu cho Rừng Ngẫu Nhiên
    
    Tham số:
        X_train: Tập huấn luyện đặc trưng
        y_train: Tập huấn luyện nhãn
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
    return grid_search.best_params_
```

## 4.3. Kết Quả và Thảo Luận

### 4.3.1. Hiệu Suất Tổng Thể
Sau quá trình huấn luyện và tối ưu hóa, mô hình đạt được độ chính xác 44.44% trên tập kiểm thử, với độ chính xác dương tính (precision) 47.04%, độ nhạy (recall) 44.44%, và điểm F1 37.94%. Mặc dù các chỉ số này chưa thực sự cao, nhưng đã vượt trội so với dự đoán ngẫu nhiên và các phương pháp đơn giản khác.

Đánh giá hiệu suất được thực hiện như sau:

```python
def evaluate_model(y_true, y_pred):
    """Đánh giá hiệu suất mô hình
    
    Tham số:
        y_true: Nhãn thực tế
        y_pred: Nhãn dự báo
    """
    print("\nBáo cáo phân loại chi tiết:")
    print(classification_report(y_true, y_pred))
    
    # Vẽ ma trận nhầm lẫn
    plt.figure(figsize=(8, 6))
    cm = confusion_matrix(y_true, y_pred)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title('Ma trận nhầm lẫn')
    plt.xlabel('Dự báo')
    plt.ylabel('Thực tế')
    plt.savefig('output/confusion_matrix.png')
    plt.close()
```

### 4.3.2. Phân Tích Đặc Trưng
Phân tích tầm quan trọng của các đặc trưng cho thấy RSI đóng góp nhiều nhất (25%) vào quyết định của mô hình, tiếp theo là MACD (20%) và MA50 (18%). Điều này phản ánh tầm quan trọng của các chỉ báo động lượng và xu hướng trong việc dự đoán biến động giá cổ phiếu.

Phân tích đặc trưng được thực hiện thông qua:

```python
def analyze_feature_importance(model, feature_names):
    """Phân tích và vẽ biểu đồ mức độ ảnh hưởng của các chỉ báo
    
    Tham số:
        model: Mô hình đã huấn luyện
        feature_names: Danh sách tên các chỉ báo
    """
    # Lấy mức độ ảnh hưởng của các chỉ báo
    importance_dict = model.get_feature_importance(feature_names)
    
    # Vẽ biểu đồ
    plt.figure(figsize=(12, 6))
    plt.bar(importance_dict.keys(), importance_dict.values())
    plt.xticks(rotation=45, ha='right')
    plt.title('Mức độ ảnh hưởng của các chỉ báo')
    plt.tight_layout()
    plt.savefig('output/feature_importance.png')
    plt.close()
```

### 4.3.3. Ưu Điểm và Hạn Chế
Kiến trúc hai tầng đã thể hiện một số ưu điểm đáng kể như khả năng giảm thiểu overfitting và tăng khả năng tổng quát hóa. Tuy nhiên, mô hình vẫn còn những hạn chế như độ chính xác chưa cao và thời gian huấn luyện tương đối lâu do cấu trúc phức tạp của Random Forest. Những hạn chế này có thể được cải thiện trong tương lai thông qua việc bổ sung thêm các đặc trưng về sentiment thị trường và tối ưu hóa quy trình huấn luyện.

Phân tích lỗi chi tiết được thực hiện thông qua:

```python
def analyze_errors(model, X_test, y_test):
    """Phân tích chi tiết các trường hợp dự báo sai
    
    Tham số:
        model: Mô hình đã huấn luyện
        X_test: Tập kiểm tra đặc trưng
        y_test: Tập kiểm tra nhãn
    """
    # Dự báo trên tập kiểm tra
    y_pred = model.predict(X_test)
    
    # Tìm các trường hợp dự báo sai
    errors = X_test[y_pred != y_test]
    error_true = y_test[y_pred != y_test]
    error_pred = y_pred[y_pred != y_test]
    
    print("\nPhân tích lỗi dự báo:")
    for i, (true, pred) in enumerate(zip(error_true, error_pred)):
        print(f"Mẫu {i+1}:")
        print(f"  Thực tế: {true}")
        print(f"  Dự báo: {pred}")
        print(f"  Đặc trưng: {errors.iloc[i].to_dict()}")
```
