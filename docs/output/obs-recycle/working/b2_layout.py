# -*- coding: utf-8 -*-
"""《OBS 回收站 需求规格说明书》正文内容与版面编排。"""
import math
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from PIL import Image

from b1_base import (add_table, fmt_run, indent_chars, field_chars, cell_text,
                     shade, set_table_borders, IMGDIR, USABLE_W, SONG, ASCII_FONT, MONO)


# ---------------------------------------------------------------- 内容助手

_seq = {"bm": 0}


def _bookmark(p, name):
    start = OxmlElement("w:bookmarkStart")
    start.set(qn("w:id"), str(9000 + _seq["bm"]))
    start.set(qn("w:name"), name)
    end = OxmlElement("w:bookmarkEnd")
    end.set(qn("w:id"), str(9000 + _seq["bm"]))
    pPr = p._p.find(qn("w:pPr"))
    if pPr is not None:
        pPr.addnext(start)
    else:
        p._p.insert(0, start)
    p._p.append(end)


def h(doc, text, level, m=None):
    p = doc.add_paragraph(text, style="Heading %d" % level)
    _seq["bm"] += 1
    name = "_Toc9%05d" % _seq["bm"]
    _bookmark(p, name)
    if m is not None:
        page = m.heading(text, level)
        m.toc.append((level, text, name, page))
    return p


def para(doc, text, first=200, size=12, bold=False, align="justify",
         space_after=0, space_before=0, m=None):
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
    if m is not None:
        m.text(text, size, indent=(2 if first else 0), before=space_before, after=space_after)
    return p


def lead(doc, label, text, m=None):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 1.5
    indent_chars(p, first=200)
    fmt_run(p.add_run(label), size=12, bold=True)
    fmt_run(p.add_run(text), size=12)
    if m is not None:
        m.text(label + text, 12)
    return p


def steps(doc, items, m=None):
    for i, it in enumerate(items, 1):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        indent_chars(p, left=200, hanging=200)
        fmt_run(p.add_run("%d、%s" % (i, it)), size=12)
        if m is not None:
            m.text("%d、" % i + it, 12, indent=2)


def bullets(doc, items, mark="●", m=None):
    for it in items:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        indent_chars(p, left=300, hanging=100)
        fmt_run(p.add_run(mark + " "), size=10)
        if isinstance(it, tuple):
            fmt_run(p.add_run(it[0]), size=12, bold=True)
            fmt_run(p.add_run(it[1]), size=12)
            txt = it[0] + it[1]
        else:
            fmt_run(p.add_run(it), size=12)
            txt = it
        if m is not None:
            m.text("● " + txt, 12, indent=3)


def page_break(doc):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    r = p.add_run()
    fmt_run(r, size=1)
    br = OxmlElement("w:br")
    br.set(qn("w:type"), "page")
    r._r.append(br)


def figure(doc, name, caption, width_cm=12.0, m=None):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.first_line_indent = Pt(0)
    p.paragraph_format.keep_with_next = True
    run = p.add_run()
    run.add_picture(path_of(name), width=Cm(width_cm))
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
    except Exception:
        pass
    cap = doc.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.paragraph_format.space_before = Pt(2)
    cap.paragraph_format.space_after = Pt(10)
    cap.paragraph_format.line_spacing = 1.0
    cap.paragraph_format.first_line_indent = Pt(0)
    fmt_run(cap.add_run(caption), size=10.5)
    if m is not None:
        m.figure(width_cm, name, caption)
    return cap


def path_of(name):
    import os
    return os.path.join(IMGDIR, name)


def ui_table(doc, rows, m=None, widths=(3.8, 11.2)):
    add_table(doc, ["界面元素", "说明与交互要求"], rows,
              [Cm(widths[0]), Cm(widths[1])], aligns=["left", "left"], font_size=10)
    if m is not None:
        m.table([["界面元素", "说明与交互要求"]] + rows, list(widths), font=10)


def std_table(doc, header, rows, widths, aligns=None, font=10.5, m=None):
    add_table(doc, header, rows, [Cm(w) for w in widths],
              aligns=aligns, font_size=font)
    if m is not None:
        m.table([header] + rows, list(widths), font=font)


def json_block(doc, lines, m=None):
    t = doc.add_table(rows=1, cols=1)
    t.autofit = False
    tblPr = t._tbl.tblPr
    layout = OxmlElement("w:tblLayout")
    layout.set(qn("w:type"), "fixed")
    tblPr.append(layout)
    set_table_borders(t, sz=4, color="808080")
    cell = t.rows[0].cells[0]
    cell.width = Cm(15.0)
    shade(cell, "F7F7F7")
    cell.text = ""
    for i, ln in enumerate(lines):
        p = cell.paragraphs[0] if i == 0 else cell.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.0
        fmt_run(p.add_run(ln), size=9, cn=MONO, latin=MONO)
    tail = doc.add_paragraph()
    tail.paragraph_format.space_before = Pt(0)
    tail.paragraph_format.space_after = Pt(0)
    tail.paragraph_format.line_spacing = 0.6
    fmt_run(tail.add_run(""), size=6)
    if m is not None:
        m.raw(len(lines) * 9 * 1.25 / 28.35 + 0.4)


# ---------------------------------------------------------------- 封面


def cover(doc):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(120)
    p.paragraph_format.space_after = Pt(0)
    fmt_run(p.add_run(""), size=12)

    for _ in range(19):
        q = doc.add_paragraph()
        q.paragraph_format.line_spacing = 1.0
        fmt_run(q.add_run(""), size=12)

    def line(text, size, after=0, before=0, bold=True):
        q = doc.add_paragraph()
        q.alignment = WD_ALIGN_PARAGRAPH.CENTER
        q.paragraph_format.space_before = Pt(before)
        q.paragraph_format.space_after = Pt(after)
        q.paragraph_format.line_spacing = 1.2
        pPr = q._p.get_or_add_pPr()
        for tag in ("w:autoSpaceDE", "w:autoSpaceDN"):
            e = OxmlElement(tag)
            e.set(qn("w:val"), "0")
            pPr.insert_element_before(e, "w:bidi", "w:adjustRightInd", "w:snapToGrid",
                                      "w:spacing", "w:ind", "w:contextualSpacing",
                                      "w:mirrorIndents", "w:suppressOverlap", "w:jc",
                                      "w:textDirection", "w:textAlignment",
                                      "w:textboxTightWrap", "w:outlineLvl", "w:divId",
                                      "w:cnfStyle", "w:rPr", "w:sectPr")
        fmt_run(q.add_run(text), size=size, bold=bold)
        return q

    line("上海浦东发展银行", 28, after=26)
    line("IaaS研发需求", 26, after=20)
    line("需求规格说明书", 26, after=14)

    q = doc.add_paragraph()
    q.alignment = WD_ALIGN_PARAGRAPH.CENTER
    q.paragraph_format.line_spacing = 1.2
    q.paragraph_format.space_before = Pt(4)
    q.paragraph_format.space_after = Pt(34)
    fmt_run(q.add_run("（华为云 OBS 对象存储桶回收站）"), size=15, bold=False)

    q = doc.add_paragraph()
    q.alignment = WD_ALIGN_PARAGRAPH.CENTER
    q.paragraph_format.line_spacing = 1.2
    fmt_run(q.add_run("V1.0"), size=15, bold=False)

    page_break(doc)


def rules_page(doc):
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
        [
            ["1", "创建全文", "2026-11-09", "V1.0", "", ""],
            ["2", "更新回收/恢复弹窗横向表格及按钮、去掉回收站状态列、更新截图；deny* 策略改用 Principal: \"*\"；新增 90 天静默期及到期前 10/5/1 天邮件通知销毁章节", "2026-11-10", "V1.0", "", ""],
        ],
        [Cm(1.5), Cm(6.0), Cm(2.8), Cm(1.8), Cm(1.45), Cm(1.45)],
        aligns=["center"] * 6,
    )

    page_break(doc)


# ---------------------------------------------------------------- 目录


def toc_page(doc, entries, start_page, m=None):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(16)
    fmt_run(p.add_run("目　　录"), size=16, bold=True)

    if not entries:
        q = doc.add_paragraph()
        q.paragraph_format.line_spacing = 1.5
        field_chars(q, 'TOC \\o "1-4" \\h \\z \\u', "（目录）", size=12)
        page_break(doc)
        return

    for idx, (level, text, bm, rel_page) in enumerate(entries):
        q = doc.add_paragraph()
        q.paragraph_format.line_spacing = 1.5
        q.paragraph_format.space_before = Pt(0)
        q.paragraph_format.space_after = Pt(0)
        q.paragraph_format.left_indent = Pt(12 * 1.0 * (level - 1))
        q.paragraph_format.tab_stops.add_tab_stop(
            Cm(14.95), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)

        if idx == 0:
            r = q.add_run()
            fmt_run(r, size=10.5)
            fc = OxmlElement("w:fldChar")
            fc.set(qn("w:fldCharType"), "begin")
            r._r.append(fc)
            r = q.add_run()
            fmt_run(r, size=10.5)
            it = OxmlElement("w:instrText")
            it.set(qn("xml:space"), "preserve")
            it.text = ' TOC \\o "1-4" \\h \\z \\u '
            r._r.append(it)
            r = q.add_run()
            fmt_run(r, size=10.5)
            sep = OxmlElement("w:fldChar")
            sep.set(qn("w:fldCharType"), "separate")
            r._r.append(sep)

        # HYPERLINK 域
        r = q.add_run()
        fmt_run(r, size=10.5)
        fc = OxmlElement("w:fldChar")
        fc.set(qn("w:fldCharType"), "begin")
        r._r.append(fc)
        r = q.add_run()
        fmt_run(r, size=10.5)
        it = OxmlElement("w:instrText")
        it.set(qn("xml:space"), "preserve")
        it.text = 'HYPERLINK \\l "%s"' % bm
        r._r.append(it)
        r = q.add_run()
        fmt_run(r, size=10.5)
        sep = OxmlElement("w:fldChar")
        sep.set(qn("w:fldCharType"), "separate")
        r._r.append(sep)

        fmt_run(q.add_run(text), size=10.5)
        q.add_run().add_tab()

        # PAGEREF 域
        r = q.add_run()
        fmt_run(r, size=10.5)
        fc = OxmlElement("w:fldChar")
        fc.set(qn("w:fldCharType"), "begin")
        r._r.append(fc)
        r = q.add_run()
        fmt_run(r, size=10.5)
        it = OxmlElement("w:instrText")
        it.set(qn("xml:space"), "preserve")
        it.text = " PAGEREF %s \\h " % bm
        r._r.append(it)
        r = q.add_run()
        fmt_run(r, size=10.5)
        sep = OxmlElement("w:fldChar")
        sep.set(qn("w:fldCharType"), "separate")
        r._r.append(sep)
        fmt_run(q.add_run(str(start_page + rel_page)), size=10.5)
        for _ in range(2):
            r = q.add_run()
            fmt_run(r, size=10.5)
            end = OxmlElement("w:fldChar")
            end.set(qn("w:fldCharType"), "end")
            r._r.append(end)

    q = doc.add_paragraph()
    q.paragraph_format.space_before = Pt(0)
    q.paragraph_format.space_after = Pt(0)
    r = q.add_run()
    fmt_run(r, size=10.5)
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    r._r.append(end)

    page_break(doc)
