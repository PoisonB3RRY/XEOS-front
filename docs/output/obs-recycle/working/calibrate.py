# -*- coding: utf-8 -*-
"""用参考文档标定篇幅估算参数：比较预测页码与参考文档目录页码。"""
import math
import docx
from docx.text.paragraph import Paragraph
from docx.table import Table
from docx.shared import Emu

USABLE_H = 24.6
USABLE_W = 15.0
REF = r"C:/Users/nickj/GitRepo/XEOS-front/docs/IAM身份中心-存量用户组迁移-需求规格说明书_V1.0.docx"

d = docx.Document(REF)
body = d.element.body

# 目录页码
toc_pages = {}
for p in d.paragraphs:
    if p.style.name.startswith("toc"):
        t = p.text
        if "\t" in t:
            name, pg = t.rsplit("\t", 1)
            try:
                toc_pages[name.strip()] = int(pg)
            except ValueError:
                pass


def units(s):
    return sum(1.0 if ord(c) > 127 else 0.5 for c in s)


def measure(LH=1.5, TBL_LH=1.22, IMG_GAP=21/28.35, TITLE_H=0.0):
    h = 0.0
    rows = []
    started = False
    for c in body.iterchildren():
        if not started:
            if c.tag.endswith('}p'):
                if Paragraph(c, d).text.strip() == '1 引言':
                    started = True
                else:
                    continue
            else:
                continue
        if c.tag.endswith('}p'):
            p = Paragraph(c, d)
            # 分页
            if 'w:type="page"' in c.xml:
                h = math.ceil(h / USABLE_H - 1e-9) * USABLE_H
                continue
            t = p.text.strip()
            if not t:
                # 空段落按行高计入
                sz = 12
                h += sz * LH / 28.35
                continue
            st = p.style.name
            if st.startswith('Heading'):
                lvl = int(st.split()[-1])
                sz = {1: 16, 2: 14, 3: 12, 4: 12}.get(lvl, 12)
                before = {1: 18, 2: 14, 3: 10, 4: 8}.get(lvl, 8)
                after = {1: 10, 2: 8, 3: 6, 4: 4}.get(lvl, 4)
                limit = USABLE_W / (sz / 28.35)
                lines = max(1, math.ceil(units(t) / limit))
                h += lines * sz * LH / 28.35 + (before + after) / 28.35
                rows.append((t, 1 + int(h // USABLE_H)))
                continue
            # 图片段落
            if c.xpath('.//pic:pic'):
                for sh in p._p.xpath('.//wp:extent'):
                    w = int(sh.get('cx')) / 360000.0
                    hh = int(sh.get('cy')) / 360000.0
                    h += hh + IMG_GAP
                continue
            # 普通段落：字号取首个 run
            sz = 12
            for r in p.runs:
                if r.font.size:
                    sz = r.font.size.pt
                    break
            lead = 0
            pPr = p._p.find('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}pPr')
            ind = 0
            if pPr is not None:
                i = pPr.find('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}ind')
                if i is not None:
                    fc = i.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}firstLineChars')
                    if fc:
                        ind = int(fc) / 100.0
            limit = USABLE_W / (sz / 28.35)
            lines = max(1, math.ceil((units(t) + ind) / limit))
            sb = p.paragraph_format.space_before.pt if p.paragraph_format.space_before else 0
            sa = p.paragraph_format.space_after.pt if p.paragraph_format.space_after else 0
            h += lines * sz * LH / 28.35 + (sb + sa) / 28.35
        elif c.tag.endswith('}tbl'):
            tb = Table(c, d)
            widths = []
            for cell in tb.rows[0].cells:
                widths.append((cell.width.cm if cell.width else 3.0))
            if not widths:
                continue
            for r in tb.rows:
                mx = 1
                for i, cell in enumerate(r.cells):
                    if i >= len(widths):
                        break
                    limit = (widths[i] - 0.38) / (10.5 / 28.35)
                    mx = max(mx, math.ceil(units(cell.text) / limit))
                h += mx * 10.5 * TBL_LH / 28.35 + 4 / 28.35
            h += 0.26
    return h, rows


for LH in (1.5, 1.75, 1.9, 2.0):
    h, rows = measure(LH=LH)
    print("LH=%.2f 总高=%.1fcm → 正文页数≈%.1f (实际 35)" % (LH, h, h / USABLE_H))
    for label in ("2.1 OBS 用户组管理列表页", "3 接口需求", "4 业务流程", "4.5 接口结果与页面判定的对应关系"):
        for t, pg in rows:
            if t.startswith(label):
                print("   %-40s 预测 p%-3d 实际 p%d" % (t[:38], 4 + pg, toc_pages.get(label, -1)))
                break
