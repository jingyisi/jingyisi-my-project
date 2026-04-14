import requests
from bs4 import BeautifulSoup
import re
import time

# 请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36 Edg/145.0.0.0"
}

# -------------------------------
# 2. 发送请求获取网页 (修正：循环获取并拼接内容)
# -------------------------------
def fetch_pages(base_url, start_page, end_page):
    all_html_content = ""  # 用于存储所有页面的文本
    try:
        for page in range(start_page, end_page + 1):
            target_url = f'{base_url}/{page}.html'
            print(f"正在请求: {target_url}")

            response = requests.get(target_url, headers=headers, timeout=10)
            response.encoding = 'utf-8'  # 建议根据网站实际编码调整，通常是 utf-8 或 gbk

            if response.status_code == 200:
                # 将每一页的内容拼接到一起
                all_html_content += response.text
                time.sleep(1)  # 防止请求过快被封禁
            else:
                print(f"页面 {page} 请求失败，状态码: {response.status_code}")

        return all_html_content  # 返回所有页面的合并内容

    except Exception as e:
        print(f"请求过程中出错: {e}")
        return all_html_content  # 即使出错，也返回目前已获取的内容


# -------------------------------
# 3. 清洗文本：核心处理换行符
# -------------------------------
def clean_text(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # --- 1. 提取正文 ---
    # 【注意】这是最关键的一步，class 名称必须和网站源码一致
    # 如果你的网站正文在 <div class="content"> 或 <div id="content"> 中，请修改这里的查找规则
    content_div = soup.find('div', class_='content')  # 尝试匹配 class="content"
    if not content_div:
        content_div = soup.find('div', id='content')   # 尝试匹配 id="content"
    if not content_div:
        content_div = soup.find('div', class_='chapter-content') # 原代码中的尝试
    if not content_div:
        print("警告：未找到正文容器，将提取整个页面文本。")
        content_div = soup.find('body')

    text = content_div.get_text()

    # --- 2. 去除 HTML 实体和特殊空格 ---
    text = text.replace('\xa0', '').replace('&nbsp;', '').replace('\t', '')

    # --- 3. 修复排版折行 ---
    # 逻辑：如果一行末尾不是句号、问号等，且后面有换行，就合并
    text = re.sub(r'([^。！？\?\.])\n+(?=[^。！？\?\.])', r'\1', text)

    # --- 4. 去除每行开头和结尾的空白字符 ---
    lines = text.split('\n')
    cleaned_lines = []
    for line in lines:
        stripped_line = line.strip()
        if stripped_line:  # 非空行
            cleaned_lines.append(stripped_line)
        else:  # 空行（用于分段）
            cleaned_lines.append('')

    text = '\n'.join(cleaned_lines)

    # --- 5. 去除多余的空白行 ---
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text.strip()


# -------------------------------
# 4. 保存到文件
# -------------------------------
def save_to_file(content, filename="full_novel.txt"):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"清洗完成！已保存到 {filename}")


# -------------------------------
# 5. 主程序
# -------------------------------
if __name__ == "__main__":
    print("正在爬取网页...")

    # 这里的 base_url 是不带页码和 .html 后缀的
    base_url = "https://www.22biqu.com/biqu1"

    # 调用函数爬取第1页到第2页
    raw_html = fetch_pages(base_url, 1, 2)

    if raw_html:
        print("正在清洗文本（处理换行符）...")
        cleaned_text = clean_text(raw_html)

        # 保存完整内容
        save_to_file(cleaned_text, "full_novel_cleaned.txt")
    else:
        print("未能获取网页内容。")