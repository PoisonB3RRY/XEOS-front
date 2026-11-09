# -*- coding: utf-8 -*-
"""按浦发银行《IaaS研发需求 需求规格说明书》模板编排 OBS 回收站文档。"""
import os
import math
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
IMGDIR = os.path.join(HERE, "img")
OUT = r"C:/Users/nickj/GitRepo/XEOS-front/docs/output/obs-recycle/stage3/OBS回收站-需求规格说明书_V1.0.docx"

SONG = "宋体"
ASCII_FONT = "Times New Roman"
MONO = "Consolas"

USABLE_H = 24.6      # 正文可用高度 cm
USABLE_W = 15.0      # 正文可用宽度 cm

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


def field_chars(p, instr, placeholder="", size=10.5, bold=False):
    def _run():
        r = p.add_run()
        fmt_run(r, size=size, bold=bold)
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


def cell_text(cell, text, bold=False, size=10.5, align="left", color=None, mono=False):
    cell.text = ""
    p = cell.paragraphs[0]
    p.alignment = {"left": WD_ALIGN_PARAGRAPH.LEFT,
                   "center": WD_ALIGN_PARAGRAPH.CENTER,
                   "right": WD_ALIGN_PARAGRAPH.RIGHT}[align]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
    lines = str(text).split("\n")
    for i, ln in enumerate(lines):
        if i:
            p = cell.add_paragraph()
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
            p.alignment = {"left": WD_ALIGN_PARAGRAPH.LEFT,
                           "center": WD_ALIGN_PARAGRAPH.CENTER,
                           "right": WD_ALIGN_PARAGRAPH.RIGHT}[align]
        run = p.add_run(ln)
        fmt_run(run, size=size, bold=bold, color=color,
                cn=(MONO if mono else SONG), latin=(MONO if mono else ASCII_FONT))
    tcPr = cell._tc.get_or_add_tcPr()
    va = OxmlElement("w:vAlign")
    va.set(qn("w:val"), "center")
    tcPr.append(va)


def add_table(doc, header, rows, widths, font_size=10.5, aligns=None, header_fill="D9D9D9"):
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
    trPr.append(OxmlElement("w:tblHeader"))
    trPr.append(OxmlElement("w:cantSplit"))
    for i, h in enumerate(header):
        c = hdr.cells[i]
        c.width = widths[i]
        cell_text(c, h, bold=True, size=font_size, align="center")
        shade(c, header_fill)
        for _p in c.paragraphs:
            _p.paragraph_format.keep_with_next = True

    for row in rows:
        _r = t.add_row()
        _r._tr.get_or_add_trPr().append(OxmlElement("w:cantSplit"))
        cells = _r.cells
        for i, v in enumerate(row):
            cells[i].width = widths[i]
            cell_text(cells[i], v, size=font_size, align=aligns[i])

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 0.6
    fmt_run(p.add_run(""), size=6)
    return t


# ---------------------------------------------------------------- 篇幅估算


class Meter:
    """带分页规则的篇幅估算：表格整行不拆分、图片整体下移、标题不与正文分离。"""

    LH = 2.00          # 行高系数（已按参考文档标定）
    TBL_LH = 1.32      # 表格行高系数
    CAP_H = 0.72       # 图注 + 间距

    def __init__(self):
        self.h = 0.0
        self.toc = []          # (level, text, bookmark, rel_page)

    # ---------------------------------------------------------- 基础
    @staticmethod
    def _units(s):
        return sum(1.0 if ord(c) > 127 else 0.5 for c in s)

    def _remain(self):
        return USABLE_H - (self.h % USABLE_H)

    def _jump(self, need):
        if need > self._remain():
            self.h += self._remain()

    def rel_page(self):
        return int(self.h // USABLE_H)

    def raw(self, cm):
        self._jump(cm)
        self.h += cm

    # ---------------------------------------------------------- 元素
    def text(self, s, size=12, indent=2, before=0, after=0):
        limit = USABLE_W / (size / 28.35)
        lines = max(1, math.ceil((self._units(s) + indent) / limit))
        self.h += lines * size * self.LH / 28.35 + (before + after) / 28.35

    def heading(self, s, level):
        sizes = {1: 16, 2: 14, 3: 12, 4: 12}
        before = {1: 18, 2: 14, 3: 10, 4: 8}
        after = {1: 10, 2: 8, 3: 6, 4: 4}
        sz = sizes.get(level, 12)
        limit = USABLE_W / (sz / 28.35)
        lines = max(1, math.ceil(self._units(s) / limit))
        hh = lines * sz * self.LH / 28.35 + (before[level] + after[level]) / 28.35
        if hh + 1.0 > self._remain():
            self.h += self._remain()
        page = self.rel_page()
        self.h += hh
        return page

    def table(self, rows, widths, font=10.5):
        hdr = None
        for idx, r in enumerate(rows):
            mx = 1
            for i, v in enumerate(r):
                if i >= len(widths):
                    break
                limit = (widths[i] - 0.38) / (font / 28.35)
                mx = max(mx, math.ceil(self._units(str(v)) / limit))
            rh = mx * font * self.TBL_LH / 28.35 + 4 / 28.35
            if idx == 0:
                hdr = rh
            if rh > self._remain() and rh < USABLE_H:
                self.h += self._remain()
                if idx > 0 and hdr:
                    self.h += hdr
            self.h += rh
        self.h += 0.26

    def figure(self, w_cm, img, caption):
        with Image.open(os.path.join(IMGDIR, img)) as im:
            pw, ph = im.size
        fh = w_cm * ph / pw
        if fh + self.CAP_H > self._remain() and fh + self.CAP_H < USABLE_H:
            self.h += self._remain()
        self.h += fh + self.CAP_H
        self.text(caption, 10.5, indent=0)

    def new_page(self):
        self.h = math.ceil(self.h / USABLE_H - 1e-9) * USABLE_H


# ---------------------------------------------------------------- 文档骨架


def make_doc():
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Cm(21), Cm(29.7)
    sec.top_margin, sec.bottom_margin = Cm(2.54), Cm(2.54)
    sec.left_margin, sec.right_margin = Cm(3.0), Cm(3.0)
    sec.header_distance, sec.footer_distance = Cm(1.35), Cm(1.75)

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

    sec.different_first_page_header_footer = True
    _build_header(sec.header)
    _build_footer(sec.footer)
    _build_header(sec.first_page_header)
    if sec.first_page_footer is not None:
        sec.first_page_footer.is_linked_to_previous = False
        for p in list(sec.first_page_footer.paragraphs):
            p._p.getparent().remove(p._p)
        sec.first_page_footer.add_paragraph()

    settings = doc.settings.element
    uf = OxmlElement("w:updateFields")
    uf.set(qn("w:val"), "true")
    settings.append(uf)
    return doc


def _build_header(header):
    header.is_linked_to_previous = False
    for p in list(header.paragraphs):
        p._p.getparent().remove(p._p)
    t = header.add_table(rows=1, cols=2, width=Cm(USABLE_W))
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

    tail = header.add_paragraph()
    tail.paragraph_format.space_before = Pt(0)
    tail.paragraph_format.space_after = Pt(0)
    tail.paragraph_format.line_spacing = Pt(6)
    fmt_run(tail.add_run(""), size=1)


def _build_footer(footer):
    footer.is_linked_to_previous = False
    for p in list(footer.paragraphs):
        p._p.getparent().remove(p._p)
    p = footer.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    field_chars(p, "PAGE", "1", size=10)
