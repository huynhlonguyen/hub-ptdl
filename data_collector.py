"""
File: data_collector.py
Chức năng: Thu thập dữ liệu chứng khoán từ Yahoo Finance
"""

import os
import pandas as pd
import yfinance as yf
from datetime import datetime
import logging
from tqdm import tqdm
from src.config import (
    VN30_SYMBOLS, START_DATE, END_DATE,
    DATA_DIR, OUTPUT_DIR
)

# Thiết lập logging
logging.basicConfig(
    filename='analysis.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def ensure_directories():
    """Tạo các thư mục cần thiết"""
    for d in [DATA_DIR, OUTPUT_DIR]:
        if not os.path.exists(d):
            os.makedirs(d)
            logging.info(f"Đã tạo thư mục: {d}")

def get_stock_data_yf(symbol):
    """Lấy dữ liệu từ Yahoo Finance"""
    try:
        # Thêm .VN vào mã cổ phiếu cho thị trường Việt Nam
        ticker = yf.Ticker(f"{symbol}.VN")
        df = ticker.history(start=START_DATE, end=END_DATE)
        
        if not df.empty:
            df = df.reset_index()
            df = df.rename(columns={
                'Date': 'date',
                'Open': f'{symbol}_open',
                'High': f'{symbol}_high',
                'Low': f'{symbol}_low',
                'Close': f'{symbol}_close',
                'Volume': f'{symbol}_volume'
            })
            
            # Chỉ giữ lại các cột cần thiết
            cols_to_keep = ['date', f'{symbol}_open', f'{symbol}_high', 
                           f'{symbol}_low', f'{symbol}_close', f'{symbol}_volume']
            df = df[cols_to_keep]
            
            logging.info(f"Đã lấy dữ liệu {symbol} từ Yahoo Finance")
            return df
        else:
            logging.warning(f"Không có dữ liệu cho mã {symbol}")
            return None
            
    except Exception as e:
        logging.error(f"Lỗi khi lấy dữ liệu {symbol}: {str(e)}")
        return None

def collect_data():
    """Thu thập dữ liệu cho tất cả mã VN30"""
    ensure_directories()
    
    all_data = []
    failed_symbols = []
    
    for symbol in tqdm(VN30_SYMBOLS, desc="Đang thu thập dữ liệu"):
        df = get_stock_data_yf(symbol)
        
        if df is not None:
            all_data.append(df)
        else:
            failed_symbols.append(symbol)
    
    if failed_symbols:
        logging.warning(f"Không thể lấy dữ liệu cho các mã: {failed_symbols}")
    
    if all_data:
        try:
            # Gộp tất cả dữ liệu
            final_df = pd.concat(all_data, axis=1)
            
            # Xử lý cột date trùng lặp
            date_cols = [col for col in final_df.columns if col == 'date']
            if len(date_cols) > 1:
                # Giữ lại cột date đầu tiên và xóa các cột date trùng
                final_df = final_df.loc[:, ~final_df.columns.duplicated()]
            
            # Đảm bảo cột date là index
            final_df.set_index('date', inplace=True)
            final_df.sort_index(inplace=True)
            
            # Lưu dữ liệu
            output_file = os.path.join(OUTPUT_DIR, "stock_data.csv")
            final_df.to_csv(output_file)
            
            logging.info(f"Đã lưu dữ liệu thành công vào {output_file}")
            logging.info(f"Số dòng: {len(final_df)}, Số cột: {len(final_df.columns)}")
            logging.info(f"Khoảng thời gian: từ {final_df.index.min()} đến {final_df.index.max()}")
            
            return final_df
        except Exception as e:
            logging.error(f"Lỗi khi xử lý và lưu dữ liệu: {str(e)}")
            return None
    else:
        logging.error("Không thu thập được dữ liệu nào")
        return None

if __name__ == "__main__":
    collect_data() 