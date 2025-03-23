# Chương 4: Xây dựng Mô hình Phân tích Sentiment và Dự Đoán Xu Hướng

## 4.1 Phân tích Sentiment Thị Trường

### 4.1.1 Các chỉ báo sentiment
Trong nghiên cứu này, chúng tôi sử dụng 3 chỉ báo chính để đo lường sentiment thị trường:

1. **Market Turnover (MT)**
   - Định nghĩa: Tỷ lệ giữa giá trị giao dịch và tổng vốn hóa thị trường
   - Ý nghĩa: Phản ánh mức độ tích cực của nhà đầu tư thông qua thanh khoản
   - Công thức: MT = Trading Value / Total Market Cap

2. **Advance-Decline Ratio (ADR)**
   - Định nghĩa: Tỷ lệ giữa số mã tăng giá và số mã giảm giá
   - Ý nghĩa: Đo lường sức mạnh tổng thể của thị trường
   - Công thức: ADR = Number of Advancing Stocks / Number of Declining Stocks

3. **Share Turnover**
   - Định nghĩa: Tỷ lệ giao dịch trên vốn hóa cho từng cổ phiếu
   - Ý nghĩa: Đánh giá mức độ quan tâm của nhà đầu tư với từng mã
   - Công thức: ST = Trading Value / Market Cap

### 4.1.2 Kết quả phân tích
Từ dữ liệu thị trường giai đoạn 2020-2022, chúng tôi thu được các kết quả sau:

1. **Xu hướng thị trường**
   - ADR trung bình đạt 1.71, phản ánh xu hướng tăng điểm
   - Độ lệch chuẩn ADR là 2.18, cho thấy biến động mạnh
   - Các giai đoạn ADR > 2 thường đi kèm với thị trường tăng điểm mạnh

2. **Thanh khoản thị trường**
   - Market Turnover và Share Turnover có xu hướng tăng dần
   - Giá trị giao dịch dao động từ 13.2 tỷ đến 53.3 tỷ đồng/ngày
   - Thanh khoản tập trung vào nhóm cổ phiếu vốn hóa lớn

### 4.1.3 Biểu đồ phân tích
![Xu hướng các chỉ số thị trường](../output/sentiment/market_trends.png)

*Hình 4.1: Xu hướng các chỉ số sentiment thị trường*

## 4.2 Xây dựng Mô hình Dự Đoán

### 4.2.1 Chuẩn bị dữ liệu
1. **Tiền xử lý**
   - Loại bỏ các mã có tỷ lệ dữ liệu thiếu >50%
   - Xử lý outliers bằng phương pháp winsorization
   - Chuẩn hóa dữ liệu bằng StandardScaler

2. **Tạo đặc trưng**
   - Chỉ báo kỹ thuật: SMA, EMA, RSI, MACD
   - Chỉ báo sentiment: MT, ADR, Share Turnover
   - Đặc trưng thống kê: độ lệch chuẩn, tương quan

### 4.2.2 Thiết kế mô hình
1. **Logistic Regression**
   - Input: Các chỉ báo đã chuẩn hóa
   - Output: Dự đoán xu hướng tăng/giảm
   - Tối ưu hóa: L1/L2 regularization

2. **Random Forest**
   - Input: Kết hợp đặc trưng kỹ thuật và sentiment
   - Output: Dự đoán giá trị cụ thể
   - Tối ưu hóa: số cây, độ sâu tối đa

### 4.2.3 Huấn luyện và đánh giá
1. **Phân chia dữ liệu**
   - Training set: 70% dữ liệu
   - Validation set: 15% dữ liệu
   - Test set: 15% dữ liệu

2. **Metrics đánh giá**
   - Accuracy và F1-score cho Logistic Regression
   - RMSE và MAE cho Random Forest
   - Đánh giá độ ổn định qua các giai đoạn thị trường 