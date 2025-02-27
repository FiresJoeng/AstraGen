from docx import Document
import json

template = 'input/template.docx'
doc = Document(template)

with open('input/template.json', 'r', encoding='utf-8') as f:
    替换字典 = json.load(f)

def 填充占位符(替换字典):
    for para in doc.paragraphs:
        for run in para.runs:
            for 占位符, 替换值 in 替换字典.items():
                print(f'已为{占位符}填充{替换值}.')
                if 占位符 in run.text:
                    run.text = run.text.replace(占位符, 替换值)

填充占位符(替换字典)

doc.save('output/filled_template.docx')

# for para in doc.paragraphs:
#     if '{{CompanyName}}' in para.text:
#         para.text = para.text.replace('{{CompanyName}}', epname)