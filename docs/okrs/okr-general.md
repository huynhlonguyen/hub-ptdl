# Mục tiêu chính (Objective)

> Repository GitHub: https://github.com/huynhlonguyen/hub-ptdl
> 
> Lưu ý: Toàn bộ mã nguồn code và thông tin của dự án này sẽ được lưu trữ và quản lý tại repository GitHub trên.

## Đề Tài Đã Chọn
**Dự Đoán Xu Hướng Đầu Tư Chứng Khoán Dựa Trên Phân Tích Dữ Liệu Hành Vi Nhà Đầu Tư Cá Nhân**

### Phạm vi dữ liệu mới
- Thời gian: 3 năm gần nhất (2021-2024)
- Tập trung vào các mã chứng khoán VN30
- Nguồn dữ liệu: HOSE, SSI, TCBS, VNDirect
- Tần suất cập nhật: Hàng ngày

### Vấn đề kỹ thuật cần giải quyết
1. Lỗi visualization:
   - Sửa lỗi biểu đồ phân tích kỹ thuật trắng
   - Cập nhật danh sách mã chứng khoán theo VN30
   - Thêm kiểm tra dữ liệu trước khi vẽ

2. Cải thiện thu thập dữ liệu:
   - Giới hạn thời gian lấy dữ liệu 3 năm gần nhất
   - Thêm validation cho dữ liệu thiếu
   - Log chi tiết quá trình thu thập

3. Tối ưu hóa phân tích:
   - Tập trung vào các mã VN30
   - Thêm các chỉ báo kỹ thuật mới
   - Cải thiện hiệu suất xử lý

### 1. Phân Tích 5W1H
- **What (Cái gì):** Dự đoán xu hướng đầu tư chứng khoán dựa trên hành vi nhà đầu tư
- **Why (Tại sao):** 
  + Giúp nhà đầu tư ra quyết định đầu tư tốt hơn
  + Tối ưu hóa chiến lược đầu tư
  + Giảm thiểu rủi ro
- **Where (Ở đâu):** 
  + Thị trường chứng khoán Việt Nam
  + Các nền tảng môi giới chứng khoán
- **When (Khi nào):** 
  + Dữ liệu theo thời gian thực
  + Phân tích lịch sử giao dịch
- **Who (Ai):** 
  + Nhà đầu tư cá nhân
  + Công ty môi giới
  + Các tổ chức tài chính
- **How (Như thế nào):** 
  + Thu thập dữ liệu từ nền tảng môi giới
  + Phân tích hành vi giao dịch
  + Xây dựng mô hình dự đoán

### 2. Phân Tích Pros và Cons
**Pros:**
- Dữ liệu có cấu trúc rõ ràng
- Nhiều nguồn dữ liệu công khai
- Có tính ứng dụng cao
- Phù hợp với chuyên môn

**Cons:**
- Dữ liệu thị trường phức tạp
- Nhiều yếu tố ảnh hưởng
- Độ chính xác khó đảm bảo
- Cần kiến thức chuyên sâu về thị trường

### 3. Phân Tích 6 Thinking Hats
- **White Hat (Dữ liệu):** 
  + Dữ liệu giao dịch chi tiết
  + Dữ liệu thị trường phong phú
  + Nhiều nguồn dữ liệu uy tín
- **Red Hat (Cảm xúc):** 
  + Quan tâm cao từ nhà đầu tư
  + Có tính cấp thiết
  + Có giá trị thực tế
- **Black Hat (Thận trọng):** 
  + Rủi ro cao trong dự đoán
  + Nhiều yếu tố ảnh hưởng
  + Độ chính xác khó đảm bảo
- **Yellow Hat (Lạc quan):** 
  + Có tiềm năng ứng dụng cao
  + Nhiều cơ hội phát triển
  + Có giá trị thương mại
- **Green Hat (Sáng tạo):** 
  + Có thể kết hợp nhiều phương pháp
  + Nhiều hướng phát triển
  + Có tính đổi mới
- **Blue Hat (Tổng hợp):** 
  + Phù hợp với chuyên môn
  + Có tính khả thi
  + Cần đầu tư thời gian

### 4. Nguồn Dữ Liệu
#### 4.1 Dữ Liệu Chính (Thị Trường Việt Nam)
- **Dữ liệu thị trường:**
  + HOSE (Sở Giao Dịch Chứng Khoán TP.HCM)
  + SSI (Công ty Chứng Khoán SSI)
  + TCBS (Techcombank Securities)
  + VNDirect

- **Dữ liệu hành vi:**
  + Dữ liệu giao dịch từ các nền tảng môi giới
  + Dữ liệu từ VSD (Vietnam Securities Depository)
  + Dữ liệu từ các tổ chức tài chính

#### 4.2 Dữ Liệu Bổ Sung
- **Dữ liệu vĩ mô:**
  + SBV (State Bank of Vietnam)
  + World Bank Open Data
  + IMF Data

- **Dữ liệu phân tích:**
  + Cafef
  + Vietstock
  + Các báo cáo tài chính công khai

#### 4.3 Giấy Phép Sử Dụng
- Free for academic research cho dữ liệu từ HOSE, VSD, SBV
- Free API key cho các nền tảng môi giới (SSI, TCBS, VNDirect)
- CC0 (Public Domain) cho dữ liệu từ World Bank, IMF
- Free for academic use cho dữ liệu từ các nền tảng phân tích

### 5. Phương Pháp Nghiên Cứu
- Thu thập và tiền xử lý dữ liệu
- Phân tích khám phá dữ liệu (EDA)
- Xây dựng mô hình học máy
- Đánh giá và tối ưu hóa mô hình
- Triển khai và kiểm thử

## Cấu trúc thư mục dự án
```
docs/
├── references/           # Thư mục chứa các tài liệu tham khảo đã tải về
│   ├── academic/        # Tài liệu học thuật (journal articles, conference papers)
│   ├── books/          # Sách chuyên khảo
│   ├── reports/        # Báo cáo nghiên cứu
│   └── online/         # Tài liệu trực tuyến
│
└── tieu-luan/          # Thư mục chứa bài tiểu luận
    ├── chuong1.md      # Chương 1: Giới thiệu
    ├── chuong2.md      # Chương 2: Tổng quan
    ├── chuong3.md      # Chương 3: Quy trình
    ├── chuong4.md      # Chương 4: Xây dựng mô hình
    ├── chuong5.md      # Chương 5: Đánh giá
    └── chuong6.md      # Chương 6: Ứng dụng
```

## Quản lý tài liệu
1. Tài liệu tham khảo:
   - Tải và lưu trữ trong thư mục `docs/references/`
   - Phân loại theo loại tài liệu (academic, books, reports, online)
   - Đặt tên file theo format: `YYYY-Author-Title.pdf`
   - Tạo file `index.md` trong mỗi thư mục con để liệt kê và mô tả tài liệu

2. Bài tiểu luận:
   - Lưu trữ trong thư mục `docs/tieu-luan/`
   - Mỗi chương được viết trong một file Markdown riêng
   - Sử dụng Markdown để định dạng văn bản theo chuẩn học thuật
   - Có thể chuyển đổi sang PDF khi hoàn thành

- Hoàn thành bài tiểu luận cá nhân đạt chất lượng cao theo yêu cầu của đề bài, cụ thể:

  + Yêu cầu về nội dung:
    - Đề tài có tính mới và đóng góp khoa học
    - Phương pháp nghiên cứu rõ ràng, có cơ sở lý thuyết vững chắc
    - Phân tích dữ liệu sâu sắc, có ý nghĩa thực tiễn
    - Kết luận và đề xuất có tính khả thi cao
    - Tài liệu tham khảo đầy đủ, cập nhật và có độ tin cậy cao

  + Yêu cầu về cấu trúc: (Mẫu) 
    - Chương 1: Giới thiệu về phân tích dữ liệu và học máy trong thương mại điện tử
      * Tổng quan về lĩnh vực
      * Vai trò của phân tích dữ liệu và học máy
      * Các ứng dụng thực tế

    - Chương 2: Tổng quan về các thuật toán dự đoán xu hướng tiêu dùng
      * Các phương pháp học máy phổ biến
      * So sánh ưu nhược điểm
      * Lựa chọn phương pháp phù hợp

    - Chương 3: Quy trình thu thập và xử lý dữ liệu hành vi khách hàng
      * Phương pháp thu thập dữ liệu
      * Tiền xử lý dữ liệu
      * Phân tích khám phá dữ liệu

    - Chương 4: Xây dựng mô hình học máy để dự đoán sản phẩm khách hàng sẽ quan tâm
      * Thiết kế mô hình
      * Huấn luyện và tối ưu hóa
      * Điều chỉnh siêu tham số

    - Chương 5: Đánh giá hiệu suất mô hình và các yếu tố ảnh hưởng đến độ chính xác
      * Các chỉ số đánh giá
      * Phân tích kết quả
      * Đề xuất cải thiện

    - Chương 6: Ứng dụng thực tế và đề xuất cải tiến trong tương lai
      * Triển khai mô hình
      * Giải pháp thực tế
      * Hướng phát triển

    - Tài liệu tham khảo (References)
      * Định dạng theo chuẩn APA 7th Edition
      * Tối thiểu 20 tài liệu tham khảo
      * Phân loại theo:
        - Tài liệu học thuật (journal articles, conference papers)
        - Sách chuyên khảo
        - Báo cáo nghiên cứu
        - Tài liệu trực tuyến
      * Các nguồn tài liệu cần tải về:
        - Google Scholar
        - ResearchGate
        - Academia.edu
        - IEEE Xplore
        - ScienceDirect
        - SpringerLink
        - Wiley Online Library
        - ACM Digital Library
        - arXiv.org
        - SSRN (Social Science Research Network)

    - Phân bổ số từ theo cấu trúc (Tổng: 6,750 từ, ±5%):
      * Chương 1 (Giới thiệu): 1,000 từ
      * Chương 2 (Tổng quan): 1,000 từ
      * Chương 3 (Quy trình): 1,250 từ
      * Chương 4 (Xây dựng mô hình): 1,250 từ
      * Chương 5 (Đánh giá): 1,000 từ
      * Chương 6 (Ứng dụng): 1,250 từ
      * Tài liệu tham khảo: Không tính vào tổng số từ

  + Yêu cầu về hình thức:
    - Định dạng văn bản theo chuẩn học thuật
    - Trích dẫn và tài liệu tham khảo đúng quy cách
    - Bảng biểu, đồ thị rõ ràng, có chú thích đầy đủ
    - Ngôn ngữ khoa học, chính xác, dễ hiểu

  + Yêu cầu về đóng góp:
    - Đóng góp mới về mặt lý thuyết
    - Đề xuất giải pháp thực tiễn có giá trị
    - Phương pháp nghiên cứu có thể áp dụng rộng rãi
    - Kết quả có thể phục vụ cho việc ra quyết định

# Kết quả chính (Key Results)
## 1. Lựa chọn đề tài phù hợp
- Đề tài phải thỏa mãn các tiêu chí:
  + Phù hợp với yêu cầu trong de-bai.md
  + Có nguồn dữ liệu chất lượng và dễ tiếp cận
  + Có nhiều tài liệu tham khảo và case study thành công
  + Phù hợp với chuyên môn và kinh nghiệm

## 2. Nguồn dữ liệu
- Các nguồn dữ liệu tiềm năng:
  + Kaggle datasets
  + Dữ liệu từ các tổ chức tài chính
  + Dữ liệu công khai từ các sở giao dịch
  + Dataverse Harvard (https://dataverse.harvard.edu/)
  + World Bank Open Data (https://data.worldbank.org/)
  + IMF Data (https://www.imf.org/en/Data)
  + Yahoo Finance API
  + Alpha Vantage API
  + FRED (Federal Reserve Economic Data)
  + Quandl (một số dataset miễn phí)
  + Google Finance
  + Investing.com
  + Các báo cáo tài chính công khai của các công ty niêm yết
  + Dữ liệu từ các tổ chức nghiên cứu tài chính (NBER, SSRN)
  + Các nguồn dữ liệu từ chính phủ và ngân hàng trung ương

## 3. Chuyên môn và kinh nghiệm
- Lĩnh vực chuyên môn:
  + Chứng khoán và thị trường tài chính
  + Dịch vụ ngân hàng
  + Quản lý tài khoản chứng khoán
- Kinh nghiệm thực tế:
  + Mở tài khoản chứng khoán cho khách hàng
  + Tư vấn đầu tư
- Sở thích và hiểu biết:
  + Du lịch Hàn Quốc, Nhật Bản
  + Văn hóa và kinh tế Đông Á

# Ghi chú
- File này sẽ được cập nhật thường xuyên theo tiến độ công việc
- Các mục quan trọng và đang thực hiện sẽ được đưa lên đầu file
- Các mục đã hoàn thành sẽ được chuyển xuống cuối file

# Tiến độ công việc

## Đã hoàn thành
1. Chọn đề tài: "Dự Đoán Xu Hướng Đầu Tư Chứng Khoán Dựa Trên Phân Tích Dữ liệu Hành Vi Nhà Đầu Tư Cá Nhân"

2. Thu thập và tổ chức dữ liệu:
   - Tạo cấu trúc thư mục cho dự án
   - Tải dữ liệu từ AlphaResearchVietnamMarket (HOSE 2008-2022)
   - Tổ chức dữ liệu thành các nhóm:
     * Dữ liệu thị trường (giá, khối lượng giao dịch, lợi nhuận)
     * Thông tin công ty (mô tả, tài chính)
   - Tổ chức output vào thư mục thống nhất:
     * output/models/: Kết quả huấn luyện mô hình
     * output/sentiment/: Phân tích sentiment
     * Các file phân tích kỹ thuật và thống kê

3. Phân tích dữ liệu cơ bản:
   - Tạo script phân tích thống kê cơ bản
   - Vẽ biểu đồ xu hướng giá các cổ phiếu lớn
   - Tính toán ma trận tương quan
   - Phân tích độ biến động của cổ phiếu

4. Phân tích sentiment thị trường:
   - Tính toán và phân tích các chỉ số:
     * ADR trung bình: 1.71
     * Market Turnover và Share Turnover có xu hướng tăng
     * Độ biến động ADR cao (std = 2.18)
   - Tạo biểu đồ xu hướng các chỉ số

5. Xây dựng mô hình ban đầu:
   - Mô hình hai tầng (Random Forest + Logistic Regression)
   - Kết quả đánh giá:
     * Accuracy: 44.44%
     * Precision: 47.04%
     * Recall: 44.44%
     * F1-score: 37.94%

## Đang thực hiện
1. Cải thiện mô hình dự đoán:
   - Tối ưu hóa hyperparameters
   - Thêm features từ phân tích sentiment
   - Thử nghiệm các thuật toán ensemble khác
   - Cross-validation với nhiều khoảng thời gian

2. Thu thập thêm dữ liệu về hành vi nhà đầu tư:
   - Dữ liệu khối lượng giao dịch theo nhóm
   - Dữ liệu sentiment từ diễn đàn và mạng xã hội
   - Dữ liệu về tỷ lệ margin

3. O1: Tối ưu hóa hiệu suất phân tích dữ liệu
**KR1.1:** Giảm thời gian xử lý xuống 50% so với baseline
- [ ] Tối ưu hóa hàm filter_recent_data
- [ ] Sử dụng parallel processing cho phân tích đa mã
- [ ] Cache kết quả tính toán trung gian

**KR1.2:** Tăng độ chính xác của mô hình lên 60%
- [ ] Thêm features mới từ sentiment analysis
- [ ] Tối ưu hyperparameters
- [ ] Cross-validation với nhiều khoảng thời gian

### O2: Cải thiện độ tin cậy của hệ thống
**KR2.1:** Giảm số lỗi runtime xuống 0
- [x] Thêm logging chi tiết
- [x] Validate dữ liệu đầu vào
- [ ] Xử lý các edge cases

**KR2.2:** Tăng khả năng theo dõi và debug
- [x] Thêm logging vào file
- [ ] Thêm unit tests
- [ ] Thêm monitoring metrics

### Kế hoạch thực hiện ngắn hạn

#### Tuần 1: Setup và Cải thiện cơ sở
- [x] Cập nhật run_analysis.py với xử lý lỗi tốt hơn
- [x] Thêm chức năng lọc dữ liệu theo thời gian
- [ ] Thêm unit tests cho các hàm core

#### Tuần 2: Tối ưu hóa hiệu suất
- [ ] Implement parallel processing
- [ ] Thêm caching layer
- [ ] Profile và tối ưu các bottlenecks

#### Tuần 3: Cải thiện mô hình
- [ ] Thêm features mới
- [ ] Grid search cho hyperparameters
- [ ] Implement cross-validation framework

#### Tuần 4: Testing và Documentation
- [ ] Hoàn thiện test suite
- [ ] Viết documentation chi tiết
- [ ] Tạo báo cáo hiệu suất

### Metrics theo dõi
1. Thời gian xử lý (baseline vs optimized)
2. Độ chính xác của mô hình
3. Số lỗi runtime
4. Test coverage

# Ghi chú
- Các mục quan trọng và đang thực hiện đã được đưa lên đầu
- Các mục đã hoàn thành được chuyển xuống phía dưới
- Kết quả chi tiết được lưu trong thư mục output/