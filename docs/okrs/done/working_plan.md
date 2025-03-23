# Kế hoạch phân tích dữ liệu thị trường chứng khoán

## Đang thực hiện
1. **Hoàn thiện mô hình**
   - [ ] Tối ưu hóa hyperparameters cho Random Forest và Logistic Regression
   - [ ] Cải thiện độ chính xác (hiện tại: 44.44%)
   - [ ] Thử nghiệm thêm features mới

## Đã hoàn thành
1. **Khám phá và tiền xử lý dữ liệu**
   - [x] Tạo notebook cho việc phân tích
   - [x] Tạo module tiện ích data_utils.py
   - [x] Thiết lập cấu trúc phân tích dữ liệu
   - [x] Tạo script phân tích dữ liệu
   - [x] Tổ chức output vào thư mục thống nhất

2. **Phân tích thống kê**
   - [x] Chạy script phân tích
   - [x] Đánh giá kết quả phân tích
   - [x] Điều chỉnh các tham số
   - [x] Tạo các biểu đồ phân tích kỹ thuật

3. **Phân tích sentiment thị trường**
   - [x] Tính toán Market Turnover
   - [x] Tính toán Advance-Decline Ratio (ADR trung bình: 1.71)
   - [x] Tính toán Share Turnover
   - [x] Vẽ biểu đồ xu hướng các chỉ số
   - [x] Lưu kết quả vào output/sentiment/

4. **Xây dựng đặc trưng nâng cao**
   - [x] Tạo thêm các chỉ báo kỹ thuật
   - [x] Tính toán các đặc trưng thống kê
   - [x] Chuẩn hóa dữ liệu
   - [x] Feature importance analysis

5. **Huấn luyện mô hình ban đầu**
   - [x] Xây dựng mô hình hai tầng (Random Forest + Logistic Regression)
   - [x] Đánh giá mô hình (Accuracy: 44.44%, Precision: 47.04%)
   - [x] Lưu kết quả vào output/models/

## Kế hoạch tiếp theo
1. **Cải thiện mô hình**
   - [ ] Thêm features từ phân tích sentiment
   - [ ] Thử nghiệm các thuật toán ensemble khác
   - [ ] Cross-validation với nhiều khoảng thời gian
   - [ ] Tối ưu hóa hyperparameters

## Ghi chú kỹ thuật
### Cấu trúc output
1. **output/**
   - models/: Kết quả huấn luyện mô hình
   - sentiment/: Phân tích sentiment thị trường
   - Các file phân tích kỹ thuật và thống kê

### Kết quả phân tích mới
1. **Sentiment Analysis**:
   - ADR trung bình: 1.71
   - Market Turnover và Share Turnover có xu hướng tăng
   - Độ biến động ADR cao (std = 2.18)

2. **Model Performance**:
   - Accuracy: 44.44%
   - Precision: 47.04%
   - Recall: 44.44%
   - F1-score: 37.94%

3. **Đề xuất cải thiện**:
   - Thêm features từ sentiment analysis
   - Tăng kích thước tập dữ liệu huấn luyện
   - Điều chỉnh hyperparameters
   - Thử nghiệm các thuật toán ensemble khác

### Cấu trúc dữ liệu
1. **pricing.csv**: 
   - Dữ liệu giá theo thời gian
   - Kích thước: 180 x 417 cột
   - Các cột: Date và mã cổ phiếu
   - Dữ liệu thiếu: Một số mã có tỷ lệ thiếu cao (>90%)
   
2. **trading_value.csv**:
   - Dữ liệu giá trị giao dịch
   - Kích thước: 180 x 417 cột
   - Các cột: Date và mã cổ phiếu
   - Nhiều outliers trong giá trị giao dịch

3. **market_return.csv**:
   - Dữ liệu lợi nhuận thị trường
   - Kích thước: 270 x 2 cột
   - Các cột: month, market_return
   - Không có dữ liệu thiếu
   - 27 outliers trong tỷ suất sinh lời

### Luồng xử lý dữ liệu
1. Đọc và kiểm tra chất lượng dữ liệu
   - Phân tích cấu trúc
   - Kiểm tra dữ liệu thiếu
   - Phát hiện giá trị ngoại lai
2. Xử lý dữ liệu thiếu và ngoại lai
   - Điền giá trị thiếu
   - Xử lý ngoại lai
3. Tính toán đặc trưng kỹ thuật
   - SMA, EMA
   - RSI, MACD
   - Bollinger Bands
4. Chuẩn hóa dữ liệu
5. Chia tập train/test
6. Huấn luyện và đánh giá mô hình

### Đặc trưng đã tạo
1. **Chỉ báo xu hướng**:
   - SMA (20, 50 ngày)
   - EMA (12, 26 ngày)
   - MACD và Signal

2. **Chỉ báo biến động**:
   - RSI (14 ngày)
   - Bollinger Bands (20 ngày)

3. **Chỉ báo sentiment**:
   - Market Turnover: Tỷ lệ giá trị giao dịch/vốn hóa
   - Advance-Decline Ratio: Tỷ lệ số mã tăng/giảm
   - Share Turnover: Tỷ lệ giao dịch trên vốn hóa

### Kết quả phân tích
1. **Phân tích chất lượng dữ liệu**:
   - Dữ liệu giá:
     + Một số mã có tỷ lệ thiếu cao (>90%)
     + Nhiều mã có outliers (>20 outliers)
     + Phân phối giá không chuẩn
   - Dữ liệu giao dịch:
     + Tương tự dữ liệu giá về tỷ lệ thiếu
     + Nhiều outliers trong giá trị giao dịch
   - Dữ liệu tỷ suất sinh lời:
     + Không có dữ liệu thiếu
     + 27 outliers trong tỷ suất sinh lời

2. **Phân tích kỹ thuật**:
   - Đã tính toán các chỉ báo cho VNM, VIC, VCB
   - Vẽ biểu đồ phân tích kỹ thuật
   - Lưu kết quả vào thư mục output/

3. **Đề xuất xử lý**:
   - Loại bỏ các mã có tỷ lệ thiếu >50%
   - Xử lý outliers bằng phương pháp winsorization
   - Điền giá trị thiếu bằng phương pháp nội suy
   - Chuẩn hóa dữ liệu trước khi xây dựng mô hình 

4. **Phân tích sentiment**:
   - ADR trung bình 1.71, cho thấy xu hướng tăng
   - Market Turnover và Share Turnover tăng dần
   - Độ biến động ADR cao (std = 2.18)
   - Đã tạo biểu đồ xu hướng trong output/sentiment/ 