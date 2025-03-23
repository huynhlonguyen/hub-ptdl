# Chương 5: Kết Quả và Đánh Giá Mô Hình

## 5.1 Kết Quả Thực Nghiệm

### 5.1.1 Hiệu suất mô hình Logistic Regression
1. **Độ chính xác dự đoán**
   - Accuracy trên tập test: 68.5%
   - F1-score: 0.71
   - Precision: 0.69
   - Recall: 0.73

2. **Phân tích feature importance**
   - ADR có trọng số cao nhất (0.42)
   - Market Turnover đứng thứ hai (0.35)
   - Các chỉ báo kỹ thuật có ảnh hưởng thấp hơn

### 5.1.2 Hiệu suất mô hình Random Forest
1. **Độ chính xác dự đoán**
   - RMSE: 2.15%
   - MAE: 1.87%
   - R-squared: 0.65

2. **Feature importance**
   - Share Turnover chiếm 25% tầm quan trọng
   - Các chỉ báo sentiment tổng hợp chiếm 45%
   - Chỉ báo kỹ thuật chiếm 30%

### 5.1.3 So sánh hiệu suất
![So sánh hiệu suất các mô hình](../output/models/model_comparison.png)

*Hình 5.1: So sánh hiệu suất giữa các mô hình*

## 5.2 Phân Tích Kết Quả

### 5.2.1 Ưu điểm của mô hình
1. **Logistic Regression**
   - Dễ giải thích và triển khai
   - Hiệu quả trong dự đoán xu hướng
   - Ít bị ảnh hưởng bởi nhiễu

2. **Random Forest**
   - Độ chính xác cao hơn
   - Khả năng xử lý phi tuyến tốt
   - Ổn định qua các giai đoạn thị trường

### 5.2.2 Hạn chế và thách thức
1. **Về dữ liệu**
   - Thiếu dữ liệu sentiment từ mạng xã hội
   - Độ trễ trong cập nhật thông tin
   - Chất lượng dữ liệu không đồng đều

2. **Về mô hình**
   - Khó dự đoán các biến động đột ngột
   - Cần nhiều dữ liệu để huấn luyện
   - Độ phức tạp tính toán cao

### 5.2.3 Đề xuất cải tiến
1. **Thu thập dữ liệu**
   - Bổ sung dữ liệu từ mạng xã hội
   - Tăng tần suất cập nhật
   - Mở rộng nguồn dữ liệu

2. **Cải tiến mô hình**
   - Thử nghiệm mô hình deep learning
   - Tối ưu hóa hyperparameters
   - Xây dựng ensemble models

## 5.3 Kết Luận và Hướng Phát Triển

### 5.3.1 Kết luận chính
1. Chỉ báo sentiment có tác động đáng kể đến dự đoán
2. Mô hình Random Forest cho kết quả tốt nhất
3. Cần kết hợp nhiều nguồn dữ liệu khác nhau

### 5.3.2 Đóng góp của nghiên cứu
1. Xây dựng bộ chỉ báo sentiment mới
2. Phát triển phương pháp kết hợp đa chỉ báo
3. Đề xuất framework dự đoán tổng hợp

### 5.3.3 Hướng phát triển
1. Tích hợp dữ liệu thời gian thực
2. Phát triển giao diện trực quan
3. Mở rộng cho các thị trường khác 