from docx import Document

template = ''
doc = Document(template)

def 填充占位符(模板占位信息, 公司信息):
    for para in doc.paragraphs:
        if '{{CompanyName}}' in para.text:
            para.text = para.text.replace(f'{模板占位信息}', 公司信息)

doc.save('filled_template.docx')
