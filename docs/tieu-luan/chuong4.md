# Chương 4: Xây Dựng Mô Hình Học Máy Để Dự Đoán Xu Hướng Chứng Khoán

## 4.1. Thiết Kế Mô Hình

### 4.1.1. Phạm Vi và Dữ Liệu Nghiên Cứu
Nghiên cứu này tập trung vào việc phân tích và dự đoán xu hướng của các mã chứng khoán thuộc rổ VN30 trên sàn HOSE (Sở Giao dịch Chứng khoán TP.HCM) trong giai đoạn từ tháng 1/2021 đến tháng 3/2024. Các mã chứng khoán được phân tích bao gồm các cổ phiếu blue-chip như VCB (Vietcombank), TCB (Techcombank), MBB (MBBank), HPG (Hòa Phát), VNM (Vinamilk), và các mã khác trong VN30. Việc lựa chọn các mã này dựa trên tính thanh khoản cao và vai trò dẫn dắt thị trường của chúng.

### 4.1.2. Kiến Trúc Mô Hình
Để nâng cao độ chính xác trong dự đoán, chúng tôi đề xuất một mô hình học máy hai tầng. Tầng thứ nhất sử dụng Random Forest Classifier để phân tích các chỉ báo kỹ thuật, trong khi tầng thứ hai áp dụng Logistic Regression để tổng hợp và đưa ra dự đoán cuối cùng. Kiến trúc này cho phép mô hình vừa nắm bắt được các mối quan hệ phi tuyến trong dữ liệu thông qua Random Forest, vừa duy trì khả năng diễn giải kết quả thông qua Logistic Regression.

### 4.1.3. Đặc Trưng Đầu Vào
Mô hình sử dụng một tập hợp đa dạng các đặc trưng được tính toán từ dữ liệu giao dịch hàng ngày. Các chỉ báo kỹ thuật cơ bản bao gồm Moving Average (MA) với hai khung thời gian 20 và 50 ngày, giúp xác định xu hướng trung và dài hạn. Chỉ số RSI (Relative Strength Index) được sử dụng để đánh giá tình trạng quá mua hoặc quá bán, trong khi MACD (Moving Average Convergence Divergence) và đường Signal giúp xác định điểm đảo chiều tiềm năng. Bên cạnh đó, Bollinger Bands được áp dụng để đánh giá độ biến động và xác định các mức hỗ trợ/kháng cự động.

Ngoài các chỉ báo kỹ thuật, mô hình còn sử dụng dữ liệu về giá (đóng cửa, cao nhất, thấp nhất) và khối lượng giao dịch. Từ các dữ liệu gốc này, chúng tôi tính toán thêm các đặc trưng phái sinh như tỷ lệ thay đổi giá, độ biến động, và momentum để nắm bắt được động lực của thị trường.

## 4.2. Huấn Luyện và Tối Ưu Hóa

### 4.2.1. Quy Trình Xử Lý Dữ Liệu
Dữ liệu giao dịch được thu thập từ các nguồn đáng tin cậy như TCBS và SSI Data Services, sau đó được tiền xử lý để loại bỏ nhiễu và chuẩn hóa. Quá trình chuẩn bị dữ liệu được thực hiện thông qua một pipeline tự động, bao gồm việc tính toán các chỉ báo kỹ thuật và chuẩn hóa các đặc trưng. Dữ liệu sau đó được chia thành ba tập: 70% cho huấn luyện, 15% cho validation, và 15% cho kiểm thử, đảm bảo tính liên tục về mặt thời gian.

### 4.2.2. Quá Trình Huấn Luyện
Việc huấn luyện mô hình được thực hiện theo hai giai đoạn. Đầu tiên, Random Forest Classifier được huấn luyện với các tham số ban đầu gồm 100 cây quyết định, độ sâu tối đa 10 nút, và điều kiện tách nút tối thiểu 5 mẫu. Tiếp theo, Logistic Regression được huấn luyện với hệ số điều chỉnh C=1.0 và số vòng lặp tối đa 1000.

### 4.2.3. Tối Ưu Hóa Mô Hình
Để tìm ra cấu hình tối ưu, chúng tôi thực hiện grid search trên một không gian tham số đa chiều. Đối với Random Forest, các giá trị được thử nghiệm bao gồm số lượng cây (50, 100, 200), độ sâu tối đa (5, 10, 15), và số mẫu tối thiểu để tách nút (2, 5, 10). Với Logistic Regression, chúng tôi thử nghiệm các giá trị C (0.1, 1.0, 10.0) và số vòng lặp tối đa (500, 1000).

## 4.3. Kết Quả và Thảo Luận

### 4.3.1. Hiệu Suất Tổng Thể
Sau quá trình huấn luyện và tối ưu hóa, mô hình đạt được độ chính xác 44.44% trên tập kiểm thử, với độ chính xác dương tính (precision) 47.04%, độ nhạy (recall) 44.44%, và điểm F1 37.94%. Mặc dù các chỉ số này chưa thực sự cao, nhưng đã vượt trội so với dự đoán ngẫu nhiên và các phương pháp đơn giản khác.

### 4.3.2. Phân Tích Đặc Trưng
Phân tích tầm quan trọng của các đặc trưng cho thấy RSI đóng góp nhiều nhất (25%) vào quyết định của mô hình, tiếp theo là MACD (20%) và MA50 (18%). Điều này phản ánh tầm quan trọng của các chỉ báo động lượng và xu hướng trong việc dự đoán biến động giá cổ phiếu.

### 4.3.3. Ưu Điểm và Hạn Chế
Kiến trúc hai tầng đã thể hiện một số ưu điểm đáng kể như khả năng giảm thiểu overfitting và tăng khả năng tổng quát hóa. Tuy nhiên, mô hình vẫn còn những hạn chế như độ chính xác chưa cao và thời gian huấn luyện tương đối lâu do cấu trúc phức tạp của Random Forest. Những hạn chế này có thể được cải thiện trong tương lai thông qua việc bổ sung thêm các đặc trưng về sentiment thị trường và tối ưu hóa quy trình huấn luyện.
