import random

def make_problem():
    a = random.randint(1, 10)
    b = random.randint(1, 10)
    operator = random.choice(['+', '-', '*', '/'])
    if operator == '/':
        a = a * b
    return a, b, operator

def check_answer(a, b, operator, user_input):
    if operator == '+':
        correct = a + b
    elif operator == '-':
        correct = a - b
    elif operator == '*':
        correct = a * b
    else:
        correct = round(a / b, 2)
    try:
        return float(user_input) == correct
    except ValueError:
        return False

def main():
    total = 5
    correct_count = 0

    for i in range(1, total + 1):
        a, b, op = make_problem()
        question = f"問題{i}: {a} {op} {b} = ? "
        answer = input(question)
        if check_answer(a, b, op, answer):
            print("✅ 正解！")
            correct_count += 1
        else:
            if op == '/':
                right = round(a / b, 2)
            else:
                right = eval(f"{a}{op}{b}")
            print(f"❌ 不正解… 正しい答えは {right} です。")
        print()

    rate = correct_count / total * 100
    print(f"【結果】 {total} 問中 {correct_count} 問正解 → 正答率：{rate:.1f}%")

# ここで main() を実行する
if __name__ == "__main__":
    main()
