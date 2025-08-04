# generate_qr.py

import qrcode  # QRコードを作るライブラリを読み込む

def make_qr(text, filename):
    """
    text：QRコードにしたい文字列
    filename：保存する画像ファイル名（例："myqr.png"）
    """
    # 1. QRCodeオブジェクトを作る
    qr = qrcode.QRCode(
        version=1,             # サイズ（1～40）小さいとシンプルなコードに
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # エラー訂正レベル
        box_size=10,           # 1つの□（ドット）が何ピクセルか
        border=4               # 周りの余白（□の数）
    )

    # 2. 文字列をセットする
    qr.add_data(text)
    qr.make(fit=True)  # 自動で最適なサイズにする

    # 3. 画像を作成する
    img = qr.make_image(fill_color="black", back_color="white")

    # 4. ファイルに保存する
    img.save(filename)
    print(f"✅ QRコードを {filename} に保存しました！")

if __name__ == "__main__":
    # ここに好きな文字列と出力ファイル名を書いて実行してみよう
    sample_text =  "お誕生日おめでとう！"
    output_file = "happy_birthday_qr.png"
    make_qr(sample_text, output_file)
