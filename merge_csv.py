import glob
import csv

# 保存先のファイル名
output_file = 'merged.csv'

# CSVファイルをまとめるフォルダ
input_folder = './'

# CSVファイルのパスを取得
csv_files = glob.glob(input_folder + 'data*.csv')

# 出力ファイルを開く
with open(output_file, 'w', newline='', encoding='utf-8') as fout:
    writer = None

    for i, file in enumerate(csv_files):
        with open(file, 'r', encoding='utf-8') as fin:
            reader = csv.reader(fin)
            header = next(reader)  # ヘッダー行を読み込み

            # 1つ目のファイルなら、ヘッダーを書き込む
            if i == 0:
                writer = csv.writer(fout)
                writer.writerow(header)

            # データ行をすべて書き込む
            for row in reader:
                writer.writerow(row)
