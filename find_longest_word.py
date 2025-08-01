# find_longest_word.py

def find_longest_word(text):
    """
    入力された文字列 text をスペースで分割し、
    最も長い単語を返す関数
    """
    # 1. 文章をスペースで分ける
    words = text.split()

    # 2. 最長単語を記憶する変数（最初は空文字列）
    longest = ""

    # 3. すべての単語をチェック
    for word in words:
        # strip() で「.,!?。、！?」などの記号を取り除く（任意）
        clean_word = word.strip('.,!?。、！?')
        # 長さを比較して更新
        if len(clean_word) > len(longest):
            longest = clean_word

    return longest

if __name__ == "__main__":
    # ユーザーから文章を入力してもらう
    sentence = input("文章を入力してください: ")
    
    # 関数を呼び出して最長単語を取得
    result = find_longest_word(sentence)
    
    # 結果を表示
    print(f"最長の単語は「{result}」です（文字数: {len(result)}文字）。")
