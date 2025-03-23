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

def get_stock_data_yf(symbol, start_date, end_date):
    """Lấy dữ liệu từ Yahoo Finance"""
    try:
        # Thêm .VN vào mã cổ phiếu cho thị trường Việt Nam
        ticker = yf.Ticker(f"{symbol}.VN")
        df = ticker.history(start=start_date, end=end_date)
        
        if not df.empty:
            df.reset_index(inplace=True)
            df.columns = ['date', f'{symbol}_open', f'{symbol}_high', 
                         f'{symbol}_low', f'{symbol}_close', 
                         f'{symbol}_volume', f'{symbol}_dividends', 
                         f'{symbol}_stock_splits']
            
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
        df = get_stock_data_yf(symbol, START_DATE, END_DATE)
        
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
            final_df = final_df.loc[:,~final_df.columns.duplicated()]  # Loại bỏ cột trùng
            
            # Đảm bảo cột date là duy nhất
            date_cols = [col for col in final_df.columns if col == 'date']
            if len(date_cols) > 1:
                final_df = final_df.loc[:,~final_df.columns.duplicated()]
            
            final_df.sort_values('date', inplace=True)
            final_df.reset_index(drop=True, inplace=True)
            
            # Lưu dữ liệu
            output_file = os.path.join(OUTPUT_DIR, "stock_data.csv")
            final_df.to_csv(output_file, index=False)
            logging.info(f"Đã lưu dữ liệu thành công vào {output_file}")
            logging.info(f"Số dòng: {len(final_df)}, Số cột: {len(final_df.columns)}")
            logging.info(f"Khoảng thời gian: từ {final_df['date'].min()} đến {final_df['date'].max()}")
            
            return final_df
        except Exception as e:
            logging.error(f"Lỗi khi xử lý và lưu dữ liệu: {str(e)}")
            return None
    else:
        logging.error("Không thu thập được dữ liệu nào")
        return None

if __name__ == "__main__":
    collect_data() 