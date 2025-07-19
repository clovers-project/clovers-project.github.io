import re


def process_file(input_file, output_file):
    # 定义正则表达式模式
    # [7.652097, "o", "o"]
    max_num = float("inf")
    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
    flag = True
    while flag:
        flag = False
        outputs = []
        interval = 0.0
        pattern = re.compile(r'^\[(\d+\.\d+), "o", "(.)"\]')
        num = max_num
        for line in lines:
            match = pattern.match(line)
            if match:
                temp_num = float(match.group(1))
                if flag:
                    print(f"{temp_num-interval = }")
                    new_line = f"[{temp_num-interval:.6f}," + line[match.end() :]

                else:
                    if temp_num > (num + 0.35):
                        interval = temp_num - num - 0.34
                        print(f"\n{interval = }, {num = }, {temp_num = }")
                        flag = True
                        pattern = re.compile(r"^\[(\d+\.\d+),")
                    num = temp_num
                    new_line = f'[{temp_num-interval:.6f}, "o", "{match.group(2)}"]' + line[match.end() :]
                outputs.append(new_line)
            else:
                num = max_num
                outputs.append(line)
        lines = outputs
    with open(output_file, "w", encoding="utf-8") as f:
        f.writelines(outputs)


output_filename = "create.cast"
input_filename = output_filename + "0"
process_file(input_filename, output_filename)
