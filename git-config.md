# Cấu hình Git cho dự án

## Thông tin người dùng
- Username: huynhlonguyen
- Email: huynhlonguyen@gmail.com

## Repository
https://github.com/huynhlonguyen/hub-ptdl.git

## Các lệnh Git cần thiết

### Cấu hình Git
```bash
git config --global user.email "huynhlonguyen@gmail.com"
git config --global user.name "huynhlonguyen"
```

### Khởi tạo và push repository
```bash
# Khởi tạo repository
git init

# Thêm tất cả file vào staging
git add .

# Commit đầu tiên
git commit -m "first commit"

# Đổi tên nhánh chính thành main
git branch -M main

# Thêm remote repository
git remote add origin https://github.com/huynhlonguyen/hub-ptdl.git

# Push code lên GitHub
git push -u origin main
```

### Push code mới (cho các lần sau)
```bash
git add .
git commit -m "update code"
git push
```