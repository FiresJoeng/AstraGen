import json
import re
from docx import Document


def replace_placeholder(text, json_data):
    """
    替换给定文本中的占位符：
      - 对于简单键，直接替换；
      - 对于数组形式的键，查找 key 后面中括号内的子键，拼接所有数组项中该子键的值；
      - 对于字典形式的值，支持形如 "key{sub_key}" 的占位符
    """
    # 数组形式占位符处理: key[sub_key]
    for key, value in json_data.items():
        if isinstance(value, list):
            # 构造正则：key[sub_key]
            pattern = re.compile(r'{}\[([^\]]+)\]'.format(re.escape(key)))
            # 查找所有匹配的子键
            matches = pattern.findall(text)
            for sub_key in matches:
                # 拼接所有数组项中该子键的值，若某项中不存在则跳过
                replacement = "\n".join(str(item.get(sub_key, ''))
                                        for item in value if sub_key in item)
                # 替换所有匹配的占位符
                text = pattern.sub(lambda m: replacement if m.group(
                    1) == sub_key else m.group(0), text)

    # 字典形式占位符处理: key{sub_key}
    for key, value in json_data.items():
        if isinstance(value, dict):
            pattern = re.compile(
                r'{}{{([a-zA-Z0-9_]+)}}'.format(re.escape(key)))
            matches = pattern.findall(text)
            for sub_key in matches:
                replacement = str(value.get(sub_key, ''))
                text = pattern.sub(lambda m: replacement if m.group(
                    1) == sub_key else m.group(0), text)

    # 简单形式占位符处理: key
    for key, value in json_data.items():
        if isinstance(value, (str, int, float)):
            if key in text:
                text = text.replace(key, str(value))
    return text


def process_docx(docx_path, json_data, output_path):
    doc = Document(docx_path)

    # 遍历所有段落
    for paragraph in doc.paragraphs:
        for run in paragraph.runs:
            new_text = replace_placeholder(run.text, json_data)
            run.text = new_text

    # 遍历所有表格中的单元格
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    for run in paragraph.runs:
                        new_text = replace_placeholder(run.text, json_data)
                        run.text = new_text

    # 保存处理后的文档
    doc.save(output_path)


def generate_report(file_name):
    # 定义文件路径
    json_path = f"output/{file_name}.json"
    docx_path = "input/template.docx"
    output_path = f"output/XX支行关于{file_name}的贷款申请报告.docx"

    # 加载 JSON 数据
    with open(json_path, "r", encoding="utf-8") as f:
        json_data = json.load(f)

    # 处理 docx 文件
    process_docx(docx_path, json_data, output_path)
    print("替换完成，输出文件保存至：", output_path)


# 底层运行逻辑，测试用
if __name__ == "__main__":
    try:
        keyword = input("文件名 (无后缀) > ").strip()
        if not keyword:
            raise ValueError("[Error] 文件名不能为空！")
        generate_report(keyword)
    except Exception as e:
        print("[Error] 程序出现错误:", str(e))
