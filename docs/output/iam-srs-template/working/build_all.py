# -*- coding: utf-8 -*-
"""按浦发银行《IaaS研发需求 需求规格说明书》模板编排 IAM 存量用户组迁移文档。"""
import os
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_SECTION
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

OUT = r"C:/Users/nickj/GitRepo/XEOS-front/docs/output/iam-srs-template/stage3/IAM身份中心-存量用户组迁移-需求规格说明书_V1.0.docx"
SONG = "宋体"
ASCII_FONT = "Times New Roman"

# ---------------------------------------------------------------- 基础工具


def _rfonts(rpr, cn=SONG, latin=ASCII_FONT):
    rf = rpr.find(qn("w:rFonts"))
    if rf is None:
        rf = OxmlElement("w:rFonts")
        rpr.insert(0, rf)
    for a in ("w:asciiTheme", "w:hAnsiTheme", "w:eastAsiaTheme", "w:cstheme"):
        if rf.get(qn(a)) is not None:
            del rf.attrib[qn(a)]
    rf.set(qn("w:ascii"), latin)
    rf.set(qn("w:hAnsi"), latin)
    rf.set(qn("w:eastAsia"), cn)
    rf.set(qn("w:cs"), latin)


def fmt_run(run, size=12, bold=False, cn=SONG, latin=ASCII_FONT, color=None, italic=False):
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    if color is not None:
        run.font.color.rgb = color
    _rfonts(run._element.get_or_add_rPr(), cn, latin)
    return run


def indent_chars(p, first=200, left=0, hanging=0):
    """按字符设置缩进（first/left/hanging 单位为 1/100 字符）"""
    if left or hanging:
        p.paragraph_format.left_indent = Pt(12 * (left or hanging) / 100.0)
    if first:
        p.paragraph_format.first_line_indent = Pt(12 * first / 100.0)
    if hanging:
        p.paragraph_format.first_line_indent = Pt(-12 * hanging / 100.0)
    pPr = p._p.get_or_add_pPr()
    ind = pPr.find(qn("w:ind"))
    if ind is None:
        return
    if first:
        ind.set(qn("w:firstLineChars"), str(first))
    if left:
        ind.set(qn("w:leftChars"), str(left))
    if hanging:
        ind.set(qn("w:hangingChars"), str(hanging))


def field_chars(p, instr, placeholder="", size=10.5):
    """在段落中插入一个域（begin/instr/separate/result/end）"""
    def _run():
        r = p.add_run()
        fmt_run(r, size=size)
        return r

    r1 = _run()
    fc = OxmlElement("w:fldChar")
    fc.set(qn("w:fldCharType"), "begin")
    fc.set(qn("w:dirty"), "true")
    r1._r.append(fc)

    r2 = _run()
    it = OxmlElement("w:instrText")
    it.set(qn("xml:space"), "preserve")
    it.text = " %s " % instr
    r2._r.append(it)

    r3 = _run()
    sep = OxmlElement("w:fldChar")
    sep.set(qn("w:fldCharType"), "separate")
    r3._r.append(sep)

    r4 = _run()
    t = OxmlElement("w:t")
    t.text = placeholder
    t.set(qn("xml:space"), "preserve")
    r4._r.append(t)

    r5 = _run()
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    r5._r.append(end)


def set_cell_borders(cell, sz=4, color="000000"):
    tcPr = cell._tc.get_or_add_tcPr()
    borders = OxmlElement("w:tcBorders")
    for edge in ("top", "left", "bottom", "right"):
        e = OxmlElement("w:" + edge)
        e.set(qn("w:val"), "single")
        e.set(qn("w:sz"), str(sz))
        e.set(qn("w:space"), "0")
        e.set(qn("w:color"), color)
        borders.append(e)
    tcPr.append(borders)


def set_table_borders(table, sz=4, color="000000"):
    tblPr = table._tbl.tblPr
    old = tblPr.find(qn("w:tblBorders"))
    if old is not None:
        tblPr.remove(old)
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        e = OxmlElement("w:" + edge)
        e.set(qn("w:val"), "single")
        e.set(qn("w:sz"), str(sz))
        e.set(qn("w:space"), "0")
        e.set(qn("w:color"), color)
        borders.append(e)
    tblPr.append(borders)


def shade(cell, fill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    tcPr.append(shd)


def cell_text(cell, text, bold=False, size=10.5, align="left", color=None):
    cell.text = ""
    p = cell.paragraphs[0]
    p.alignment = {"left": WD_ALIGN_PARAGRAPH.LEFT,
                   "center": WD_ALIGN_PARAGRAPH.CENTER,
                   "right": WD_ALIGN_PARAGRAPH.RIGHT}[align]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
    fmt_run(p.add_run(text), size=size, bold=bold, color=color)
    tcPr = cell._tc.get_or_add_tcPr()
    va = OxmlElement("w:vAlign")
    va.set(qn("w:val"), "center")
    tcPr.append(va)


def add_table(doc, header, rows, widths, header_fill="D9D9D9", font_size=10.5, aligns=None):
    t = doc.add_table(rows=1, cols=len(header))
    t.alignment = WD_TABLE_ALIGNMENT.LEFT
    t.autofit = False
    tblPr = t._tbl.tblPr
    layout = OxmlElement("w:tblLayout")
    layout.set(qn("w:type"), "fixed")
    tblPr.append(layout)
    tblInd = OxmlElement("w:tblInd")
    tblInd.set(qn("w:w"), "108")
    tblInd.set(qn("w:type"), "dxa")
    tblPr.append(tblInd)
    set_table_borders(t, sz=4, color="000000")
    if aligns is None:
        aligns = ["center"] + ["left"] * (len(header) - 1)

    hdr = t.rows[0]
    trPr = hdr._tr.get_or_add_trPr()
    th = OxmlElement("w:tblHeader")
    trPr.append(th)
    trPr.append(OxmlElement("w:cantSplit"))
    for i, h in enumerate(header):
        c = hdr.cells[i]
        c.width = widths[i]
        cell_text(c, h, bold=True, size=font_size, align="center")
        shade(c, header_fill)
        for _p in c.paragraphs:          # 表头不得与首行数据分页
            _p.paragraph_format.keep_with_next = True

    for row in rows:
        _r = t.add_row()
        _r._tr.get_or_add_trPr().append(OxmlElement("w:cantSplit"))
        cells = _r.cells
        for i, v in enumerate(row):
            cells[i].width = widths[i]
            cell_text(cells[i], str(v), size=font_size, align=aligns[i])
    # 表格后补一个小间距段
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 0.6
    fmt_run(p.add_run(""), size=6)
    return t


# ---------------------------------------------------------------- 文档骨架

doc = Document()
sec = doc.sections[0]
sec.page_width, sec.page_height = Cm(21), Cm(29.7)
sec.top_margin, sec.bottom_margin = Cm(2.54), Cm(2.54)
sec.left_margin, sec.right_margin = Cm(3.0), Cm(3.0)
sec.header_distance, sec.footer_distance = Cm(1.35), Cm(1.75)
CONTENT_W = Cm(15.0)

normal = doc.styles["Normal"]
normal.font.size = Pt(12)
normal.font.name = ASCII_FONT
_rfonts(normal.element.get_or_add_rPr())
normal.paragraph_format.line_spacing = 1.5
normal.paragraph_format.space_before = Pt(0)
normal.paragraph_format.space_after = Pt(0)
normal.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY


def style_heading(name, size, before=12, after=6, bold=True):
    st = doc.styles[name]
    st.font.size = Pt(size)
    st.font.bold = bold
    st.font.color.rgb = RGBColor(0, 0, 0)
    _rfonts(st.element.get_or_add_rPr())
    pf = st.paragraph_format
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    pf.line_spacing = 1.5
    pf.keep_with_next = True
    pf.first_line_indent = Pt(0)
    pf.alignment = WD_ALIGN_PARAGRAPH.LEFT


style_heading("Heading 1", 16, before=18, after=10)
style_heading("Heading 2", 14, before=14, after=8)
style_heading("Heading 3", 12, before=10, after=6)
style_heading("Heading 4", 12, before=8, after=4)


def h(text, level):
    p = doc.add_paragraph(text, style="Heading %d" % level)
    return p


def para(text, first=200, size=12, bold=False, align="justify", space_after=0, space_before=0):
    p = doc.add_paragraph()
    p.alignment = {"justify": WD_ALIGN_PARAGRAPH.JUSTIFY,
                   "left": WD_ALIGN_PARAGRAPH.LEFT,
                   "center": WD_ALIGN_PARAGRAPH.CENTER}[align]
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.5
    if first:
        indent_chars(p, first=first)
    else:
        p.paragraph_format.first_line_indent = Pt(0)
    fmt_run(p.add_run(text), size=size, bold=bold)
    return p


def lead(label, text, size=12):
    """'需求背景：' 这类领起段"""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 1.5
    indent_chars(p, first=200)
    fmt_run(p.add_run(label), size=size, bold=True)
    fmt_run(p.add_run(text), size=size)
    return p


def steps(items, size=12):
    for i, it in enumerate(items, 1):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        indent_chars(p, left=200, hanging=200)
        fmt_run(p.add_run("%d、%s" % (i, it)), size=size)


def bullets(items, size=12, mark="●", indent=200):
    for it in items:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        indent_chars(p, left=indent + 100, hanging=100)
        fmt_run(p.add_run(mark + " "), size=size - 2)
        if isinstance(it, tuple):
            fmt_run(p.add_run(it[0]), size=size, bold=True)
            fmt_run(p.add_run(it[1]), size=size)
        else:
            fmt_run(p.add_run(it), size=size)


def page_break():
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    r = p.add_run()
    fmt_run(r, size=1)
    br = OxmlElement("w:br")
    br.set(qn("w:type"), "page")
    r._r.append(br)


# ---------------------------------------------------------------- 页眉 / 页脚


def build_header(header):
    header.is_linked_to_previous = False
    # 清空已有段落内容
    for p in list(header.paragraphs):
        p._p.getparent().remove(p._p)
    t = header.add_table(rows=1, cols=2, width=CONTENT_W)
    t.autofit = False
    tblPr = t._tbl.tblPr
    layout = OxmlElement("w:tblLayout")
    layout.set(qn("w:type"), "fixed")
    tblPr.append(layout)
    tblInd = OxmlElement("w:tblInd")
    tblInd.set(qn("w:w"), "108")
    tblInd.set(qn("w:type"), "dxa")
    tblPr.append(tblInd)
    set_table_borders(t, sz=4, color="808080")
    left, right = t.rows[0].cells
    left.width = Cm(6.2)
    right.width = Cm(8.8)
    trPr = t.rows[0]._tr.get_or_add_trPr()
    trHeight = OxmlElement("w:trHeight")
    trHeight.set(qn("w:val"), "560")
    trHeight.set(qn("w:hRule"), "atLeast")
    trPr.append(trHeight)

    left.text = ""
    p = left.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.0
    fmt_run(p.add_run("浦发银行"), size=13, bold=True, color=RGBColor(0x44, 0x54, 0x6A))
    fmt_run(p.add_run("  SPD BANK"), size=8, bold=True, color=RGBColor(0x44, 0x54, 0x6A))
    right.text = ""
    p2 = right.paragraphs[0]
    p2.paragraph_format.space_before = Pt(0)
    p2.paragraph_format.space_after = Pt(0)
    fmt_run(p2.add_run(""), size=8)

    # 表后留空白段落（Word 要求）
    tail = header.add_paragraph()
    tail.paragraph_format.space_before = Pt(0)
    tail.paragraph_format.space_after = Pt(0)
    tail.paragraph_format.line_spacing = Pt(6)
    fmt_run(tail.add_run(""), size=1)


def build_footer(footer):
    footer.is_linked_to_previous = False
    for p in list(footer.paragraphs):
        p._p.getparent().remove(p._p)
    p = footer.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    field_chars(p, "PAGE", "1", size=10)


sec.different_first_page_header_footer = True
build_header(sec.header)
build_footer(sec.footer)
# 首页页眉与正文一致，首页无页码
build_header(sec.first_page_header)
if sec.first_page_footer is not None:
    sec.first_page_footer.is_linked_to_previous = False
    for p in list(sec.first_page_footer.paragraphs):
        p._p.getparent().remove(p._p)
    sec.first_page_footer.add_paragraph()

# ---------------------------------------------------------------- 封面


def cover_line(text, size, after=0, before=0):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(before)
    p.paragraph_format.space_after = Pt(after)
    p.paragraph_format.line_spacing = 1.2
    pPr = p._p.get_or_add_pPr()
    for tag in ("w:autoSpaceDE", "w:autoSpaceDN"):
        e = OxmlElement(tag)
        e.set(qn("w:val"), "0")
        pPr.insert_element_before(e, "w:bidi", "w:adjustRightInd", "w:snapToGrid",
                                  "w:spacing", "w:ind", "w:contextualSpacing",
                                  "w:mirrorIndents", "w:suppressOverlap", "w:jc",
                                  "w:textDirection", "w:textAlignment",
                                  "w:textboxTightWrap", "w:outlineLvl", "w:divId",
                                  "w:cnfStyle", "w:rPr", "w:sectPr")
    fmt_run(p.add_run(text), size=size, bold=True)
    return p


for _ in range(21):
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.0
    fmt_run(p.add_run(""), size=12)

cover_line("上海浦东发展银行", 28, after=26)
cover_line("IaaS研发需求", 26, after=20)
cover_line("需求规格说明书", 26, after=14)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.line_spacing = 1.2
p.paragraph_format.space_before = Pt(4)
p.paragraph_format.space_after = Pt(34)
fmt_run(p.add_run("（华为云 IAM 身份中心存量用户组迁移）"), size=15)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.line_spacing = 1.2
fmt_run(p.add_run("V1.0"), size=15)

page_break()

# ---------------------------------------------------------------- 文档编排规范及约定

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(6)
p.paragraph_format.space_after = Pt(18)
fmt_run(p.add_run("文档编排规范及约定"), size=16, bold=True)

rules = [
    "【文档编排规范及约定】的内容仅是对本文档编写的规范和约定进行描述，文档编写人员须严格按照本规范和约定进行编写，在文档正式发布时删除该部分内容；",
    "须填写“文档修订控制记录”；",
    "文档目录须更新为最新的，与实际内容相对应。",
]
for i, r in enumerate(rules, 1):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 1.5
    indent_chars(p, left=200, hanging=200)
    fmt_run(p.add_run("%d．%s" % (i, r)), size=12)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.LEFT
p.paragraph_format.space_before = Pt(24)
p.paragraph_format.space_after = Pt(8)
fmt_run(p.add_run("文档修订控制记录"), size=12, bold=True)

add_table(
    doc,
    ["序号", "修订内容", "修订日期", "版本号", "修订人", "审核人"],
    [["1", "创建全文", "2026-11-08", "V1.0", "", ""]],
    [Cm(1.5), Cm(6.0), Cm(2.8), Cm(1.8), Cm(1.45), Cm(1.45)],
    aligns=["center"] * 6,
)

page_break()

# ---------------------------------------------------------------- 目录

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(6)
p.paragraph_format.space_after = Pt(16)
fmt_run(p.add_run("目　　录"), size=16, bold=True)

toc_p = doc.add_paragraph()
toc_p.paragraph_format.line_spacing = 1.5
field_chars(toc_p, 'TOC \\o "1-4" \\h \\z \\u', "（请在 Word/WPS 中按 F9 或右键“更新域”生成目录）", size=12)

page_break()
# -*- coding: utf-8 -*-
# 正文部分：1 引言 / 2 产品功能（按页面原型改写）
import os
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

IMGDIR = r"C:/Users/nickj/GitRepo/XEOS-front/docs/output/iam-srs-template/working/img"


def figure(name, caption, width_cm=12.0):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.first_line_indent = Pt(0)
    p.paragraph_format.keep_with_next = True
    run = p.add_run()
    run.add_picture(os.path.join(IMGDIR, name), width=Cm(width_cm))
    try:
        pic = run._r.xpath(".//pic:pic")[0]
        spPr = pic.find(qn("pic:spPr"))
        ln = OxmlElement("a:ln")
        ln.set("w", "9525")
        solid = OxmlElement("a:solidFill")
        clr = OxmlElement("a:srgbClr")
        clr.set("val", "BFBFBF")
        solid.append(clr)
        ln.append(solid)
        spPr.append(ln)
    except Exception as e:
        print("border skip:", e)
    cap = doc.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.paragraph_format.space_before = Pt(2)
    cap.paragraph_format.space_after = Pt(10)
    cap.paragraph_format.line_spacing = 1.0
    cap.paragraph_format.first_line_indent = Pt(0)
    fmt_run(cap.add_run(caption), size=10.5)
    return cap


def ui_table(rows):
    return add_table(doc, ["界面元素", "说明与交互要求"], rows,
                     [Cm(3.8), Cm(11.2)], aligns=["left", "left"], font_size=10)


# ================================================================ 1 引言
h("1 引言", 1)

h("1.1 编写目的", 2)
para("本文档将业务侧已确认的《存量用户组迁移方案（IAM 身份中心）》与云管理平台 OBS 用户组管理的页面原型转化为可开发、可测试、可验收的需求规格，明确功能边界、页面交互、接口依赖、执行顺序约束与验收口径，作为研发实现、测试用例设计与上线验收的共同依据。本文档只描述需求，不描述具体实现方法。")

h("1.1.1 作用", 3)
para("实现需求方与研发方的双向沟通，形成需求基线，为下一阶段的概要设计提供依据。需求方提出变更时，通过需求变更流程处理，变更结果以本文档的修订记录为准。")

h("1.1.2 预期读者", 3)
para("云平台运维团队、IaaS 研发团队、前端与后端开发人员、测试团队，以及参与迁移方案审批的安全合规团队。")

h("1.1.3 需求提出者", 3)
para("安全合规团队（存量权限收敛要求的提出方）；云平台运维团队（迁移执行与结果确认方）。")

h("1.1.4 需求承接者及实施者", 3)
para("需求分析方：云平台运维团队。")
para("需求实施方：IaaS 研发团队（页面与后端接口研发）、云平台运维团队（执行、核对与验收）。")

h("1.1.5 使用者", 3)
para("云平台运维工程师（执行迁移操作）、安全合规审核人员（核对迁移结果）、测试人员（验证页面交互与异常处置）。")

h("1.2 术语定义", 2)
add_table(
    doc,
    ["术语", "说明"],
    [
        ["OBS", "对象存储服务。本需求中，OBS 用户的权限通过其所属用户组继承获得"],
        ["IAM 身份中心", "华为云统一身份管理服务，集中管理用户、用户组及其成员关系"],
        ["多云服务", "公司与云侧之间的统一接入层，业务侧统一经其调用华为云接口；Region、Endpoint、服务委托管理员凭据与限流策略均在该服务内完成，业务侧无需感知"],
        ["身份源（Identity Store）", "用户与用户组数据的容器，由 identity_store_id 唯一标识，长度固定 12 位"],
        ["用户组（Group）", "权限的集合载体，用户加入用户组后即继承该组的全部权限"],
        ["成员关系（Membership）", "“用户—用户组”的绑定记录，由 membership_id 唯一标识"],
        ["原用户组（旧组）", "存量用户当前所属、待解除绑定的用户组，如 obs-group-readonly"],
        ["目标用户组", "存量用户迁入后应归属的用户组，下文简称目标组"],
        ["迁入", "页面操作术语：为用户建立与目标用户组的成员关系，对应“加入用户组”"],
        ["退出", "页面操作术语：解除用户与原用户组的成员关系，对应“退出用户组”"],
        ["资源组织", "用户所属的业务组织，在列表中用于区分用户归属"],
        ["幂等", "同一操作重复执行不产生额外副作用，重复加入、重复退出均视为成功"],
        ["权限空档", "用户已退出原组但尚未加入目标组的状态，此时用户不具备任何一组的权限"],
    ],
    [Cm(4.6), Cm(10.4)],
    aligns=["left", "left"],
)

h("1.3 参考资料", 2)
add_table(
    doc,
    ["序号", "名称", "来源", "版本或日期"],
    [
        ["1", "《存量用户组迁移方案（IAM 身份中心）》", "内部业务文档", "2026-11-08"],
        ["2", "《IAM 身份中心 API 参考》", "华为云", "文档版本 02，2025-12-19"],
        ["3", "OBS 用户组管理页面原型（列表页、勾选态、详情/加入/退出/批量迁入弹窗）", "需求方提供", "2026-11-08"],
    ],
    [Cm(1.4), Cm(7.4), Cm(3.2), Cm(3.0)],
    aligns=["center", "left", "left", "left"],
)

# ================================================================ 2 产品功能
h("2 产品功能", 1)

para("本需求在云管理平台的存储服务下新增 OBS 用户组管理能力，以页面方式承载存量用户从原用户组到目标用户组的迁移：运维人员在列表页查看 OBS 用户及其当前所属用户组，对单个用户执行加入或退出操作，也可勾选多个用户执行批量迁入。页面背后的写操作仍通过华为云 IAM 身份中心的成员关系接口完成——业务侧已完成接口可行性验证，只需 4 个开放接口，即可拆分为“加入目标组”与“退出原组”两个相互独立的写操作。")
para("权限收敛的必要性在于：现有 OBS 用户的权限通过原用户组继承获得，其中包含业务上已不再需要的权限（例如对象存储的列举类权限）。仅把用户加入目标组并不会自动剥离原组权限，必须显式退出原组，收敛才真正生效；而在退出之前必须先加入目标组，否则用户会在操作窗口内失去全部权限。因此页面上的操作顺序固定为“先加入目标组、再退出原组”。")
para("本需求包含以下四个功能点：")
steps([
    "OBS 用户组管理列表页：集中展示 OBS 用户及其当前所属用户组，提供详情查看、单个加入/退出与勾选批量迁入的统一入口；",
    "存量单个用户加入目标用户组：以弹窗方式为单个用户选择目标用户组并完成加入；",
    "存量单个用户退出原用户组：以弹窗方式列出该用户全部所属用户组，勾选后完成退出；",
    "存量用户批量迁入目标用户组：对勾选的多个用户（单次最多 10 个）统一迁入同一目标用户组并汇总结果。",
])
para("本次不包含以下内容：目标用户组的创建与权限策略配置（作为前置条件，由权限管理流程预先完成）；OBS 用户的开户与身份源创建；批量退出用户组（批量操作仅支持迁入，退出在单个用户弹窗内完成）；迁移结果的自动校验抽查（不调用成员关系校验类接口）；失败操作的自动回滚。")

# ---------------------------------------------------------------- 2.1 列表页
h("2.1 OBS 用户组管理列表页", 2)

h("2.1.1 需求背景和目标（必须）", 3)
lead("需求背景：", "存量 OBS 用户的权限通过原用户组继承，其中包含已不再需要的权限项，需要按用户逐一收敛。当前平台没有 OBS 用户与用户组的集中视图，运维只能在 IAM 控制台按用户逐个查询，既无法快速判断“谁在哪个组”，也无法在不跳转系统的前提下完成迁组操作，迁移过程难以复核。为此需要在云管理平台的存储服务下新增 OBS 用户组管理页面。")
lead("需求目标：", "提供 OBS 用户的集中列表视图，展示用户名、当前所属用户组、资源组织与区域；提供查看所属用户组详情、单个用户加入/退出、勾选多个用户批量迁入的入口；对勾选数量设置上限（单次最多 10 个用户），把误操作的影响面控制在可接受范围。")
lead("目标用户：", "云平台运维工程师（主用户）；安全合规人员（按列表与详情核对迁移结果）。")

h("2.1.2 功能需求", 3)
h("2.1.2.1 功能的使用场景", 4)
para("运维人员收到权限收敛任务后，进入“存储服务—OBS用户组管理”，按用户名检索目标用户，先点“详情”确认其当前所属用户组（例如 obs-group-readonly），再决定对该用户执行“加入用户组”或“退出用户组”；若需成批处理，则勾选多个用户后点击“批量迁入”统一选择目标组。整个过程在同一个页面内完成，不需要跳转 IAM 控制台。")

h("2.1.2.2 UI界面（必须）", 4)
para("页面整体布局见图 1：左侧为平台导航，工作区打开“OBS用户组管理”页签，页内包含工具栏（批量迁入按钮、勾选上限提示、用户搜索）与用户列表。勾选多个用户后的状态见图 2；点击“当前用户组”列的“详情”，打开用户所属用户组详情弹窗（图 3）。")
figure("fig1_list.png", "图 1　OBS 用户组管理列表页", 15)
figure("fig2_checked.png", "图 2　列表页勾选多个用户后的状态（按钮文案随勾选数量变化）", 15)
figure("fig3_groups_detail.png", "图 3　用户所属用户组详情弹窗", 12)
para("界面元素与交互要求见下表。")
ui_table([
    ["导航入口", "位于左侧“存储服务”下，与“OBS租户”等同级；点击后在工作区打开“OBS用户组管理”页签，页签可关闭并返回首页"],
    ["页签标题", "OBS用户组管理"],
    ["批量迁入按钮", "工具栏左侧主按钮，文案随勾选数量变化：“批量迁入（已选 0/10）”→“批量迁入（已选 4/10）”；未勾选任何用户时置灰不可点击"],
    ["勾选上限提示", "按钮右侧固定提示“单次最多勾选 10 个用户”；达到上限后其余行的复选框不可再勾选"],
    ["搜索框", "工具栏右侧，占位文案“按用户名筛选，回车查询”；回车触发查询，清空关键字后回车恢复全量"],
    ["列表列", "依次为：复选框（表头为全选）、用户名、当前用户组、资源组织、区域、操作"],
    ["当前用户组列", "统一显示“详情”文字链接，点击打开用户所属用户组详情弹窗；不在列表内直接展开组名（单个用户可能属于多个组）"],
    ["操作列", "提供“加入用户组”（链接色）与“退出用户组”（警示红色）两个文字链接；用户当前无所属用户组时，“退出用户组”置灰不可点击"],
    ["选中态", "勾选行显示浅蓝色背景，与未选中行区分；表头复选框支持全选/取消全选，部分勾选时显示半选态"],
    ["详情弹窗", "标题“用户所属用户组详情”；信息条展示“用户”“资源组织”“已加入组数量”；下方“所属用户组”区域以标签形式列出全部组名，只读，仅提供“关闭”按钮"],
])

h("2.1.2.3 功能核心点描述（必须）", 4)
steps([
    "页面入口与加载：从“存储服务—OBS用户组管理”进入，页面加载 OBS 用户清单；加载中显示加载态，加载失败给出错误提示与“重试”入口，不得以空列表代替失败态。",
    "列表字段：展示用户名、当前用户组、资源组织、区域四项信息；用户名与资源组织直接显示文本，“当前用户组”显示“详情”链接，“区域”显示所在地域（如“上海”）。",
    "搜索：在搜索框输入用户名后回车，按用户名筛选列表；结果为空时显示空态文案，清空关键字后回车恢复全量。",
    "勾选与计数：勾选行首复选框后，工具栏按钮文案中的已选数量实时加一；达到 10 个后其余复选框禁用，并提示“单次最多勾选 10 个用户”；点击表头复选框可全选或取消全选。",
    "查看所属用户组：点击任意行“详情”，打开弹窗展示该用户的用户名、资源组织、已加入组数量与全部所属用户组标签；标签数量与“已加入组数量”一致；无所属组时数量为 0 并显示空态提示。",
    "单个操作入口：点击“加入用户组”打开加入弹窗（见 2.2），点击“退出用户组”打开退出弹窗（见 2.3）；两个弹窗均自动带入该行用户，不需要二次选择用户。",
    "批量操作入口：勾选用户后点击“批量迁入（已选 N/10）”打开批量迁入弹窗（见 2.4），弹窗中的待迁入用户与本页勾选结果一致。",
    "操作后刷新：加入、退出、批量迁入成功后，列表与详情弹窗的数据同步刷新，运维无需手动刷新页面即可核验结果。",
])

h("2.1.2.4 成功的标准（必须）", 4)
bullets([
    "运维可在单一页面完成“查用户—看所属组—迁组”的全流程，不需要跳转 IAM 控制台。",
    "列表完整展示用户名、当前用户组、资源组织、区域四项字段，1366×768 及以上分辨率下页面无横向滚动。",
    "勾选数量、按钮文案与上限提示三者一致；勾选第 11 个用户时被拦截并给出提示。",
    "详情弹窗展示的组数量与标签个数一致，且与该用户实际的成员关系一致。",
    "当前无所属用户组的用户，“退出用户组”链接呈禁用态且不可点击。",
])

h("2.1.2.5 异常处置标准和风险考虑（按需）", 4)
para("列表页本身不产生写操作，异常处置原则是“状态可见、原因可查”，不出现静默失败。")
bullets([
    ("列表加载失败：", "展示错误提示与重试按钮，不展示空列表，避免被误认为“已无用户”。"),
    ("搜索无结果：", "显示空态文案并保留搜索关键字，便于修正后重新查询。"),
    ("用户无所属用户组：", "详情弹窗显示“已加入组数量 0”并给出空态提示，该行“退出用户组”置灰。"),
    ("数据同步延迟：", "若列表数据来自平台缓存，可能与 IAM 实际不一致，以详情弹窗的查询结果为准（数据来源与刷新机制待确认）。"),
])
para("风险考虑：")
bullets([
    "列表页同时提供“加入”与“退出”入口，其中退出是不可逆的权限收回操作，须通过弹窗二次确认（见 2.3），并对无所属组的用户禁用退出入口。",
    "一次误勾选会影响多个用户，因此设置单次上限 10 个，并在批量弹窗中回显待迁入用户清单供核对。",
    "页面文案使用“迁入”而非“迁移”，避免运维误以为批量迁入即完成整项迁移（原组权限并未剥离）。",
])
para("待确认事项：")
bullets([
    "列表数据来源（实时查询 IAM 或平台侧缓存）与刷新机制。",
    "列表是否分页、每页条数以及默认排序规则（原型未体现）。",
    "是否支持按资源组织、区域筛选，以及“区域”列在多地域场景下的取值口径。",
])

h("2.1.3 非功能需求（按需）", 3)
bullets([
    ("性能要求：", "列表首屏加载不超过 3 秒（数据量以实际用户规模为准）；搜索、勾选、打开详情弹窗的响应不超过 1 秒。"),
    ("易用性要求：", "主按钮、禁用态与危险操作（退出）在颜色与文案上可区分；禁用态能说明原因（未勾选用户、未选择目标组等）。"),
    ("安全要求：", "页面入口仅对具备 OBS 用户管理权限的角色可见；所有写操作记录操作人、时间、目标用户与结果。"),
    ("兼容性要求：", "支持 Chrome、Edge 主流版本，最小分辨率 1366×768。"),
])

h("2.1.4 需求优先级（必须）", 3)
bullets([("优先级分类：", "高优先。列表页是其余三个功能点的唯一入口，缺失则迁移无法在平台上完成。")])
bullets([("预期上线时间：", "")])
bullets([
    "重保环境上线时间：待排期确认（建议 2026/12/15）",
    "生产环境上线时间：待排期确认（建议 2027/01/31）",
], mark="○", indent=400)

# ---------------------------------------------------------------- 2.2 单个用户加入
h("2.2 存量单个用户加入目标用户组", 2)

h("2.2.1 需求背景和目标（必须）", 3)
lead("需求背景：", "用户在列表页可以看到自己当前所属的用户组，但要完成“先加后减”，还需要能为单个用户指定目标用户组并建立成员关系。原组权限在退出后立即失效，若目标组关系尚未建立，用户会在窗口内同时不具备新旧两组权限（即权限空档），直接影响业务连续性。因此加入操作必须可以单独执行，且在执行顺序上先于退出。")
lead("需求目标：", "以弹窗方式为单个用户选择目标用户组并完成加入：弹窗内清楚展示目标用户与其当前所属组，避免迁错人；目标组从下拉列表中选择，避免手工输入组名出错；加入成功后即时反馈并刷新列表。")
lead("目标用户：", "云平台运维工程师（执行人）；安全合规人员（按详情核对结果）。")

h("2.2.2 功能需求", 3)
h("2.2.2.1 功能的使用场景", 4)
para("运维人员在列表页定位到某用户（如 li01），点击该行“加入用户组”，弹窗顶部显示“目标用户：li01｜当前所属组：obs-group-readonly”，运维在“选择目标用户组”下拉中选定目标组后点击“确认加入”；弹窗关闭并提示加入成功，再次打开该用户的详情，可看到新组已出现在所属用户组列表中，已加入组数量随之增加。")

h("2.2.2.2 UI界面（必须）", 4)
para("加入用户组弹窗见图 4，界面元素与交互要求见下表。")
figure("fig4_join.png", "图 4　单个用户加入用户组弹窗", 12)
ui_table([
    ["弹窗标题", "“加入用户组”；右上角提供关闭按钮（×），关闭等同于取消"],
    ["信息条", "只读展示“目标用户”与“当前所属组”：目标用户由列表行带入，不可修改；当前所属组以标签形式展示用户现有的全部组，无组时显示“无”"],
    ["目标用户组", "必填项（标红星），下拉单选，占位文案“请选择要加入的目标用户组”；候选为身份中心内已存在的用户组，按组名展示"],
    ["主按钮", "“确认加入”；未选择目标用户组时置灰不可点击；提交中显示加载态并禁止重复点击"],
    ["次按钮", "“取消”，关闭弹窗且不产生任何变更"],
])

h("2.2.2.3 功能核心点描述（必须）", 4)
steps([
    "打开弹窗：由列表行“加入用户组”触发，目标用户与该用户当前所属组自动带入；当前所属组通过查询该用户的成员关系实时获得，不依赖列表缓存。",
    "目标组候选：下拉候选来自 ListGroups（同一身份源内的用户组），选定后以 group_id 作为绑定目标，不再依赖组名匹配；若存在同名组，候选需提供可区分信息（如组 ID 尾段），避免误选。",
    "提交前校验：未选择目标用户组时“确认加入”置灰；选择后按钮可点击，并在提交前回显所选组名供二次确认。",
    "提交：调用 CreateGroupMembership，请求携带 group_id、member_id.user_id 与 identity_store_id；返回 membership_id 即判定加入成功，弹窗关闭并给出成功提示。",
    "幂等处理：若用户已在该组中（接口返回 409），按成功处理，提示“该用户已在该组中”，不重复建立关系、不报错。",
    "失败处理：参数非法、身份源不匹配、目标组不存在、无权限、登录失效等，按错误原因给出可读提示，弹窗保持打开以便修正后重试；网络超时或服务异常提示“操作失败，请重试”，由用户确认后重试（操作幂等，重复提交安全）。",
    "结果同步：加入成功后刷新列表的当前用户组数据；再次打开详情弹窗应能看到新组，已加入组数量同步加一。",
])

h("2.2.2.4 成功的标准（必须）", 4)
bullets([
    "弹窗能准确显示目标用户与其当前所属组（多个组并列展示，无组时显示“无”）。",
    "未选择目标用户组时“确认加入”不可点击。",
    "选择目标组并确认后提示加入成功，详情弹窗中新组出现且已加入组数量加一。",
    "对已在该组的用户重复执行，提示“已在该组中”，不产生重复成员关系。",
    "单个用户加入失败不影响页面其他功能，修正后可再次提交。",
])

h("2.2.2.5 异常处置标准和风险考虑（按需）", 4)
para("加入是“只增不减”的安全操作，异常处置原则是“可读提示、可重试、不重复”。")
bullets([
    ("目标组在提交前被删除：", "接口返回资源不存在，提示“目标组已不存在，请刷新后重新选择”，不自动重试。"),
    ("身份源不匹配：", "提示“用户与目标用户组不属于同一身份源”，不重试，需人工核对数据归属。"),
    ("无操作权限（403）或登录失效（401）：", "提示对应原因；401 引导重新登录，403 提示联系权限管理员。"),
    ("网络超时或服务异常（5xx）：", "提示“操作失败，请重试”；操作本身幂等，重复提交不会产生重复关系。"),
])
para("风险考虑：")
bullets([
    "误选目标组会把用户加入错误的组，造成权限扩大；因此弹窗信息条必须回显“目标用户 + 当前所属组”，并在提交前展示所选组名。",
    "加入完成后用户同时拥有新旧两组权限（权限叠加），这是设计预期，不会中断业务，但迁移尚未完成，须继续执行退出原组（见 2.3）。",
])
para("待确认事项：")
bullets([
    "目标用户组数量较多时，下拉是否需要支持按组名搜索。",
    "同名用户组在下拉中的区分方式（展示组 ID 或资源组织）。",
])

h("2.2.3 非功能需求（按需）", 3)
bullets([
    ("性能要求：", "打开弹窗并加载当前所属组不超过 2 秒；提交加入请求的响应时间以接口为准，前端超时设置不超过 15 秒。"),
    ("安全要求：", "仅具备 OBS 用户管理权限的角色可执行；写操作记录操作人、目标用户、目标组、结果与请求标识。"),
    ("可靠性要求：", "加入操作幂等，重复提交不产生重复成员关系。"),
])

h("2.2.4 需求优先级（必须）", 3)
bullets([("优先级分类：", "高优先。本功能点是避免权限空档的唯一手段，缺失则不能执行退出原组，迁移不可实施。")])
bullets([("预期上线时间：", "")])
bullets([
    "重保环境上线时间：待排期确认（建议 2026/12/15）",
    "生产环境上线时间：待排期确认（建议 2027/01/31）",
], mark="○", indent=400)

# ---------------------------------------------------------------- 2.3 单个用户退出
h("2.3 存量单个用户退出原用户组", 2)

h("2.3.1 需求背景和目标（必须）", 3)
lead("需求背景：", "用户加入目标组之后，原用户组中仍保留其成员关系，原组继承的冗余权限尚未剥离，权限收敛目标未达成。华为云接口不支持按“用户 + 用户组”直接删除成员关系，退出所需的 membership_id 只能从“列出用户加入的组”的查询结果中获得，因此退出必须以“查询—勾选—确认”的方式完成，不能由运维直接输入组名。")
lead("需求目标：", "以弹窗方式列出单个用户的全部所属用户组，运维勾选需要退出的组后一次提交完成退出；支持一次退出多个组（例如同时清理旧组与临时组）；退出成功后列表与详情同步刷新，并在结果中明确成功与失败数量。")
lead("目标用户：", "云平台运维工程师（执行人）；安全合规人员（按记录核对）。")

h("2.3.2 功能需求", 3)
h("2.3.2.1 功能的使用场景", 4)
para("运维人员确认某用户已加入目标组后，点击该行“退出用户组”，弹窗列出该用户当前所属的全部用户组（如 obs-group-readonly）；勾选需要退出的组，底部计数与按钮文案随勾选数量变化，点击“确认退出选中的 1 个用户组”后完成退出；再次打开该用户的详情，该组已不在列表中，已加入组数量相应减少。")

h("2.3.2.2 UI界面（必须）", 4)
para("退出用户组弹窗见图 5，界面元素与交互要求见下表。")
figure("fig5_leave.png", "图 5　单个用户退出用户组弹窗", 12)
ui_table([
    ["弹窗标题", "“退出用户组”，采用警示色（红色）标题与加入操作区分；右上角关闭按钮（×）等同取消"],
    ["信息条", "只读展示“目标用户”与“待选择退出组（共 N 个）”，N 为该用户当前所属用户组数量"],
    ["组列表", "表头行“所属用户组”带复选框（用于全选/取消全选）；每个组占一行，左侧复选框、右侧组名标签（如 obs-group-readonly），支持多选"],
    ["计数提示", "列表下方显示“已选中待退出用户组：N 个”，随勾选实时变化，未勾选时为 0"],
    ["主按钮", "文案随勾选数量变化：“确认退出选中的 N 个用户组”；N 为 0 时置灰不可点击；提交中显示加载态并禁止重复点击"],
    ["次按钮", "“取消”，关闭弹窗且不产生任何变更"],
])

h("2.3.2.3 功能核心点描述（必须）", 4)
steps([
    "打开弹窗：由列表行“退出用户组”触发，带入目标用户；同时查询该用户的全部成员关系（ListGroupMembershipsForMember，按响应中的 next_marker 翻页取全），逐条列出组名与对应的 membership_id，保证“共 N 个”与实际一致。",
    "默认状态：不预先勾选任何组，避免误提交；运维勾选后才允许提交。",
    "计数与文案联动：勾选或取消勾选时，实时更新“已选中待退出用户组：N 个”与主按钮文案；N 为 0 时主按钮置灰不可点击。",
    "提交执行：按勾选顺序逐条调用 DeleteGroupMembership（传 identity_store_id 与 membership_id），逐条记录成功与失败。",
    "结果处理：全部成功时关闭弹窗、提示“已退出 N 个用户组”并刷新列表；存在失败时弹窗保持打开，逐条标注失败原因（无权限、成员关系已不存在、超时等），失败项保留勾选状态便于再次提交。",
    "幂等处理：接口返回 404（成员关系已不存在）按已退出处理，计入成功、不报错。",
    "异常数据：若查询结果中存在多条指向同一组的记录（异常情况），按组名去重展示，退出时逐条删除并记录告警。",
    "交互保护：提交过程中禁用主按钮与组列表复选框，防止重复提交。",
])

h("2.3.2.4 成功的标准（必须）", 4)
bullets([
    "弹窗列出的组清单与该用户实际所属用户组一致，“共 N 个”与清单条数一致。",
    "勾选 0 个时主按钮不可点击；勾选后按钮文案与已选数量一致。",
    "退出成功后详情弹窗不再显示该组，已加入组数量同步减少。",
    "对同一组重复执行退出不报错，按幂等成功处理。",
    "部分失败时，失败组仍保留在弹窗中并附明确原因。",
])

h("2.3.2.5 异常处置标准和风险考虑（按需）", 4)
para("退出是不可逆的权限收回操作，异常处置原则是“数量明示、失败可见、留有回退说明”。")
bullets([
    ("用户已无任何所属组：", "列表页“退出用户组”置灰不可点击；若弹窗以其他方式打开，显示空态提示“该用户暂无所属用户组”。"),
    ("部分失败：", "提示“成功 X 个、失败 Y 个”，失败项保留在弹窗中供再次提交，已成功项不再出现在刷新后的列表里。"),
    ("组数量较多：", "弹窗内区域滚动展示，不截断、不隐藏，计数以全部组为准。"),
    ("超时或无响应：", "提示“操作失败，请重试”，不自动重试；重试前建议先刷新弹窗以获取最新所属组。"),
])
para("风险考虑：")
bullets([
    "退出原组后权限立即失效，若用户尚未加入目标组会造成权限空档；弹窗信息条固定展示“目标用户”与待退出组，页面文案提示“请确认该用户已加入目标组后再退出”。",
    "误勾选会导致权限收回，恢复需重新加入，因此主按钮文案必须明确“确认退出选中的 N 个用户组”，不允许“一键全选后直接提交”的默认路径。",
    "退出属高危写操作，须记录操作人、时间、目标用户、用户组与结果，满足事后审计追溯（留存期限待确认）。",
])
para("待确认事项：")
bullets([
    "是否需要提供“全部勾选”的快捷操作（当前仅表头复选框）。",
    "退出操作是否需要填写变更原因或关联工单号。",
])

h("2.3.3 非功能需求（按需）", 3)
bullets([
    ("性能要求：", "打开弹窗并加载所属用户组不超过 2 秒（组数量 100 个以内）；退出提交的响应时间以接口为准。"),
    ("安全与合规要求：", "退出属高危操作，须二次确认并全量留痕；入口仅对授权角色可见。"),
    ("可靠性要求：", "退出幂等，重复提交不报错；部分失败不影响已成功项的状态一致性。"),
])

h("2.3.4 需求优先级（必须）", 3)
bullets([("优先级分类：", "高优先。本功能点是权限收敛目标的直接承载，缺失则原组的冗余权限无法剥离。")])
bullets([("预期上线时间：", "")])
bullets([
    "重保环境上线时间：待排期确认（建议 2026/12/15）",
    "生产环境上线时间：待排期确认（建议 2027/01/31）",
], mark="○", indent=400)

# ---------------------------------------------------------------- 2.4 批量迁入
h("2.4 存量用户批量迁入目标用户组", 2)

h("2.4.1 需求背景和目标（必须）", 3)
lead("需求背景：", "存量 OBS 用户规模为千级，若只能逐个操作，人工成本高且容易漏迁、错迁。列表页已支持多选，具备批量处理的条件。批量操作的语义定为“统一迁入同一目标用户组”，单次最多 10 个用户，既覆盖常见的成批处理场景，也把单次误操作的影响面控制在可接受范围。批量迁入只做“加入”，不自动退出原组：一旦在批量流程中自动退出，执行顺序与异常处理无法逐用户确认，容易出现权限空档。")
lead("需求目标：", "支持勾选多个用户后统一选择目标用户组并一次性完成加入，逐用户返回执行结果；失败用户可识别、可重试；操作结果与页面列表状态保持一致。")
lead("目标用户：", "云平台运维工程师（执行人）。")

h("2.4.2 功能需求", 3)
h("2.4.2.1 功能的使用场景", 4)
para("运维人员在列表页勾选 4 个待迁移用户（li01、wang02、liu03、chen04），工具栏按钮变为“批量迁入（已选 4/10）”；点击后弹窗显示待迁入用户标签与“目标迁入用户组”下拉，选择目标组后点击“确认批量迁入”；提交完成提示“共 4 个用户，成功 3 个，失败 1 个”并列出失败用户与原因；关闭弹窗后列表刷新，运维再对失败用户单独重试。")

h("2.4.2.2 UI界面（必须）", 4)
para("批量迁入用户组弹窗见图 6，界面元素与交互要求见下表。")
figure("fig6_batch.png", "图 6　多个用户批量迁入用户组弹窗", 12)
ui_table([
    ["入口按钮", "列表页工具栏“批量迁入（已选 N/10）”；N 为 0 时置灰不可点击，N 为 1 到 10 时可点击"],
    ["弹窗标题", "“批量迁入用户组”；右上角关闭按钮（×）等同取消"],
    ["待迁入用户", "只读展示“待迁入用户（已选 N 人）”，下方以标签形式横向排列所选用户名，超出区域可滚动；弹窗内不支持增删，需关闭后回列表调整"],
    ["目标迁入用户组", "必填项（标红星），下拉单选，占位文案“请选择要统一迁入的目标用户组”；所选目标组对本次全部用户生效"],
    ["主按钮", "“确认批量迁入”；未选择目标组时置灰不可点击；提交中显示加载态与执行进度，并禁止重复点击"],
    ["次按钮", "“取消”，关闭弹窗且不产生任何变更"],
])

h("2.4.2.3 功能核心点描述（必须）", 4)
steps([
    "入口约束：勾选数量为 0 时按钮置灰；勾选数量达到 10 后其余行复选框禁用，并提示“单次最多勾选 10 个用户”。",
    "带入校验：打开弹窗时以当前勾选结果生成待迁入用户列表，与列表页勾选状态一致；弹窗打开期间列表勾选发生变化时，以弹窗打开时的快照为准，提交前回显人数供核对。",
    "目标组选择：下拉候选来自 ListGroups，选定后取 group_id，本次全部用户共用同一目标组；同名组须可区分，避免整批绑错组。",
    "执行方式：按用户逐个调用 CreateGroupMembership，串行执行以保证逐用户留痕与结果可核对（限流由多云服务统一处理）；每个用户独立记录成功或失败与错误原因，单个失败不影响其余用户。",
    "幂等处理：接口返回 409（已在组中）按成功处理，结果中标注“已在该组中”。",
    "结果汇总：提交结束后提示“共 N 个用户，成功 X 个，失败 Y 个”，失败项列出用户名与原因，且 X 加 Y 等于 N；弹窗关闭、列表刷新。",
    "不退出原组：批量迁入只建立目标组的成员关系，不调用退出接口；原组权限需通过单个用户“退出用户组”收回（原因见风险考虑）。",
    "重试：对失败用户，运维可重新勾选后再次从原入口执行批量迁入，幂等机制保证已成功用户不产生重复关系。",
])

h("2.4.2.4 成功的标准（必须）", 4)
bullets([
    "勾选 N 个用户并确认后，每个用户均建立目标组成员关系（或原本已存在），结果提示中成功数与失败数之和等于 N。",
    "单次勾选上限 10 生效，勾选第 11 个用户时被拦截并给出提示。",
    "批量执行中 1 个用户失败时，其余用户正常完成，失败项可单独识别。",
    "批量迁入完成后，逐个打开详情可看到新组，已加入组数量同步变化。",
    "对同一批用户重复执行批量迁入，不产生重复成员关系。",
])

h("2.4.2.5 异常处置标准和风险考虑（按需）", 4)
para("批量操作的影响面大于单个操作，异常处置原则是“失败隔离、结果可数、可再重试”。")
bullets([
    ("部分失败：", "提示成功与失败数量，失败项给出原因（无权限、目标组不存在、超时、参数非法）；失败用户可重新勾选后再次批量迁入。"),
    ("目标组被删除或无权限：", "整批失败时统一提示原因，不逐个重试，避免产生大量无效调用。"),
    ("勾选数量超限：", "前端拦截并提示，不进入弹窗。"),
    ("提交中断（页面刷新或网络中断）：", "再次提交时幂等，不会重复建立成员关系；已成功的用户可通过逐个查看详情核对。"),
])
para("风险考虑：")
bullets([
    "“迁入即完成”的误解：批量迁入不退出原组，若运维据此认为迁移结束，权限将长期未收敛；页面与结果提示中须固定说明“如需收回原组权限，请对用户执行退出用户组”。",
    "批量误操作的影响面：单次最多 10 个用户，弹窗内回显待迁入用户与目标组，提交前可整体核对。",
    "接口限流：限流已由多云服务统一控制，业务侧无需计算配额或调整并发；若仍返回限流错误，提示稍后重试并单独计数，不与业务失败混为一谈。",
])
para("待确认事项：")
bullets([
    "批量执行是否需要展示进度条或转为后台异步任务（当前为同步提交并等待结果）。",
    "是否提供“仅重试失败用户”的快捷操作。",
    "单次 10 个的上限是否为固定值，是否允许按角色或配置调整。",
])

h("2.4.3 非功能需求（按需）", 3)
bullets([
    ("性能要求：", "10 个用户的批量迁入在 60 秒内返回结果；单个用户失败不影响整批的响应时间上限（超时按接口设置逐用户计算）。"),
    ("可靠性要求：", "批量执行中的单用户失败必须隔离，结果计数守恒（成功 + 失败 = 总数）。"),
    ("安全要求：", "批量操作记录操作人、时间、目标用户清单、目标组与逐用户结果。"),
])

h("2.4.4 需求优先级（必须）", 3)
bullets([("优先级分类：", "高优先。千级存量用户无法逐个操作，批量迁入是控制迁移窗口长度的关键手段。")])
bullets([("预期上线时间：", "")])
bullets([
    "重保环境上线时间：待排期确认（建议 2026/12/15）",
    "生产环境上线时间：待排期确认（建议 2027/01/31）",
], mark="○", indent=400)

def _pb(p):
    """把段前分页设在标题上，避免分页符独占一页产生空白页。"""
    p.paragraph_format.page_break_before = True
    return p


# -*- coding: utf-8 -*-
# 第 3 章 接口需求 / 第 4 章 业务流程

APIW = [Cm(4.6), Cm(2.0), Cm(2.2), Cm(6.2)]


def api_table(rows):
    return add_table(doc, ["参数", "是否必选", "参数类型", "说明"], rows, APIW,
                     aligns=["left", "center", "center", "left"], font_size=10)


# ================================================================ 3 接口需求
_pb(h("3 接口需求", 1))

para("本章说明四个功能点分别调用哪些接口、每个接口的参数与返回值，以及平台侧的调用约束。接口路径、参数约束与返回结构均取自《IAM 身份中心 API 参考》（文档版本 02，2025-12-19）4.12 用户组管理与 4.13 用户/用户组绑定关系管理两节，本文档只做与本需求相关的裁剪，不改变接口语义。")

# ---------------------------------------------------------------- 3.1
h("3.1 功能与接口的对应关系", 2)
para("四个功能点共使用 4 个接口，不存在“一个功能点独占一个接口”的简单对应：列表页与两个弹窗都需要先“读”后“写”，因此读接口（ListGroups、ListGroupMembershipsForMember）被多个功能点复用。对应关系见下表。")
add_table(
    doc,
    ["功能点", "调用接口", "调用时机与用途", "返回值用途"],
    [
        ["2.1 列表页",
         "ListGroups\nListGroupMembershipsForMember",
         "进入页面时加载用户组清单；按用户查询其当前所属用户组（列表列展示、详情弹窗展示）",
         "ListGroups 提供 group_id 与 display_name 的映射；ForMember 提供用户所属的 group_id 集合"],
        ["2.2 单个用户加入",
         "ListGroupMembershipsForMember\nListGroups\nCreateGroupMembership",
         "打开弹窗时带入该用户当前所属组、加载目标组下拉候选；点击“确认加入”时建立成员关系",
         "CreateGroupMembership 返回 membership_id，作为加入成功的判定依据"],
        ["2.3 单个用户退出",
         "ListGroupMembershipsForMember\nListGroups\nDeleteGroupMembership",
         "打开弹窗时列出该用户全部所属组并取得每组对应的 membership_id；勾选后逐个解绑",
         "ForMember 返回的 membership_id 是 DeleteGroupMembership 的唯一入参依据"],
        ["2.4 批量迁入",
         "ListGroups\nCreateGroupMembership（逐用户，N 次）",
         "加载目标组下拉候选；点击“确认批量迁入”后按用户串行建立成员关系",
         "逐用户返回 membership_id 或错误原因，用于结果汇总"],
    ],
    [Cm(3.3), Cm(4.3), Cm(4.3), Cm(3.1)],
    aligns=["left", "left", "left", "left"],
    font_size=10,
)
para("从表中可以读出两条对实现有直接影响的结论，需在开发前确认：")
bullets([
    ("读接口复用：", "ListGroups 是“组 ID → 组名”的唯一来源，ListGroupMembershipsForMember 只返回 group_id 而不返回组名。因此任何需要向用户展示组名的地方（列表列、详情弹窗、退出弹窗）都必须把 ForMember 的结果再用 ListGroups 做一次名称映射，不能直接展示 group_id。"),
    ("写接口依赖读接口：", "DeleteGroupMembership 的入参是 membership_id（成员关系 ID），不是 group_id 与 user_id 的组合。退出操作必须先用 ForMember 取到该用户在各组的 membership_id，再按 membership_id 逐个解绑；不能用组 ID 直接退组。"),
])

# ---------------------------------------------------------------- 3.2
h("3.2 接口清单", 2)
para("四个接口的协议级信息见下表。四个接口均为组织级管理接口，仅允许组织的管理账号或作为服务委托管理员的成员账号调用。平台侧不直接对接云侧，而是统一经多云服务（公司与云侧之间的统一接入层）调用：Region、Endpoint、服务委托管理员凭据与限流策略均由多云服务在内部完成，业务侧只需传入业务参数（identity_store_id、user_id、group_id、membership_id 等）。")
add_table(
    doc,
    ["序号", "接口名称", "请求方法", "URI", "访问级别"],
    [
        ["1", "ListGroups\n（列出用户组）", "GET",
         "/v1/identity-stores/{identity_store_id}/groups", "Read"],
        ["2", "ListGroupMembershipsForMember\n（列出用户加入的组）", "GET",
         "/v1/identity-stores/{identity_store_id}/group-memberships-for-member", "Read"],
        ["3", "CreateGroupMembership\n（绑定用户和组）", "POST",
         "/v1/identity-stores/{identity_store_id}/group-memberships", "Write"],
        ["4", "DeleteGroupMembership\n（解绑用户和组）", "DELETE",
         "/v1/identity-stores/{identity_store_id}/group-memberships/{membership_id}", "Write"],
    ],
    [Cm(1.3), Cm(4.7), Cm(1.9), Cm(4.9), Cm(2.2)],
    aligns=["center", "left", "center", "left", "center"],
    font_size=9,
)

# ---------------------------------------------------------------- 3.3
h("3.3 公共请求约定", 2)
bullets([
    ("域名与协议：", "云侧接口统一使用 HTTPS，路径形如 /v1/identity-stores/{identity_store_id}/...；hostname 所对应的 Region 与 Endpoint 由多云服务按环境预置，业务侧不感知、也不作为参数传入，本需求不涉及多 Region 选择。"),
    ("身份源参数：", "所有接口的路径参数 identity_store_id 为身份源的全局唯一标识符，长度固定 12 位；平台侧以配置项维护，不允许由页面传入，避免越权访问其他身份源。"),
    ("鉴权头：", "云侧接口支持 X-Security-Token 请求头（String，最大长度 2048），仅在调用方使用临时安全凭据时必填。本需求中该头由多云服务按服务委托管理员身份统一处理，业务侧不构造鉴权信息、不持有云侧凭据。"),
    ("错误响应：", "4xx 响应统一返回 error_code（错误码）、error_msg（错误信息）、request_id（请求 ID）三个字段；403 响应额外返回 encoded_authorization_message（加密的错误信息）。平台侧的错误提示应优先使用 error_msg，并在日志中留存 request_id 以便向云侧追溯。"),
    ("分页：", "列表类接口（ListGroups、ListGroupMembershipsForMember）均通过 limit 与 marker 分页，limit 默认 100、最大 100，响应中 page_info.next_marker 为 null 表示已到末页。"),
])
para("状态码与平台侧的处置方式见下表。")
add_table(
    doc,
    ["状态码", "含义", "平台侧处置"],
    [
        ["200", "请求成功（ListGroups、ForMember、CreateGroupMembership 均以 200 返回结果体）", "正常处理返回数据"],
        ["400", "请求参数错误（参数缺失、格式或长度不合法、身份源不匹配）", "提示参数或环境配置错误，记录 request_id，不重试"],
        ["403", "无权限或凭据失效（含 encoded_authorization_message）", "提示无权限或登录失效，检查服务委托授权后重试"],
        ["404", "资源不存在（目标组已被删除、成员关系已不存在）", "退出操作中视为“已不在该组”，按成功处理；加入操作中提示目标组不存在"],
        ["409", "资源冲突（用户已在该用户组中）", "加入操作中按成功处理，提示“该用户已在该组中”"],
        ["5xx / 超时", "云侧服务异常或网络超时", "提示稍后重试；操作幂等，可直接重试"],
        ["限流 / 429", "调用频率超出配额，被限流拦截", "限流由多云服务统一处理（含配额与重试策略），业务侧按串行方式提交即可；若仍返回限流错误，提示稍后重试并不计入业务失败"],
    ],
    [Cm(1.8), Cm(6.6), Cm(6.6)],
    aligns=["center", "left", "left"],
    font_size=10,
)

# ---------------------------------------------------------------- 3.4
h("3.4 ListGroups —— 列出用户组", 2)
para("按身份源查询用户组列表，用于填充“选择目标用户组”下拉候选，以及把 group_id 映射为组名。支持按显示名模糊查询，匹配区分大小写。")
para("（1）路径参数", bold=True)
api_table([
    ["identity_store_id", "是", "String", "身份源的全局唯一标识符（ID）。长度固定 12 位"],
])
para("（2）Query 参数", bold=True)
api_table([
    ["marker", "否", "String", "分页标记。长度 24 位；取上一页响应中 page_info.next_marker 的值"],
    ["limit", "否", "Integer", "每个请求返回的最大结果数。取值范围 1—100，缺省值 100"],
    ["display_name", "否", "String", "按用户组显示名模糊查询。用于下拉框内检索目标组；匹配区分大小写，前端检索需按原样提交关键字"],
])
para("（3）请求 Header", bold=True)
api_table([
    ["X-Security-Token", "否", "String", "使用临时安全凭据时必填，取值为会话令牌。最大长度 2048"],
])
para("（4）响应参数（状态码 200）", bold=True)
api_table([
    ["groups", "—", "Array", "满足查询条件的用户组对象列表"],
    ["page_info", "—", "Object", "分页信息，含 next_marker 与 current_count"],
])
para("其中 groups 数组元素的字段见下表，平台侧实际使用的字段为 group_id 与 display_name，其余字段按需留档。", first=0)
add_table(
    doc,
    ["字段", "类型", "说明", "本需求是否使用"],
    [
        ["group_id", "String", "用户组的全局唯一标识符，长度 1—47", "使用：作为加入目标组时的绑定依据"],
        ["display_name", "String", "用户组显示名称，长度 1—1024", "使用：下拉候选与列表展示"],
        ["description", "String", "用户组描述，长度 1—1024", "不使用"],
        ["external_id", "String", "外部身份源分配给此资源的标识符", "不使用"],
        ["external_ids", "Array", "外部身份提供商颁发的标识符列表，数组长度 0—10，元素含 id 与 issuer", "不使用"],
        ["identity_store_id", "String", "所属身份源的 ID，长度 1—36", "使用：校验与配置一致性"],
        ["created_at / created_by", "Long / String", "创建时间戳与创建者", "不使用"],
        ["updated_at / updated_by", "Long / String", "更新时间戳与更新者", "不使用"],
    ],
    [Cm(4.0), Cm(3.0), Cm(5.6), Cm(2.4)],
    aligns=["left", "center", "left", "left"],
    font_size=10,
)
para("page_info 字段：next_marker（String，无更多数据时为 null）、current_count（Integer，本页返回条目数）。")

# ---------------------------------------------------------------- 3.5
h("3.5 ListGroupMembershipsForMember —— 列出用户加入的组", 2)
para("按用户 ID 列出该用户已加入的全部用户组，是本需求唯一的“读用户所属组”接口：列表页的当前用户组、详情弹窗的组标签、退出弹窗的待退出清单，均以本接口结果为数据源。")
para("（1）路径参数", bold=True)
api_table([
    ["identity_store_id", "是", "String", "身份源的全局唯一标识符（ID）。长度固定 12 位"],
])
para("（2）Query 参数", bold=True)
api_table([
    ["user_id", "是", "String", "用户唯一标识。长度 1—64"],
    ["limit", "否", "Integer", "每个请求返回的最大结果数。取值范围 1—100，缺省值 100"],
    ["marker", "否", "String", "分页标记。长度 24 位"],
])
para("（3）请求 Header", bold=True)
api_table([
    ["X-Security-Token", "否", "String", "使用临时安全凭据时必填，取值为会话令牌。最大长度 2048"],
])
para("（4）响应参数（状态码 200）", bold=True)
api_table([
    ["group_memberships", "—", "Array", "满足查询条件的成员关系对象列表"],
    ["page_info", "—", "Object", "分页信息，含 next_marker 与 current_count"],
])
para("group_memberships 数组元素的字段见下表。注意该数组返回的是“成员关系”而不是“用户组”，只包含 group_id，不包含用户组名称。", first=0)
add_table(
    doc,
    ["字段", "类型", "说明", "本需求是否使用"],
    [
        ["membership_id", "String", "用户与组关联关系的全局唯一标识符，长度 1—47", "使用：退出用户组时作为 DeleteGroupMembership 的入参"],
        ["group_id", "String", "用户组的全局唯一标识符", "使用：配合 ListGroups 映射为组名"],
        ["member_id.user_id", "String", "用户的全局唯一标识符，长度 1—47", "使用：校验返回结果与请求用户一致"],
        ["identity_store_id", "String", "所属身份源的 ID，长度 1—36", "使用：配置一致性校验"],
    ],
    [Cm(4.2), Cm(2.6), Cm(5.6), Cm(2.6)],
    aligns=["left", "center", "left", "left"],
    font_size=10,
)

# ---------------------------------------------------------------- 3.6
h("3.6 CreateGroupMembership —— 绑定用户和组", 2)
para("将用户添加到用户组中，是“加入目标用户组”与“批量迁入”的唯一写接口。用户和用户组必须在同一身份源下，跨身份源绑定会被拒绝。")
para("（1）路径参数", bold=True)
api_table([
    ["identity_store_id", "是", "String", "身份源的全局唯一标识符（ID）。长度固定 12 位"],
])
para("（2）请求 Body 参数", bold=True)
api_table([
    ["group_id", "是", "String", "目标用户组的全局唯一标识符。长度 1—47。取自 ListGroups 的返回值或页面下拉所选"],
    ["member_id", "是", "Object", "包含组成员标识符的对象，见下表"],
])
para("member_id 子字段：", bold=True, first=0)
api_table([
    ["user_id", "是", "String", "用户的全局唯一标识符（ID）。长度 1—47"],
])
para("（3）请求 Header", bold=True)
api_table([
    ["X-Security-Token", "否", "String", "使用临时安全凭据时必填，取值为会话令牌。最大长度 2048"],
])
para("（4）响应参数（状态码 200）", bold=True)
api_table([
    ["membership_id", "—", "String", "用户与组关联关系的全局唯一标识符，长度 1—47"],
    ["identity_store_id", "—", "String", "身份源的全局唯一标识符（ID），长度 1—36"],
])

# ---------------------------------------------------------------- 3.7
h("3.7 DeleteGroupMembership —— 解绑用户和组", 2)
para("根据关联关系 ID 解绑用户和用户组，即把用户移出用户组，是“退出原用户组”的唯一写接口。该接口只接受 membership_id，不接受 group_id 与 user_id，因此调用前必须先通过 ListGroupMembershipsForMember 取得 membership_id。")
para("（1）路径参数", bold=True)
api_table([
    ["identity_store_id", "是", "String", "身份源的全局唯一标识符（ID）。长度固定 12 位"],
    ["membership_id", "是", "String", "用户与组关联关系的全局唯一标识符。长度 1—64。取自 ListGroupMembershipsForMember 的返回值"],
])
para("（2）请求 Header", bold=True)
api_table([
    ["X-Security-Token", "否", "String", "使用临时安全凭据时必填，取值为会话令牌。最大长度 2048"],
])
para("（3）响应参数", bold=True, first=0)
para("解绑成功返回状态码 200，响应无响应体；失败时按 3.3 的统一错误结构返回 error_code、error_msg 与 request_id。平台侧以 HTTP 状态码判定成败，不依赖响应体内容。")

# ---------------------------------------------------------------- 3.8
h("3.8 调用约束与实现要求", 2)
para("以下约束由接口语义与业务流程共同决定，属于研发必须遵守的实现要求，测试用例需逐条覆盖。")
add_table(
    doc,
    ["编号", "约束", "说明与依据"],
    [
        ["IF-01", "退出前必须先取 membership_id",
         "DeleteGroupMembership 的路径参数是 membership_id，无法用 group_id 与 user_id 组合直接退组。退出弹窗打开时须调用 ForMember 取得该用户在各组的 membership_id，并在提交时按所选组的 membership_id 逐个解绑。"],
        ["IF-02", "组名展示必须经 ListGroups 映射",
         "ForMember 只返回 group_id，不含组名。列表列、详情弹窗、退出弹窗展示组名时，须以 ListGroups 的结果建立 group_id→display_name 映射；映射缺失（组已删除）时展示“组已失效（group_id 前 8 位）”而不是空白。"],
        ["IF-03", "分页必须循环取全量",
         "两个查询接口单页最多 100 条，next_marker 非 null 时须继续请求，直到其为 null。用户所属组超过 100 个、用户组总数超过 100 个时不得只取首页。"],
        ["IF-04", "写入必须串行",
         "批量迁入按用户串行调用 CreateGroupMembership，单个用户完成后才发起下一个，不得并发提交；串行的目的是保证“先加入、后退出”的顺序与逐用户结果留痕，而非规避限流（限流已由多云服务统一处理）。批量上限 10 个用户与本约束配合。"],
        ["IF-05", "幂等判定",
         "加入时返回 409（用户已在该组中）视为成功；退出时返回 404（成员关系已不存在）视为成功。两者均计入成功数并在结果中注明，不作为失败提示。"],
        ["IF-06", "身份源一致性",
         "identity_store_id 由平台配置统一注入，页面不传；目标组与用户必须属于同一身份源，下拉候选只加载当前身份源下的用户组，避免跨身份源误绑。"],
        ["IF-07", "调用主体与授权",
         "四个接口均要求组织的管理账号或服务委托管理员成员账号调用。服务委托管理员的授权与凭据已在多云服务中配置完成（授权项为 IdentityCenter:group:list、IdentityCenter:groupMembership:listForMember、IdentityCenter:groupMembership:create、IdentityCenter:groupMembership:delete），业务侧不重复申请、不自行管理凭据。"],
        ["IF-08", "错误可追溯",
         "每次调用记录接口名、请求参数、HTTP 状态码、error_code 与 request_id；提示文案使用 error_msg 的可读信息，不向前端暴露堆栈或凭据。"],
    ],
    [Cm(1.4), Cm(4.2), Cm(9.4)],
    aligns=["center", "left", "left"],
    font_size=10,
)
para("调用环境与前提（已与需求方确认，研发按此实现，不再作为待确认项）：")
_t = add_table(
    doc,
    ["事项", "结论", "对实现的约束"],
    [
        ["Region 与 Endpoint",
         "由多云服务统一处理，不在本需求范围",
         "代码中不硬编码 hostname、region；环境切换不改业务代码"],
        ["服务委托管理员账号",
         "已在多云服务中配置完成",
         "业务侧不持有凭据、不构造鉴权头；401/403 统一提示，不自行重试鉴权"],
        ["限流（QPS）",
         "已由多云服务统一限流",
         "仍按用户串行提交（为保证顺序与留痕，非规避限流）；限流错误不计业务失败"],
        ["ListGroups 显示名匹配",
         "区分大小写",
         "关键字原样提交、不做归一；界面注明“区分大小写”，避免误判为组不存在"],
    ],
    [Cm(3.9), Cm(5.9), Cm(5.2)],
    aligns=["left", "left", "left"],
    font_size=10,
)
# 形如“（1）路径参数”的小标签不得与紧随其后的表格分页
import re as _re
for _p in doc.paragraphs:
    if _re.match(r"^（\d）", _p.text.strip()):
        _p.paragraph_format.keep_with_next = True

# ================================================================ 4 业务流程
_pb(h("4 业务流程", 1))
para("本章按“总体—单个用户—批量”三层描述流程，后三节分别对应 2.2、2.3、2.4 的页面交互与接口调用顺序。图中蓝色节点为接口调用，橙色节点为业务规则集中的关键步骤。")

h("4.1 总体业务流程", 2)
para("迁移以用户为单位推进，单个用户的处理顺序固定为“先加入目标组、再退出原组”。批量迁入只承担“加入”这一步，退出仍由单用户弹窗完成，避免批量流程中出现无法逐用户确认的顺序问题。")
figure("fig7_flow_main.png", "图 7　存量用户组迁移总体业务流程", 13.0)
para("流程说明：")
steps([
    "进入列表页，加载用户清单及各用户当前所属用户组（数据来源见 3.5）。",
    "按用户名检索定位用户，点“详情”核对当前所属组，判断是否需要迁移。",
    "先执行“加入用户组”，成功后再执行“退出用户组”（详见图 8、图 9）。",
    "回到列表处理下一个用户；全部完成后逐用户核对结果。",
])

_pb(h("4.2 单个用户加入目标用户组流程", 2))
para("加入流程的关键点是“先取现状、再写关系”：弹窗打开先查询现状供核对，提交只调用一次写接口，结果判定把 409 归入成功。")
figure("fig8_flow_join.png", "图 8　单个用户加入目标用户组流程", 13.6)
para("流程要点：")
bullets([
    ("进入方式：", "由列表行“加入用户组”触发，目标用户由列表行带入，弹窗内不可更改。"),
    ("现状查询：", "调用 ListGroupMembershipsForMember 取得该用户当前所属组，再经 ListGroups 映射为组名后展示在信息条；查询失败时不打开弹窗，直接提示原因，避免用户在信息不全的情况下操作。"),
    ("候选加载：", "ListGroups 分页取全量用户组作为下拉候选；候选为空时提示“当前身份源下无可用用户组”，并禁用提交按钮。"),
    ("提交与判定：", "调用 CreateGroupMembership 提交 group_id 与 member_id.user_id；返回 200 且带 membership_id 判为成功，返回 409 判为“已在该组中”，两者都关闭弹窗并刷新列表（刷新后列表与详情应能查到新组、已加入组数量加一）；其余情况弹窗保持打开。"),
])

para("本节的接口调用时序见下表，入参约束以第 3 章为准。")
add_table(
    doc,
    ["步骤", "页面动作", "调用接口", "关键入参", "结果判定"],
    [
        ["1", "列表页点“加入用户组”，打开弹窗", "ListGroupMembershipsForMember", "user_id、limit=100、marker", "取所属组集合，失败则不打开弹窗"],
        ["2", "弹窗加载目标组下拉候选", "ListGroups", "limit=100、marker（需要时带 display_name）", "候选为空时提示并禁用提交"],
        ["3", "点“确认加入”", "CreateGroupMembership", "group_id、member_id.user_id", "200 成功；409 视为已加入；其余为失败"],
        ["4", "成功后刷新列表与详情", "ListGroupMembershipsForMember ＋ ListGroups", "user_id；组清单", "详情可见新组，已加入组数量加一"],
    ],
    [Cm(1.2), Cm(3.6), Cm(3.8), Cm(3.4), Cm(3.0)],
    aligns=["center", "left", "left", "left", "left"],
    font_size=10,
)

_pb(h("4.3 单个用户退出原用户组流程", 2))
para("退出比加入多一步“取关系 ID”：必须先由 ListGroupMembershipsForMember 拿到 membership_id，才能调用 DeleteGroupMembership。")
figure("fig9_flow_leave.png", "图 9　单个用户退出原用户组流程", 13.2)
para("流程要点：")
bullets([
    ("前置判断：", "用户当前无所属用户组时，列表行的“退出用户组”链接置灰不可点击，流程不进入弹窗。"),
    ("清单加载：", "调用 ForMember 取得全部成员关系，保留 group_id 与 membership_id 的对应关系；经 ListGroups 映射组名后列示，映射不到的组标注为“组已失效”。"),
    ("勾选约束：", "勾选数量为 0 时提交按钮置灰；按钮文案随勾选数量变化，提示本次将退出的组数。退出会立即收回该组权限，若用户尚未加入目标组，界面应提示先执行加入操作，防止权限空档。"),
    ("提交与判定：", "按勾选的组逐个调用 DeleteGroupMembership（每次一个 membership_id），串行执行并逐项记录：200 判为成功，404 判为“已不在该组”并按成功处理，其余为失败；汇总提示成功数与失败数，失败项给出原因。"),
])

para("本节的接口调用时序见下表。注意第 3 步的入参是第 1 步取得的 membership_id，两步之间存在数据依赖，不可并行。")
add_table(
    doc,
    ["步骤", "页面动作", "调用接口", "关键入参", "结果判定"],
    [
        ["1", "打开退出弹窗，列示所属用户组", "ListGroupMembershipsForMember", "user_id、limit=100、marker", "取 group_id 与 membership_id 的对应关系"],
        ["2", "把组 ID 映射为组名", "ListGroups", "limit=100、marker", "映射不到的组标注“组已失效”"],
        ["3", "勾选后点“确认退出”，逐组提交", "DeleteGroupMembership", "membership_id（取自第 1 步）", "200 成功；404 视为已不在该组；其余为失败"],
        ["4", "汇总并刷新列表与详情", "ListGroupMembershipsForMember ＋ ListGroups", "user_id；组清单", "已加入组数量相应减少"],
    ],
    [Cm(1.2), Cm(3.6), Cm(3.8), Cm(3.4), Cm(3.0)],
    aligns=["center", "left", "left", "left", "left"],
    font_size=10,
)

_pb(h("4.4 存量用户批量迁入流程", 2))
para("批量迁入是“同一目标组 × N 个用户”的循环写入：打开弹窗对待迁入用户取快照，提交后按用户串行调用 CreateGroupMembership 并做计数守恒校验。")
figure("fig10_flow_batch.png", "图 10　存量用户批量迁入目标用户组流程", 12.6)
para("流程要点：")
bullets([
    ("入口约束：", "勾选数量为 0 时入口按钮置灰，达到 10 个后其余行复选框禁用，前端拦截超限，不进入弹窗。"),
    ("快照机制：", "弹窗打开瞬间固定待迁入用户清单，弹窗内不可增删；如需调整须关闭弹窗回列表重新勾选，避免执行过程中清单漂移。"),
    ("循环写入：", "以 i = 1…N 串行调用 CreateGroupMembership，每个用户独立判定：200 或 409 计成功，其余计失败并记录 error_code 与 request_id，单用户失败不中断整批。"),
    ("结果汇总：", "结束后提示“共 N 个，成功 X 个，失败 Y 个”，校验 X + Y = N；失败项列出用户名与原因，可重新勾选后再次执行。批量迁入不调用 DeleteGroupMembership，原组权限不随批量操作收回，结果提示中须固定说明“如需收回原组权限，请对用户执行退出用户组”。"),
])

para("本节的接口调用时序见下表，其中第 3 步按用户重复 N 次，每次结束后立即记录结果再进入下一个用户。")
add_table(
    doc,
    ["步骤", "页面动作", "调用接口", "关键入参", "结果判定"],
    [
        ["1", "打开批量弹窗，加载目标组候选", "ListGroups", "limit=100、marker", "候选为空时提示并禁用提交"],
        ["2", "点“确认批量迁入”，固定待迁入清单", "—（前端快照）", "勾选结果快照，N ≤ 10", "人数与列表勾选一致"],
        ["3", "对第 i 个用户提交（i = 1…N）", "CreateGroupMembership", "group_id、member_id.user_id（第 i 个）", "200 或 409 计成功；其余计失败并记录原因"],
        ["4", "汇总并刷新列表", "—（前端汇总）", "逐用户结果", "成功数 + 失败数 = N"],
    ],
    [Cm(1.2), Cm(3.6), Cm(3.8), Cm(3.4), Cm(3.0)],
    aligns=["center", "left", "left", "left", "left"],
    font_size=10,
)

_pb(h("4.5 接口结果与页面判定的对应关系", 2))
para("同一份接口返回在三个功能点上可能对应不同的页面判定，为避免实现时口径不一，统一见下表。")
add_table(
    doc,
    ["接口与结果", "2.2 加入", "2.3 退出", "2.4 批量迁入"],
    [
        ["200 且返回 membership_id", "成功：提示加入成功，关闭弹窗", "—", "该用户计成功"],
        ["200 无响应体", "—", "成功：该组退出完成", "—"],
        ["409 用户已在该组", "成功：提示“该用户已在该组中”", "—", "该用户计成功，结果注明“已加入”"],
        ["404 资源不存在", "失败：提示目标组不存在，弹窗保持", "成功：视为“已不在该组”，结果注明", "失败：提示请求无效，记录原因"],
        ["400 参数错误", "失败：提示参数错误，记录 request_id", "失败：同左", "该用户计失败，不重试"],
        ["403 无权限", "失败：提示无权限或登录失效", "失败：同左", "整批中止并提示，避免持续无效调用"],
        ["超时 / 5xx", "失败：提示稍后重试（可安全重试）", "失败：同左", "该用户计失败，提示稍后重试"],
    ],
    [Cm(4.0), Cm(4.0), Cm(3.4), Cm(3.6)],
    aligns=["left", "left", "left", "left"],
    font_size=10,
)
ZW = {
    "ListGroupMembershipsForMember": "ListGroup\u200bMemberships\u200bFor\u200bMember",
    "CreateGroupMembership": "Create\u200bGroup\u200bMembership",
    "DeleteGroupMembership": "Delete\u200bGroup\u200bMembership",
}
for t in doc.tables:
    for row in t.rows:
        for cell in row.cells:
            for pp in cell.paragraphs:
                for r in pp.runs:
                    txt = r.text
                    for k, v in ZW.items():
                        if k in txt:
                            txt = txt.replace(k, v)
                    if txt != r.text:
                        r.text = txt

para("说明：加入与退出均为幂等操作，重复提交不会产生重复成员关系，因此“超时后重试”在业务上是安全的；但批量场景下 403 属于配置或授权问题，重试不会自愈，故整批中止并提示，避免产生大量无效调用。")
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
