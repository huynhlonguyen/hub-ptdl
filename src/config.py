"""
File: config.py
Chức năng: Cung cấp các cấu hình và hằng số cho dự án
"""

import os
from pathlib import Path

# Thư mục dự án
PROJECT_ROOT = Path(os.path.dirname(os.path.dirname(__file__)))
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "output"

# Cấu hình dữ liệu
START_DATE = "2021-01-01"
END_DATE = "2024-03-23"

# Danh sách mã VN30 (cập nhật 2024)
VN30_SYMBOLS = [
    'ACB', 'BCM', 'BID', 'BVH', 'CTG', 'FPT', 'GAS', 'GVR', 'HDB', 'HPG',
    'MBB', 'MSN', 'MWG', 'NVL', 'PDR', 'PLX', 'PNJ', 'POW', 'SAB', 'SSI',
    'STB', 'TCB', 'TPB', 'VCB', 'VHM', 'VIB', 'VIC', 'VJC', 'VNM', 'VPB'
]

# API endpoints
VNDIRECT_API = "https://finfo-api.vndirect.com.vn/v4"
SSI_API = "https://iboard.ssi.com.vn/dchart/api"

# Cấu hình logging
LOG_FILE = PROJECT_ROOT / "analysis.log"
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

# Cấu hình biểu đồ
PLOT_STYLE = {
    'figure.figsize': (15, 8),
    'axes.titlesize': 14,
    'axes.labelsize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'lines.linewidth': 1.5,
    'grid.alpha': 0.3
} 