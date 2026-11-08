# -*- coding: utf-8 -*-
"""Stage2 排版：final_draft.md → doc-typeset 规范 HTML（business-report 模板 + business-modern tokens）。"""
import re, io, os, html as htmllib

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD = os.path.join(BASE, "stage1", "final_draft.md")
OUT = os.path.join(BASE, "stage2", "formatted-IAM存量用户组迁移需求规格说明书.html")

src = io.open(MD, encoding="utf-8").read()
lines = src.split("\n")

def inline(t):
    t = htmllib.escape(t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    return t.replace("`", "")

blocks, i, doc_title = [], 0, ""
while i < len(lines):
    s = lines[i].strip()
    if not s:
        i += 1; continue
    if s.startswith("# ") and not doc_title:
        doc_title = s[2:].strip(); i += 1; continue
    if s.startswith("### "):
        blocks.append(("h2", s[4:].strip())); i += 1; continue
    if s.startswith("#### "):
        blocks.append(("h3", s[5:].strip())); i += 1; continue
    if s.startswith("## "):
        blocks.append(("h1", s[3:].strip())); i += 1; continue
    if s.startswith("|"):
        rows = []
        while i < len(lines) and lines[i].strip().startswith("|"):
            rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
            i += 1
        data = [r for r in rows if not all(re.fullmatch(r":?-{2,}:?", c or "-") for c in r)]
        if data:
            blocks.append(("table", data))
        continue
    if s.startswith("> "):
        buf = []
        while i < len(lines) and lines[i].strip().startswith(">"):
            buf.append(lines[i].strip().lstrip(">").strip()); i += 1
        blocks.append(("quote", " ".join(buf))); continue
    if re.match(r"^\d+\.\s", s):
        items = []
        while i < len(lines) and re.match(r"^\s*\d+\.\s", lines[i]):
            items.append(re.sub(r"^\s*\d+\.\s", "", lines[i])); i += 1
        blocks.append(("ol", items)); continue
    if s.startswith("- "):
        items = []
        while i < len(lines) and re.match(r"^\s*-\s+", lines[i]):
            items.append(re.sub(r"^\s*-\s+", "", lines[i])); i += 1
        blocks.append(("ul", items)); continue
    blocks.append(("p", s)); i += 1

sec_id, toc = 0, []
for idx, (kind, payload) in enumerate(blocks):
    if kind in ("h1", "h2"):
        sec_id += 1
        sid = "section-%d" % sec_id
        toc.append((1 if kind == "h1" else 2, payload, sid))
        blocks[idx] = (kind, (payload, sid))

css = """
@page { @bottom-center { content: counter(page); } }
@page cover { @bottom-center { content: none; } }
section[role="cover"] { page: cover; }

:root {
  /* 字号 */
  --fs-h1: 16pt; --fs-h2: 13.5pt; --fs-h3: 12pt; --fs-body: 12pt;
  --fs-table: 9pt; --fs-quote: 11pt; --fs-summary: 11.5pt;
  --fs-cover-cat: 12pt; --fs-cover-title: 25pt; --fs-cover-sub: 14pt; --fs-cover-meta: 10.5pt;
  --fs-toc-title: 16pt; --fs-toc-item: 11pt;
  /* 字体 */
  --ff-heading: "SimHei", "黑体", sans-serif;
  --ff-body: "SimSun", "宋体", serif;
  /* 颜色 */
  --color-primary: #1565C0; --color-secondary: #0288D1;
  --color-heading: #1A237E; --color-text: #212121; --color-muted: #616161;
  --color-divider: #D6DCE5; --color-bg: #FFFFFF; --color-surface: #F2F5F9;
  --color-white: #FFFFFF;
  /* 间距 */
  --sp-paragraph: 0 0 0.55em 0;
  --sp-cover-top: 3.2cm; --sp-cover-cat: 0 0 18pt 0; --sp-cover-title: 0 0 10pt 0;
  --sp-cover-sub: 0 0 40pt 0; --sp-cover-line: 0 0 7pt 0; --sp-cover-foot: 52pt 0 0 0;
  --sp-toc-title: 0 0 16pt 0; --sp-toc-item: 0 0 4pt 0; --sp-toc-lv1: 8pt 0 4pt 0;
  --sp-toc-indent: 1.6em;
  --sp-h1: 20pt 0 12pt 0; --sp-h1-pad: 5pt 9pt;
  --sp-h2: 16pt 0 8pt 0; --sp-h3: 12pt 0 6pt 0;
  --sp-quote: 10pt 0 0.55em 0; --sp-quote-pad: 7pt 9pt;
  --sp-summary: 12pt 0 14pt 0; --sp-summary-pad: 9pt 11pt;
  --sp-list: 0 0 8pt 0; --sp-list-indent: 2.4em; --sp-li: 0 0 3pt 0;
  --sp-table: 8pt 0 12pt 0; --sp-cell: 4pt 5pt;
  /* 版式 */
  --lh-body: 1.65; --lh-tight: 1.45; --lh-toc: 1.55;
  --page-content-width: 16cm;
  --fw-bold: 700; --fw-normal: 400;
}

* { box-sizing: border-box; }

section[role="cover"] { padding: 0; }
.cover-wrap { padding-top: var(--sp-cover-top); }

.cover-category {
  font-family: var(--ff-heading); font-size: var(--fs-cover-cat); font-weight: var(--fw-bold);
  color: var(--color-primary); letter-spacing: 0.18em;
  text-align: center; text-indent: 0; margin: var(--sp-cover-cat);
}
.cover-title {
  font-family: var(--ff-heading); font-size: var(--fs-cover-title); font-weight: var(--fw-bold);
  color: var(--color-heading); line-height: var(--lh-tight);
  text-align: center; text-indent: 0; margin: var(--sp-cover-title);
}
.cover-subtitle {
  font-family: var(--ff-heading); font-size: var(--fs-cover-sub); font-weight: var(--fw-normal);
  color: var(--color-muted); text-align: center; text-indent: 0; margin: var(--sp-cover-sub);
}
.cover-meta {
  font-family: var(--ff-body); font-size: var(--fs-cover-meta); color: var(--color-text);
  text-align: center; text-indent: 0; margin: var(--sp-cover-line); line-height: var(--lh-body);
}
.cover-foot {
  font-family: var(--ff-body); font-size: var(--fs-cover-meta); color: var(--color-muted);
  text-align: center; text-indent: 0; margin: var(--sp-cover-foot);
}

.toc-title {
  font-family: var(--ff-heading); font-size: var(--fs-toc-title); font-weight: var(--fw-bold);
  color: var(--color-heading); text-align: center; text-indent: 0;
  margin: var(--sp-toc-title); letter-spacing: 0.12em;
}
.toc-list, .toc-list ol, .toc-list ul { list-style: none; list-style-type: none; margin: 0; padding-left: 0; }
.toc-list li {
  font-family: var(--ff-body); font-size: var(--fs-toc-item); color: var(--color-text);
  text-indent: 0; text-align: left; margin: var(--sp-toc-item); line-height: var(--lh-toc);
}
.toc-list > li.lv1 { font-family: var(--ff-heading); font-weight: var(--fw-bold); margin: var(--sp-toc-lv1); }
.toc-list ol { padding-left: var(--sp-toc-indent); }
.toc-list a { color: inherit; text-decoration: none; }

h1.section-header {
  font-family: var(--ff-heading); font-size: var(--fs-h1); font-weight: var(--fw-bold);
  color: var(--color-white); background: var(--color-primary);
  padding: var(--sp-h1-pad); margin: var(--sp-h1);
  text-indent: 0; text-align: left; line-height: var(--lh-tight);
}
h2 {
  font-family: var(--ff-heading); font-size: var(--fs-h2); font-weight: var(--fw-bold);
  color: var(--color-heading); margin: var(--sp-h2);
  text-indent: 0; text-align: left; line-height: var(--lh-tight);
}
h3 {
  font-family: var(--ff-heading); font-size: var(--fs-h3); font-weight: var(--fw-bold);
  color: var(--color-text); margin: var(--sp-h3);
  text-indent: 0; text-align: left; line-height: var(--lh-tight);
}
p {
  font-family: var(--ff-body); font-size: var(--fs-body); color: var(--color-text);
  text-indent: 2em; text-align: justify; line-height: var(--lh-body); margin: var(--sp-paragraph);
}
p.executive-summary {
  font-family: var(--ff-body); font-size: var(--fs-summary); color: var(--color-text);
  text-indent: 0; text-align: justify; line-height: var(--lh-body);
  background: var(--color-surface); border-left: 4px solid var(--color-primary);
  padding: var(--sp-summary-pad); margin: var(--sp-summary);
}
p.quote {
  font-family: var(--ff-body); font-size: var(--fs-quote); color: var(--color-text);
  text-indent: 0; text-align: left; background: var(--color-surface);
  border-left: 3px solid var(--color-primary);
  padding: var(--sp-quote-pad); margin: var(--sp-quote);
}
ol, ul { margin: var(--sp-list); padding-left: var(--sp-list-indent); }
li {
  font-family: var(--ff-body); font-size: var(--fs-body); color: var(--color-text);
  text-indent: 0; text-align: justify; line-height: var(--lh-body); margin: var(--sp-li);
}
strong { font-weight: var(--fw-bold); }

table { width: 100%; border-collapse: collapse; margin: var(--sp-table); }
thead { display: table-header-group; }
th {
  font-family: var(--ff-heading); font-size: var(--fs-table); font-weight: var(--fw-bold);
  color: var(--color-heading); background: var(--color-surface);
  border: 1px solid var(--color-divider); padding: var(--sp-cell);
  text-indent: 0; text-align: left; line-height: var(--lh-tight);
}
td {
  font-family: var(--ff-body); font-size: var(--fs-table); color: var(--color-text);
  border: 1px solid var(--color-divider); padding: var(--sp-cell);
  text-indent: 0; text-align: left; line-height: var(--lh-tight);
}
"""

def cell(tag, txt):
    return "<%s>%s</%s>" % (tag, inline(txt), tag)

def render_table(rows):
    ncol = max(len(r) for r in rows)
    pad = lambda r: r + [""] * (ncol - len(r))
    out = ["<table>", "<thead><tr>"]
    out += [cell("th", c) for c in pad(rows[0])]
    out += ["</tr></thead>", "<tbody>"]
    for r in rows[1:]:
        out.append("<tr>" + "".join(cell("td", c) for c in pad(r)) + "</tr>")
    out.append("</tbody></table>")
    return "\n".join(out)

body = []
for kind, payload in blocks:
    if kind == "h1":
        body.append('<h1 class="section-header" id="%s">%s</h1>' % (payload[1], htmllib.escape(payload[0])))
    elif kind == "h2":
        body.append('<h2 id="%s">%s</h2>' % (payload[1], htmllib.escape(payload[0])))
    elif kind == "h3":
        body.append("<h3>%s</h3>" % htmllib.escape(payload))
    elif kind == "p":
        body.append("<p>%s</p>" % inline(payload))
    elif kind == "quote":
        body.append('<p class="quote">&nbsp;&nbsp;%s</p>' % inline(payload))
    elif kind == "ol":
        body.append("<ol>" + "".join("<li>%s</li>" % inline(x) for x in payload) + "</ol>")
    elif kind == "ul":
        body.append("<ul>" + "".join("<li>%s</li>" % inline(x) for x in payload) + "</ul>")
    elif kind == "table":
        body.append(render_table(payload))

toc_parts = ['<ol class="toc-list">']
k = 0
while k < len(toc):
    lvl, text, sid = toc[k]
    sub, j = [], k + 1
    while j < len(toc) and toc[j][0] == 2:
        sub.append(toc[j]); j += 1
    if lvl == 1:
        piece = '<li class="lv1"><a href="#%s">%s</a>' % (sid, htmllib.escape(text))
        if sub:
            piece += "<ol>" + "".join(
                '<li><a href="#%s">%s</a></li>' % (s2, htmllib.escape(t2)) for _, t2, s2 in sub
            ) + "</ol>"
        piece += "</li>"
        toc_parts.append(piece); k = j
    else:
        toc_parts.append('<li class="lv1"><a href="#%s">%s</a></li>' % (sid, htmllib.escape(text)))
        k += 1
toc_parts.append("</ol>")

summary = (
    '<p class="executive-summary">&nbsp;&nbsp;<strong>摘　要</strong>　'
    '本文档将已确认的业务方案《存量用户组迁移方案（IAM 身份中心）》转化为可开发、可测试、可验收的需求规格，'
    '覆盖迁移配置校验、用户退出旧组、用户加入新组、批量编排、执行记录与断点续跑六项功能，'
    '共涉及 4 个 IAM 身份中心接口（ListGroupMembershipsForMember、DeleteGroupMembership、ListGroups、CreateGroupMembership）。'
    '核心设计约束为：批量迁移必须按“先加入新组、再退出旧组”执行，以保证用户权限只增不减；'
    '解绑所需的成员关系标识只能来自查询结果；迁移流程止于写接口成功返回，本期不做校验与抽查。'
    '主要风险集中在“无事后校验导致误操作不可自动发现”与“目标组同名导致误绑”两项，已通过结构化留痕、预演模式与选组中止策略缓解；'
    '性能指标、并发上限、留存期等 8 项参数待业务与运维确认后固化。'
    '</p>'
)

cover = """
<section role="cover">
  <div class="cover-wrap">
    <p class="cover-category">需 求 文 档</p>
    <p class="cover-title">华为云 IAM 身份中心<br>存量用户组迁移<br>需求规格说明书</p>
    <p class="cover-subtitle">用户退出旧组 / 用户加入新组</p>
    <p class="cover-meta">文档编号　　SRS-IAM-IS-MIGRATION-001</p>
    <p class="cover-meta">文档版本　　V1.0（初稿）</p>
    <p class="cover-meta">编制日期　　2026 年 11 月 8 日</p>
    <p class="cover-meta">编制依据　　《存量用户组迁移方案（IAM 身份中心）》</p>
    <p class="cover-meta">　　　　　　《IAM 身份中心 API 参考》（版本 02）</p>
    <p class="cover-meta">密　　级　　内部</p>
    <p class="cover-foot">本文件为产品设计参考，具体实施请结合公司合规与法务要求确认</p>
  </div>
</section>
"""

doc = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="docx-page-size" content="A4">
<title>%(title)s</title>
<style>%(css)s</style>
</head>
<body>
%(cover)s
<section role="cover">
<nav class="doc-toc" aria-label="文档目录">
<p class="toc-title">目　录</p>
%(toc)s
</nav>
</section>
<section role="body" class="report-body" data-page-restart="1">
%(summary)s
%(body)s
</section>
</body>
</html>
""" % {"title": htmllib.escape(doc_title), "css": css, "cover": cover,
       "toc": "\n".join(toc_parts), "summary": summary, "body": "\n".join(body)}

io.open(OUT, "w", encoding="utf-8", newline="\n").write(doc)
print("ok:", len(doc), "chars,", len(blocks), "blocks,", len(toc), "toc entries")
