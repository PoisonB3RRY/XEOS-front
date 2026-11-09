# -*- coding: utf-8 -*-
"""标定：带分页规则（表格整行不拆分、图片整体下移）的篇幅模型。"""
import math
import docx
from docx.text.paragraph import Paragraph
from docx.table import Table

USABLE_H = 24.6
USABLE_W = 15.0
REF = r"C:/Users/nickj/GitRepo/XEOS-front/docs/IAM身份中心-存量用户组迁移-需求规格说明书_V1.0.docx"

d = docx.Document(REF)
body = d.element.body

toc_pages = {}
for p in d.paragraphs:
    if p.style.name.startswith("toc") and "\t" in p.text:
        name, pg = p.text.rsplit("\t", 1)
        try:
            toc_pages[name.strip()] = int(pg)
        except ValueError:
            pass

CHECK = ["2.1 OBS 用户组管理列表页", "2.2 存量单个用户加入目标用户组", "3 接口需求",
         "4 业务流程", "4.5 接口结果与页面判定的对应关系"]


def units(s):
    return sum(1.0 if ord(c) > 127 else 0.5 for c in s)


def build_blocks():
    blocks = []
    started = False
    for c in body.iterchildren():
        if not started:
            if c.tag.endswith('}p') and Paragraph(c, d).text.strip() == '1 引言':
                started = True
            else:
                continue
        if c.tag.endswith('}p'):
            p = Paragraph(c, d)
            if 'w:type="page"' in c.xml:
                blocks.append(("page", None))
                continue
            t = p.text.strip()
            st = p.style.name
            if c.xpath('.//pic:pic'):
                ext = c.xpath('.//wp:extent')
                if ext:
                    w = int(ext[0].get('cx')) / 360000.0
                    hh = int(ext[0].get('cy')) / 360000.0
                    blocks.append(("img", (w, hh)))
                continue
            if not t:
                blocks.append(("space", 12))
                continue
            if st.startswith('Heading'):
                blocks.append(("head", (int(st.split()[-1]), t)))
                continue
            sz = 12
            for r in p.runs:
                if r.font.size:
                    sz = r.font.size.pt
                    break
            ind = 0.0
            pPr = c.find('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}pPr')
            if pPr is not None:
                i = pPr.find('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}ind')
                if i is not None:
                    fc = i.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}firstLineChars')
                    if fc:
                        ind = int(fc) / 100.0
            sb = p.paragraph_format.space_before.pt if p.paragraph_format.space_before else 0
            sa = p.paragraph_format.space_after.pt if p.paragraph_format.space_after else 0
            blocks.append(("text", (t, sz, ind, sb, sa)))
        elif c.tag.endswith('}tbl'):
            tb = Table(c, d)
            widths = [(cell.width.cm if cell.width else 3.0) for cell in tb.rows[0].cells]
            rows = []
            for r in tb.rows:
                rows.append([cell.text for cell in r.cells])
            blocks.append(("table", (widths, rows)))
    return blocks


BLOCKS = build_blocks()


def simulate(LH, TBL_LH, run):
    h = 0.0
    pages = {}
    for kind, data in BLOCKS:
        rem = USABLE_H - (h % USABLE_H)
        if kind == "page":
            h = math.ceil(h / USABLE_H - 1e-9) * USABLE_H
            continue
        if kind == "img":
            w, hh = data
            need = hh + 0.75  # 图 + 图注
            if need > rem:
                h += rem
            h += hh + 0.75
            continue
        if kind == "table":
            widths, rows = data
            hdr = None
            for idx, r in enumerate(rows):
                mx = 1
                for i, txt in enumerate(r):
                    if i >= len(widths):
                        break
                    limit = (widths[i] - 0.38) / (10.5 / 28.35)
                    mx = max(mx, math.ceil(units(txt) / limit))
                rh = mx * 10.5 * TBL_LH / 28.35 + 4 / 28.35
                if idx == 0:
                    hdr = rh
                rem = USABLE_H - (h % USABLE_H)
                if rh > rem and rh < USABLE_H:
                    h += rem
                    if idx > 0 and hdr:
                        h += hdr
                h += rh
            h += 0.26
            continue
        if kind == "space":
            h += data * LH / 28.35
            continue
        if kind == "head":
            lvl, t = data
            sz = {1: 16, 2: 14, 3: 12, 4: 12}.get(lvl, 12)
            before = {1: 18, 2: 14, 3: 10, 4: 8}.get(lvl, 8)
            after = {1: 10, 2: 8, 3: 6, 4: 4}.get(lvl, 4)
            limit = USABLE_W / (sz / 28.35)
            lines = max(1, math.ceil(units(t) / limit))
            hh = lines * sz * LH / 28.35 + (before + after) / 28.35
            rem = USABLE_H - (h % USABLE_H)
            if hh + 1.0 > rem:
                h += rem
            for label in CHECK:
                if t.startswith(label) and label not in pages:
                    pages[label] = 1 + int(h // USABLE_H)
            h += hh
            continue
        t, sz, ind, sb, sa = data
        limit = USABLE_W / (sz / 28.35)
        lines = max(1, math.ceil((units(t) + ind) / limit))
        h += lines * sz * LH / 28.35 + (sb + sa) / 28.35
    return h / USABLE_H, pages


best = None
for LH in [x / 100 for x in range(180, 221, 2)]:
    for TL in [x / 100 for x in range(120, 161, 4)]:
        tot, pages = simulate(LH, TL, None)
        err = sum(abs(pages.get(k, 0) - toc_pages.get(k, 0)) for k in CHECK)
        err += abs(tot - 35) * 0.5
        if best is None or err < best[0]:
            best = (err, LH, TL, tot, dict(pages))
print("best err=%.1f LH=%.2f TBL=%.2f total=%.1f (实际35)" % best[:4])
for k in CHECK:
    print("  %-32s 预测 p%-3d 实际 p%d" % (k[:30], best[4].get(k, 0), toc_pages.get(k, 0)))
