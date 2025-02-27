from docx import Document

template = ''
doc = Document(template)

def 填充占位符(替换字典):
    for para in doc.paragraphs:
        for 占位符, 替换值 in 替换字典.items():
            if 占位符 in para.text:
                para.text = para.text.replace(占位符, 替换值)

doc.save('filled_template.docx')
