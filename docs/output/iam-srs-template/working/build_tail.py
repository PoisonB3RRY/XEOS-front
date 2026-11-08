# ---------------------------------------------------------------- 收尾
para("")
para("说明：本文档依据内部业务方案、页面原型与《IAM 身份中心 API 参考》编制。接口路径、参数、分页规则与调用主体要求来自接口文档；页面布局与交互以原型截图为准，截图中未体现的分页、排序、筛选与批量上限配置等事项已在对应位置标注“待确认”，最终以需求方确认为准。", size=10.5)

# 让 Word 打开时更新目录域
settings = doc.settings.element
uf = settings.find(qn("w:updateFields"))
if uf is None:
    uf = OxmlElement("w:updateFields")
    settings.append(uf)
uf.set(qn("w:val"), "true")

os.makedirs(os.path.dirname(OUT), exist_ok=True)
doc.save(OUT)
print("saved:", OUT)
print("paragraphs:", len(doc.paragraphs), "tables:", len(doc.tables))
