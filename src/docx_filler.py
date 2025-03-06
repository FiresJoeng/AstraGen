import os
import json
from docx import Document

os.makedirs('input', exist_ok=True)
os.makedirs('output', exist_ok=True)


def load_json(json_path):
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"[Error] JSON 文件不存在: {json_path}")
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"[Error] 解析 JSON 文件出错 {json_path}: {e}")
    return data


def clone_row(table, row):
    """
    克隆表格中的一行
    """
    # 添加新行
    new_row = table.add_row()
    # 将模板行的每个单元格文本复制到新行对应单元格中
    for idx, cell in enumerate(row.cells):
        new_row.cells[idx].text = cell.text
    return new_row


def process_template_row(table, row, list_key, item_list):
    """
    根据模板行，生成列表数据行，list_key: JSON 中的键名称，item_list: 列表数据
    """
    for item in item_list:
        new_row = clone_row(table, row)
        # 对新行中每个单元格进行占位符替换：占位符格式要求为 {字段名}
        for cell in new_row.cells:
            for key, value in item.items():
                placeholder = "{" + key + "}"
                if placeholder in cell.text:
                    cell.text = cell.text.replace(placeholder, str(value))
    # 删除模板行
    tbl = table._tbl
    tbl.remove(row._tr)


def fill_docx(template_path, fill_data, output_path):
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"[Error] 模板文件不存在: {template_path}")
    try:
        doc = Document(template_path)
    except Exception as e:
        raise ValueError(f"[Error] 打开模板文件出错: {e}")

    if not isinstance(fill_data, dict):
        raise TypeError("[Error] fill_data 必须为字典类型。")

    # 处理普通段落内的占位符（仅针对字符串类型数据）
    for para in doc.paragraphs:
        for key, value in fill_data.items():
            # 只处理简单类型数据
            if not isinstance(value, (list, dict)):
                if key in para.text:
                    for run in para.runs:
                        if key in run.text:
                            run.text = run.text.replace(key, str(value))

    # 表格处理
    for table in doc.tables:
        # 先处理表格内的普通单元格（字符串替换）
        for row in table.rows:
            for cell in row.cells:
                for key, value in fill_data.items():
                    if not isinstance(value, (list, dict)):
                        if key in cell.text:
                            cell.text = cell.text.replace(key, str(value))
        # 针对列表数据（如 shareholders, key_personnel）进行模板行复制
        # 这里遍历表格每一行，查找是否存在模板标记
        rows_to_process = []
        for row in table.rows:
            for cell in row.cells:
                if "[shareholders]" in cell.text:
                    rows_to_process.append((row, "shareholders"))
                elif "[key_personnel]" in cell.text:
                    rows_to_process.append((row, "key_personnel"))
        # 依次处理所有需要复制的模板行
        for row, list_key in rows_to_process:
            item_list = fill_data.get(list_key, [])
            # 若列表为空，则直接删除模板行
            if item_list:
                process_template_row(table, row, list_key, item_list)
            else:
                # 删除模板行
                tbl = table._tbl
                tbl.remove(row._tr)

    try:
        doc.save(output_path)
    except Exception as e:
        raise IOError(f"[Error] 保存文档到 {output_path} 出错: {e}")


def generate_report(keyword, template='input/template.docx', output_dir='output'):
    if not keyword:
        raise ValueError("[Error] 企业名称不能为空，你是怎么做到的？")
    json_path = os.path.join(output_dir, f"{keyword}.json")
    fill_data = load_json(json_path)

    output_filename = f"关于{keyword}的贷款申请调查报告.docx"
    output_path = os.path.join(output_dir, output_filename)
    fill_docx(template, fill_data, output_path)

    return output_path


if __name__ == "__main__":
    try:
        keyword = input("文件名 (无后缀) > ").strip()
        if not keyword:
            raise ValueError("[Error] 文件名不能为空！")
        result = generate_report(keyword)
        print("生成的报告路径：", result)
    except Exception as e:
        print("[Error] 程序出现错误:", str(e))
