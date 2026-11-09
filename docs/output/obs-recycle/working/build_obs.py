# -*- coding: utf-8 -*-
"""编排：两遍构建（第一遍估算页码，第二遍出稿）。"""
import math
from b1_base import make_doc, Meter, USABLE_H, OUT
import b2_layout as L
from b2_layout import cover, rules_page, toc_page
from b3_body_a import write_ch12
from b3_body_b import write_ch34


def toc_pages(entries):
    total = 1.9  # 目录标题占用
    for level, text, bm, rel in entries:
        avail = (14.95 - (level - 1) * 0.42 - 0.9)
        units = sum(1.0 if ord(c) > 127 else 0.5 for c in text)
        lines = max(1, math.ceil(units / (avail / 0.370)))
        total += lines * 10.5 * 1.5 / 28.35
    return max(1, math.ceil(total / USABLE_H))


def build(out_path=None, entries=None, body_start=None, meter_out=None):
    L._seq["bm"] = 0
    doc = make_doc()
    cover(doc)
    rules_page(doc)
    toc_page(doc, entries or [], body_start or 3)
    m = Meter()
    write_ch12(doc, m)
    write_ch34(doc, m)
    if meter_out is not None:
        meter_out.append(m)
    if out_path:
        doc.save(out_path)
    return doc


if __name__ == "__main__":
    # 第一遍：估算各标题的相对页码
    box = []
    build(entries=None, body_start=3, meter_out=box)
    m1 = box[0]
    entries = m1.toc
    tp = toc_pages(entries)
    body_start = 3 + tp
    print("目录页数 =", tp, " 正文起始页 =", body_start, " 标题条目 =", len(entries))
    # 第二遍：写最终文件
    build(out_path=OUT, entries=entries, body_start=body_start)
    print("saved:", OUT)
