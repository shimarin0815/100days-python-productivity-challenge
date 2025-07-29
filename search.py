# search.py
import argparse
import os

def search_in_file(filepath, keyword):
    """ひとつのファイル内を検索し、キーワードを含む行を返す"""
    results = []
    with open(filepath, encoding='utf-8') as f:
        for num, line in enumerate(f, start=1):
            if keyword in line:
                # 行番号と行の内容をタプルで記録
                results.append((num, line.rstrip()))
    return results

def search_in_folder(folder, keyword):
    """フォルダ内のすべての .txt ファイルを検索"""
    all_results = {}
    for fname in os.listdir(folder):
        if fname.endswith('.txt'):
            path = os.path.join(folder, fname)
            matches = search_in_file(path, keyword)
            if matches:
                all_results[fname] = matches
    return all_results

def main():
    parser = argparse.ArgumentParser(
        description='フォルダ（またはファイル）内でキーワード検索を行います。'
    )
    parser.add_argument('target', help='検索対象のフォルダまたはファイルパス')
    parser.add_argument('keyword', help='検索するキーワード')
    args = parser.parse_args()

    if os.path.isdir(args.target):
        results = search_in_folder(args.target, args.keyword)
        for fname, matches in results.items():
            print(f'--- {fname} ---')
            for num, line in matches:
                print(f'{num}: {line}')
    elif os.path.isfile(args.target):
        matches = search_in_file(args.target, args.keyword)
        for num, line in matches:
            print(f'{num}: {line}')
    else:
        print('エラー：フォルダまたはファイルが見つかりません。')

if __name__ == '__main__':
    main()
