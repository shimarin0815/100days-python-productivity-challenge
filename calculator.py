# calculator.py

def calculate(expr: str) -> float:
    """
    "数字 演算子 数字" の形の文字列 expr を受け取り、
    計算結果を返す関数。
    サポート：+、-、*、/
    """
    # 1. スペースで分ける
    parts = expr.split()
    if len(parts) != 3:
        raise ValueError("入力は「数字 演算子 数字」の形にしてください。")

    num1_str, op, num2_str = parts

    # 2. 文字列を float に変換
    try:
        num1 = float(num1_str)
        num2 = float(num2_str)
    except ValueError:
        raise ValueError("数字の部分を正しく入力してください。")

    # 3. 演算子ごとに計算
    if op == "+":
        return num1 + num2
    elif op == "-":
        return num1 - num2
    elif op == "*":
        return num1 * num2
    elif op == "/":
        if num2 == 0:
            raise ZeroDivisionError("0で割ることはできません。")
        return num1 / num2
    else:
        raise ValueError(f"サポートしていない演算子です：{op}")


if __name__ == "__main__":
    expr = input("計算したい式を入力してください（例：12 + 7）：")
    try:
        result = calculate(expr)
        # 結果が整数なら小数点以下を表示しない
        if isinstance(result, float) and result.is_integer():
            result = int(result)
        print("結果：", result)
    except Exception as e:
        print("エラー：", e)
