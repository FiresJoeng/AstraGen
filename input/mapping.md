# 信贷报告填充映射表

### 基本信息

| 字段名称                                     | 占位符                           | 类型     | 信息源       |
|----------------------------------------------|----------------------------------|----------|--------------|
| 企业名称                                     | company_name                    | 字符串   | 免费公开信息 |
| 法定代表人                                   | legal_representative            | 字符串   | 免费公开信息 |
| 注册地址                                     | registered_address              | 字符串   | 免费公开信息 |
| 经营地址                                     | company_address                 | 字符串   | 免费公开信息 |
| 成立日期                                     | establishment_date               | 日期     | 免费公开信息 |
| 注册资本                                     | registered_capital              | 数值     | 免费公开信息 |
| 实缴资本                                     | paid_in_capital                 | 数值     | 免费公开信息 |
| 基本户开户行                                 | primary_account_bank            | 字符串   | 免费公开信息 |
| 企业类型                                     | company_type                    | 字符串   | 免费公开信息 |
| 国标行业                                     | industry                        | 字符串   | 免费公开信息 |
| 我行当年授信政策指引企业类型                 | current_year_credit_policy_guidance_enterprise_types | 字符串 | 未知 |
| 经营范围                                     | business_scope                  | 字符串   | 免费公开信息 |
| 资本金到位情况                               | fund_stats                      | 字符串   | 银行 |
| 股东情况介绍                                 | shareholders_info               | 字符串   | 付费查询信息 |
| 股权结构图                                   | equity_structure                | 图片文件 | 付费查询信息 |
| 个人品行及资信记录                           | personal_credit                 | 字符串   | 银行 |
| 公司治理                                     | corporate_governance            | 字符串   | 企业 |
| 历史沿革                                     | historical_evolution            | 字符串   | 企业 |
| 开发资质                                     | development_certification       | 字符串   | 银行 |

### 详细信息

##### 股东信息（shareholders）
| 字段名称     | 占位符            | 类型   | 信息源       |
|--------------|-------------------|--------|--------------|
| 股东名称     | shareholders[name]              | 字符串 | 免费公开信息 |
| 认缴资本     | shareholders[subscribed_capital] | 数值   | 免费公开信息 |
| 实缴资本     | shareholders[paid_in_capital]    | 数值   | 免费公开信息 |
| 持股比例     | shareholders[shareholding_ratio] | 百分比 | 免费公开信息 |
| 认缴日期     | shareholders[subscription_date]  | 日期   | 免费公开信息 |

##### 实际控制人（actual_controller）
| 字段名称         | 占位符  | 类型   | 信息源       |
|------------------|--------|--------|--------------|
| 实际控制人名称   | actual_controller[name]   | 字符串 | 免费公开信息 |
| 身份证号码       | actual_controller[id]     | 数值 | 付费查询信息 |

##### 实际控制人主要经历（actual_controller.main_experience）
| 字段名称 | 占位符  | 类型   | 信息源       |
|----------|--------|--------|--------------|
| 时间     | actual_controller[main_experience][time]   | 日期   | 付费查询信息 |
| 公司     | actual_controller[main_experience][company] | 字符串 | 付费查询信息 |
| 职务     | actual_controller[main_experience][position] | 字符串 | 付费查询信息 |

##### 关键人员（key_personnel）
| 字段名称 | 占位符 | 类型   | 信息源       |
|----------|------|--------|--------------|
| 姓名     | key_personnel[name] | 字符串 | 付费查询信息 |
