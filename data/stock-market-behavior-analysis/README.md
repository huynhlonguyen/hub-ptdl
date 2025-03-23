# Stock Market Behavior Analysis Dataset

## Cấu trúc thư mục

```
stock-market-behavior-analysis/
├── raw/                  # Dữ liệu thô chưa xử lý
│   ├── market_data/      # Dữ liệu thị trường từ HOSE, SSI, etc.
│   ├── sentiment_data/   # Dữ liệu phân tích cảm xúc từ báo chí, mạng xã hội
│   └── macro_data/       # Dữ liệu vĩ mô từ SBV, World Bank, etc.
├── processed/            # Dữ liệu đã được xử lý và chuẩn hóa
│   ├── features/         # Các đặc trưng đã được trích xuất
│   └── models/          # Dữ liệu cho việc huấn luyện mô hình
├── external/            # Dữ liệu từ nguồn bên ngoài
│   ├── benchmarks/      # Dữ liệu so sánh chuẩn
│   └── references/      # Dữ liệu tham khảo
└── metadata/            # Thông tin về dữ liệu
    ├── data_dictionary/ # Từ điển dữ liệu
    └── documentation/   # Tài liệu hướng dẫn
```

## Nguồn dữ liệu

### 1. Dữ liệu thị trường Việt Nam
- **HOSE (Ho Chi Minh Stock Exchange)**
  - Dữ liệu giao dịch chứng khoán
  - API truy cập cho mục đích học thuật
  - Giấy phép: Miễn phí cho nghiên cứu học thuật

- **SSI (SSI Securities Corporation)**
  - Dữ liệu phân tích thị trường
  - Cập nhật thường xuyên
  - API cho khách hàng

### 2. Nền tảng môi giới
- **TCBS (Techcombank Securities)**
  - Dữ liệu giao dịch và phân tích
  - API cho khách hàng

- **VNDirect**
  - Dữ liệu thị trường thời gian thực
  - API cho khách hàng

### 3. Tổ chức tài chính
- **Ngân hàng Nhà nước Việt Nam (SBV)**
  - Dữ liệu vĩ mô và thị trường
  - API truy cập

- **Trung tâm Lưu ký Chứng khoán Việt Nam (VSD)**
  - Dữ liệu giao dịch chi tiết
  - API truy cập

### 4. Nền tảng phân tích
- **Cafef**
  - Tin tức và dữ liệu thị trường
  - API truy cập

- **Vietstock**
  - Dữ liệu và phân tích thị trường
  - API truy cập

## Hướng dẫn sử dụng

1. **Tải dữ liệu**
   - Sử dụng các API được cung cấp để tải dữ liệu
   - Lưu trữ trong thư mục `raw/` theo cấu trúc đã định

2. **Xử lý dữ liệu**
   - Thực hiện các bước tiền xử lý
   - Lưu kết quả trong thư mục `processed/`

3. **Quản lý phiên bản**
   - Sử dụng Git LFS cho các file dữ liệu lớn
   - Ghi chú rõ nguồn và phiên bản dữ liệu

4. **Bảo mật**
   - Không lưu trữ thông tin nhạy cảm
   - Mã hóa các file chứa thông tin xác thực

## Lưu ý

- Đảm bảo tuân thủ giấy phép sử dụng của từng nguồn dữ liệu
- Cập nhật metadata khi có thay đổi về dữ liệu
- Sao lưu dữ liệu định kỳ 