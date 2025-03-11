import json
import re
from docx import Document

def replace_placeholder(text, json_data):
    """
    替换给定文本中的占位符：
      - 对于简单键，如 "company_name"，直接替换；
      - 对于数组形式的键，如 "shareholders[name]"，查找 key 后面中括号内的子键，拼接所有数组项中该子键的值。
      - 对于字典形式的值（例如 legal_representative），可支持形如 "legal_representative.name" 的占位符
    """
    # 先处理数组形式的占位符：key[sub_key]
    for key, value in json_data.items():
        if isinstance(value, list):
            # 构造正则：key[sub_key]
            pattern = re.compile(r'{}\[([^\]]+)\]'.format(re.escape(key)))
            # 查找所有匹配的子键
            matches = pattern.findall(text)
            for sub_key in matches:
                # 拼接所有数组项中该子键的值，若某项中不存在则跳过
                replacement = "\n".join(str(item.get(sub_key, '')) for item in value if sub_key in item)
                # 替换所有匹配的占位符
                text = pattern.sub(lambda m: replacement if m.group(1) == sub_key else m.group(0), text)
    
    # 处理字典类型的值（如 legal_representative），支持占位符 legal_representative.name
    for key, value in json_data.items():
        if isinstance(value, dict):
            pattern = re.compile(r'{}\.([a-zA-Z0-9_]+)'.format(re.escape(key)))
            matches = pattern.findall(text)
            for sub_key in matches:
                replacement = str(value.get(sub_key, ''))
                text = pattern.sub(lambda m: replacement if m.group(1) == sub_key else m.group(0), text)
    
    # 处理直接字符串类型的替换
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

def main():
    # 定义文件路径
    json_path = "input/template.json"
    docx_path = "input/template.docx"
    output_path = "output/template.docx"

    # 加载 JSON 数据
    with open(json_path, "r", encoding="utf-8") as f:
        json_data = json.load(f)

    # 处理 docx 文件
    process_docx(docx_path, json_data, output_path)
    print("替换完成，输出文件保存至：", output_path)

if __name__ == "__main__":
    main()
