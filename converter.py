
import argparse
import json
import yaml
import sys


def to_yaml(input_path, output_path):
    """JSONファイルを読み込んでYAMLファイルを書き出す"""
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"エラー: ファイルが見つかりません: {input_path}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"エラー: JSONの読み込みに失敗しました: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            # allow_unicode=True で日本語文字も問題なく書き出せます
            yaml.dump(data, f, allow_unicode=True, sort_keys=False)
    except Exception as e:
        print(f"エラー: YAMLの書き出しに失敗しました: {e}", file=sys.stderr)
        sys.exit(1)


def to_json(input_path, output_path):
    """YAMLファイルを読み込んでJSONファイルを書き出す"""
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"エラー: ファイルが見つかりません: {input_path}", file=sys.stderr)
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"エラー: YAMLの読み込みに失敗しました: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            # indent=2 で見やすいJSONに整形
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"エラー: JSONの書き出しに失敗しました: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        prog='converter.py',
        description='JSON ⇔ YAML 変換ツール（中学2年生向け）'
    )
    # サブコマンドを使って、どちらの変換をするか選べるようにする
    sub = parser.add_subparsers(dest='command', required=True)

    # JSON→YAML
    p1 = sub.add_parser('to_yaml', help='JSONをYAMLに変換します')
    p1.add_argument('input', help='入力JSONファイル名（例: sample.json）')
    p1.add_argument('output', help='出力YAMLファイル名（例: result.yaml）')

    # YAML→JSON
    p2 = sub.add_parser('to_json', help='YAMLをJSONに変換します')
    p2.add_argument('input', help='入力YAMLファイル名（例: sample.yaml）')
    p2.add_argument('output', help='出力JSONファイル名（例: result.json）')

    args = parser.parse_args()

    if args.command == 'to_yaml':
        to_yaml(args.input, args.output)
    elif args.command == 'to_json':
        to_json(args.input, args.output)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
