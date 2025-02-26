from docx import Document

template = ''
doc = Document(template)

def 填充占位符(替换字典):
    for para in doc.paragraphs:
        for 占位符, 替换值 in 替换字典.items():
            if 占位符 in para.text:
                para.text = para.text.replace(占位符, 替换值)

# 示例调用
替换字典 = {
    替换字典 = {
    '{{CompanyName}}': '某某公司',
    '{{legal representative}}': '张三',
    '{{RegisteredAddress}}': '北京市朝阳区XXX',
    '{{ActualOfficeAddress}}': '北京市海淀区XXX',
    '{{EstablishmentDate}}': '2005-11-15',
    '{{RegisteredCapital}}': '5000万元',
    '{{PaidInCapital}}': '5000万元',
    '{{BasicAccountBank}}': '中国银行XXX支行',
    '{{CompanyType}}': '有限责任公司',
    '{{Industry}}': '信息技术',
    '{{BusinessScope}}': '软件开发、技术咨询',
    '{{ShareholderInfo}}': '张三 60%，李四 40%',
    '{{ActualController}}': '王五',
    '{{IDNumber}}': '123456789012345678',
    '{{Experience}}': '1987.9-1989.12  XX公司  助理经理；\n'
                      '1990.1-1994.12  YY企业  副总经理；\n'
                      '1995.1-至今  ZZ集团  董事长',
    '{{BoardChairman}}': '赵六',
    '{{GeneralManager}}': '孙七',
    '{{DeputyGeneralManager}}': '周八',
    '{{FinancialDirector}}': '吴九',
    '{{EmployeeCount}}': '224',
    '{{EducationStructure}}': '本科及以上76人，高中107人',
    '{{HistoricalEvolution}}': '2005年成立，2010年股权变更...',
    '{{DevelopmentQualification}}': '一级资质（有效期至2030-12-31）',
    '{{AffiliatedCompany}}': 'XX科技有限公司',
    '{{TotalAssets}}': '2亿元',
    '{{NetAssets}}': '1.5亿元',
    '{{OperatingRevenue}}': '5亿元',
    '{{TotalProfit}}': '8000万元',
    '{{FinancingBalance}}': '3000万元'
}

    # 添加更多的占位符和替换值
}

填充占位符(替换字典)

doc.save('filled_template.docx')
