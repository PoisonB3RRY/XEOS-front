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
    for i, h in enumerate(header):
        c = hdr.cells[i]
        c.width = widths[i]
        cell_text(c, h, bold=True, size=font_size, align="center")
        shade(c, header_fill)

    for row in rows:
        cells = t.add_row().cells
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
