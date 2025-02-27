from docx import Document
import json

template = 'input/template.docx'
doc = Document(template)
keyword = None


with open('input/template.json', 'r', encoding='utf-8') as f:
    data_json = json.load(f)

def fill_docx(dict):
    # 文本处理
    for para in doc.paragraphs:
        for key, value in dict.items():
            if key in para.text:
                for run in para.runs:
                    run.text = run.text.replace(key, value)

    # 表格处理
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for para in cell.paragraphs:
                    for key, value in dict.items():
                        if key in para.text:
                            for run in para.runs:
                                run.text = run.text.replace(key, value)

fill_docx(data_json)
doc.save(f'output/XX支行关于{keyword}的贷款申请调查报告.docx')
