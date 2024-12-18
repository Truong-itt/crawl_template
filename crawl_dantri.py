import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm

def get_url_every_page(link):
    temp = []
    response = requests.get(link)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        div_total = soup.find('div', id='bai-viet')
        h3s = div_total.find_all('h3', class_='article-title')
        for h3 in h3s:
            a = h3.find('a')
            link = "https://dantri.com.vn" + a.get('href')
            temp.append(link)
        return temp
    else:
        print(f"Request thất bại với mã trạng thái: {response.status_code}")
        return []

def full_link():    
    print("Đang lấy dữ liệu từ page...")
    total_link_page = []
    for i in tqdm(range(1, 30)):
        if i == 1:
            url = "https://dantri.com.vn/xa-hoi.htm"
        else:
            url = f"https://dantri.com.vn/xa-hoi/trang-{i}.htm"    
        total_link_page.extend(get_url_every_page(url))
    return total_link_page

def get_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
    else:
        print(f"Request thất bại với mã trạng thái: {response.status_code}")

def get_content(urls):
    print("Đang lấy dữ liệu từ các link...")
    content_total = []
    for i in tqdm(urls):
        try:
            content = get_url(i)
            h1_link = content.find('h1')
            h2_link = content.find('h2')
            h2_link_text = h2_link.text.replace("(Dân trí) -", "").strip() if h2_link else None
            
            body = content.find('div', class_=['singular-content', 'dnews__body', 'e-magazine__body'])
            body_text = ""
            if body:
                for item_p in body.find_all('p', recursive=True):
                    body_text += item_p.get_text(strip=True) + " " 

            content_total_page = {
                'link': i,
                'title': h1_link.text.strip() if h1_link else 'Không có tiêu đề',
                'sub_title': h2_link_text if h2_link_text else 'Không có tiêu đề phụ',
                'content': body_text.strip() if body_text else 'Không có nội dung'
            }
            content_total.append(content_total_page)
        except Exception as e:
            print(f"Lỗi khi xử lý link: {i} - {e}")
            
    return content_total

def data_to_csv(data):
    df = pd.DataFrame(data)
    df.to_csv('data.csv', index=False, encoding='utf-8-sig', sep=';', header=True)
    print("Dữ liệu đã được ghi vào 'data.csv'")
    
if __name__ == '__main__':
    data_to_csv(get_content(full_link()))
    