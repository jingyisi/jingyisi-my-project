import requests
from bs4 import BeautifulSoup
import re
import time

# --- 配置参数 ---
base_url = "https://www.22biqu.com/biqu1/"  # 基础URL
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36 Edg/145.0.0.0'
}

# --- 格式化函数 ---
def format_text(text, line_width=60, indent="    "):
    """
    将长文本格式化为指定宽度的多行文本。
    :param text: 原始文本
    :param line_width: 每行字符数限制
    :param indent: 段落缩进（可选）
    :return: 格式化后的字符串
    """
    # 1. 清理文本：去除首尾空白、多余的换行和空格
    cleaned_text = re.sub(r'\s+', ' ', text).strip()

    # 2. 如果文本为空，直接返回
    if not cleaned_text:
        return ""

    # 3. 按指定宽度切割字符串
    lines = []
    for i in range(0, len(cleaned_text), line_width):
        line = cleaned_text[i:i + line_width]
        # 如果需要首行缩进，可以在第一行加上 indent
        # 这里为了模拟小说格式，我们通常段首空两格，这里用4个空格代替
        formatted_line = indent + line if i == 0 else line
        lines.append(formatted_line)

    return "\n".join(lines)

# --- 爬取逻辑 ---
def crawl_and_save():
    with open("novel_output.txt", "w", encoding="utf-8") as f:
        page_num = 1

        while True:
            # 生成URL
            if page_num % 2 == 1:
                # 奇数页：1.html, 2.html, 3.html...
                chapter_num = (page_num + 1) // 2
                url = f"{base_url}{chapter_num}.html"
            else:
                # 偶数页：1_2.html, 2_2.html...
                chapter_num = page_num // 2
                url = f"{base_url}{chapter_num}_2.html"

            print(f"正在爬取: {url}")

            try:
                response = requests.get(url, headers=headers, timeout=10)
                response.encoding = 'utf-8'  # 笔趣阁通常用 gbk 编码，如果乱码请改为 utf-8
                soup = BeautifulSoup(response.text, 'html.parser')

                # 查找小说正文（笔趣阁通用的 id="content"）
                content_div = soup.find('div', id='content')
                if not content_div:
                    print("未找到正文内容，可能已到达末尾。")
                    break

                # 提取文本
                raw_text = content_div.get_text()

                # --- 关键修改：格式化输出 ---
                # 这里调用上面写的格式化函数
                formatted_text = format_text(raw_text, line_width=50, indent="  ")

                # 写入文件
                f.write(f"--- 第 {page_num} 页内容 ---\n")
                f.write(formatted_text + "\n\n")
                f.write("=" * 40 + "\n\n")

                print(f"第 {page_num} 页爬取完成")

                # 简单的防封策略：休眠1秒
                time.sleep(2)

                page_num += 1

            except Exception as e:
                print(f"爬取出错: {e}")
                break

if __name__ == "__main__":
    crawl_and_save()