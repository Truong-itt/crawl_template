import pandas as pd
from vnauto import get_vnauto_instance

vnauto = get_vnauto_instance()

def normalize_text(text):
    """Hàm chuẩn hóa văn bản"""
    if pd.isna(text): 
        return text
    return vnauto.normalize(str(text))

def data_to_csv(df, output_file):
    df.to_csv(
        output_file,
        index=False,
        encoding='utf-8-sig',
        sep=',', 
        quotechar='"', 
        escapechar='\\' 
    )
    print("Dữ liệu đã được ghi vào " ,output_file)

def normalize_selected_columns(input_file, output_file):
    df = pd.read_csv(input_file, encoding='utf-8-sig', sep=',', quotechar='"')
    
    columns_to_normalize = ['title', 'sub_title', 'content']
    for col in columns_to_normalize:
        if col in df.columns:
            df[col] = df[col].apply(normalize_text)
    
    data_to_csv(df, output_file)
    print(f"Dữ liệu đã được chuẩn hóa cho các cột {columns_to_normalize} và lưu vào '{output_file}'")

if __name__ == '__main__':
    input_file = 'data.csv'
    output_file = 'data_normalized.csv'
    normalize_selected_columns(input_file, output_file)
