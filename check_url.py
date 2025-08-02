import re

def find_urls(text):
    # パス部分も非キャプチャグループに
    pattern = r'https?://[\w\.-]+(?:\.[A-Za-z]{2,})+(?:/[^\s]*)?'
    return re.findall(pattern, text)

if __name__ == "__main__":
    sample_text = """
    こんにちは！
    私のブログは https://example.com です。
    会社のサイトは http://company.co.jp/path/to/page ですね。
    おまけのリンク： https://sub.domain.org
    """
    found = find_urls(sample_text)
    print("見つかった URL:", found)
