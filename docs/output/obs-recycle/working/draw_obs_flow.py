# -*- coding: utf-8 -*-
"""绘制《OBS 回收站 需求规格说明书》业务流程图（PIL 直绘，无外部依赖）。"""
import os
import re
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img")
os.makedirs(OUT, exist_ok=True)

FONT_PATH = "C:/Windows/Fonts/msyh.ttc"
FS = 32
FS_LABEL = 27
F = ImageFont.truetype(FONT_PATH, FS, index=0)
FL = ImageFont.truetype(FONT_PATH, FS_LABEL, index=0)

LINE_H = int(FS * 1.34)
PAD_X = 26
MIN_H = 86

STYLE = {
    "start": dict(fill=(232, 239, 249), line=(68, 114, 196), radius=48, lw=4),
    "end": dict(fill=(232, 239, 249), line=(68, 114, 196), radius=48, lw=4),
    "process": dict(fill=(255, 255, 255), line=(120, 128, 140), radius=10, lw=3),
    "api": dict(fill=(234, 242, 252), line=(68, 114, 196), radius=10, lw=3),
    "sub": dict(fill=(255, 248, 232), line=(197, 138, 46), radius=10, lw=3),
    "decision": dict(fill=(255, 246, 230), line=(197, 138, 46), radius=0, lw=3),
    "note": dict(fill=(245, 245, 245), line=(150, 150, 150), radius=10, lw=3),
}
ARROW = (70, 76, 86)

TOKEN_RE = re.compile(r"[A-Za-z0-9_\-\./:]+|.")


def wrap_line(s, maxw, font):
    out, cur = [], ""
    for tok in TOKEN_RE.findall(s):
        if font.getlength(cur + tok) <= maxw or not cur:
            if font.getlength(tok) > maxw:
                for ch in tok:
                    if font.getlength(cur + ch) > maxw and cur:
                        out.append(cur)
                        cur = ch
                    else:
                        cur += ch
                continue
            cur += tok
        else:
            out.append(cur)
            cur = tok
    if cur:
        out.append(cur)
    return out


class Flow:
    def __init__(self, width=1600, cx=720, nw=700, pad_top=46, pad_bottom=46):
        self.W, self.cx, self.nw = width, cx, nw
        self.pad_top, self.pad_bottom = pad_top, pad_bottom
        self.nodes = []
        self.edges = []
        self.notes = []
        self.y = pad_top

    def _measure(self, lines, w):
        maxw = w - PAD_X * 2
        out = []
        for ln in lines:
            out += wrap_line(ln, maxw, F)
        return out, max(MIN_H, len(out) * LINE_H + 34)

    def add(self, lines, kind="process", gap=54, w=None, cx=None):
        cx = self.cx if cx is None else cx
        w = self.nw if w is None else w
        mw = int(w * 0.66) if kind == "decision" else w
        txt, h = self._measure(lines, mw)
        if kind == "decision":
            h = max(h + 26, 132)
        box = [cx - w // 2, self.y, cx + w // 2, self.y + h]
        self.nodes.append(dict(kind=kind, lines=txt, box=box))
        self.y = box[3] + gap
        return len(self.nodes) - 1

    def add_side(self, lines, kind, ref, cx, w=430, dy=0):
        rb = self.nodes[ref]["box"]
        cy = (rb[1] + rb[3]) // 2 + dy
        txt, h = self._measure(lines, w)
        box = [cx - w // 2, cy - h // 2, cx + w // 2, cy + h // 2]
        self.nodes.append(dict(kind=kind, lines=txt, box=box))
        return len(self.nodes) - 1

    def _poly(self, pts, label=None, lpos=None, dashed=False):
        self.edges.append(dict(pts=pts, label=label, lpos=lpos, dashed=dashed))

    def down(self, a, b, label=None):
        ab, bb = self.nodes[a]["box"], self.nodes[b]["box"]
        x = (ab[0] + ab[2]) // 2
        lpos = (x + 14, (ab[3] + bb[1]) // 2 - 34) if label else None
        self._poly([(x, ab[3]), (x, bb[1])], label, lpos)

    def down_from(self, a, b, x, label=None):
        ab, bb = self.nodes[a]["box"], self.nodes[b]["box"]
        lpos = (x + 14, (ab[3] + bb[1]) // 2 - 34) if label else None
        self._poly([(x, ab[3]), (x, bb[1])], label, lpos)

    def right(self, a, b, label=None):
        ab, bb = self.nodes[a]["box"], self.nodes[b]["box"]
        y1 = (ab[1] + ab[3]) // 2
        y2 = (bb[1] + bb[3]) // 2
        pts = [(ab[2], y1), (bb[0], y1)] if abs(y1 - y2) < 6 else \
              [(ab[2], y1), ((ab[2] + bb[0]) // 2, y1), ((ab[2] + bb[0]) // 2, y2), (bb[0], y2)]
        lpos = ((ab[2] + bb[0]) // 2 - 16, y1 - 46) if label else None
        self._poly(pts, label, lpos)

    def loop_left(self, a, b, x, label=None):
        ab, bb = self.nodes[a]["box"], self.nodes[b]["box"]
        y1 = (ab[1] + ab[3]) // 2
        y2 = (bb[1] + bb[3]) // 2
        self._poly([(ab[0], y1), (x, y1), (x, y2), (bb[0], y2)], label, (x + 12, y1 - 42))

    def skip_right(self, a, b, x, label=None):
        ab, bb = self.nodes[a]["box"], self.nodes[b]["box"]
        y1 = (ab[1] + ab[3]) // 2
        y2 = (bb[1] + bb[3]) // 2
        self._poly([(ab[2], y1), (x, y1), (x, y2), (bb[2], y2)], label, (x + 12, y1 - 42))

    def from_side(self, a, b, label=None):
        """右侧节点底部下行，再折向左汇入主列节点的右边缘。"""
        ab, bb = self.nodes[a]["box"], self.nodes[b]["box"]
        x1 = (ab[0] + ab[2]) // 2
        y1 = ab[3]
        y2 = (bb[1] + bb[3]) // 2
        lpos = (x1 + 12, y1 + 8) if label else None
        self._poly([(x1, y1), (x1, y2), (bb[2], y2)], label, lpos)

    def render(self, path):
        W = self.W
        H = self.y - 54 + self.pad_bottom
        img = Image.new("RGB", (W, H), "white")
        d = ImageDraw.Draw(img)

        for e in self.edges:
            pts = e["pts"]
            for i in range(len(pts) - 1):
                d.line([pts[i], pts[i + 1]], fill=ARROW, width=3)
            (x1, y1), (x2, y2) = pts[-2], pts[-1]
            L, Wd = 16, 9
            if abs(x2 - x1) > abs(y2 - y1):
                s = 1 if x2 > x1 else -1
                tri = [(x2, y2), (x2 - s * L, y2 - Wd), (x2 - s * L, y2 + Wd)]
            else:
                s = 1 if y2 > y1 else -1
                tri = [(x2, y2), (x2 - Wd, y2 - s * L), (x2 + Wd, y2 - s * L)]
            d.polygon(tri, fill=ARROW)
            if e["label"]:
                d.text(e["lpos"], e["label"], font=FL, fill=(90, 96, 106))

        for n in self.nodes:
            x0, y0, x1, y1 = n["box"]
            st = STYLE[n["kind"]]
            if n["kind"] == "decision":
                cy = (y0 + y1) / 2
                d.polygon([((x0 + x1) / 2, y0), (x1, cy), ((x0 + x1) / 2, y1), (x0, cy)],
                          fill=st["fill"], outline=st["line"], width=st["lw"])
                total = len(n["lines"]) * LINE_H
                ty = cy - total / 2
            else:
                d.rounded_rectangle([x0, y0, x1, y1], radius=st["radius"],
                                    fill=st["fill"], outline=st["line"], width=st["lw"])
                total = len(n["lines"]) * LINE_H
                ty = (y0 + y1) / 2 - total / 2
            for ln in n["lines"]:
                w = F.getlength(ln)
                d.text(((x0 + x1) / 2 - w / 2, ty), ln, font=F, fill=(32, 36, 44))
                ty += LINE_H

        for cx, y, text in self.notes:
            w = FL.getlength(text)
            d.text((cx - w / 2, y), text, font=FL, fill=(110, 116, 126))

        img.save(path)
        print("saved", path, img.size)


# ================================================================ 图 5 总体流程
def fig5():
    f = Flow()
    a1 = f.add(["业务方判断某存储桶不再需要", "（项目结项、业务下线、临时桶闲置）"], "start")
    a2 = f.add(["OBS 桶列表页仅展示在用桶", "已回收的桶不出现在该列表"])
    a3 = f.add(["是否确认不再使用该桶？"], "decision")
    a4 = f.add(["回收：写入 deny 桶策略",
                "先 GetBucketPolicy 备份原策略",
                "再 PutBucketPolicy 覆盖写入",
                "桶与桶内对象对业务主体不可访问"], "sub")
    a5 = f.add(["平台回收站：状态“已回收”", "桶仍保留在 OBS 中，数据原地静置、不搬迁"])
    a6 = f.add(["后续是否反悔？"], "decision")
    a7 = f.add(["恢复：撤销 deny 语句",
                "快照非空 → PutBucketPolicy 回写",
                "快照为空 → DeleteBucketPolicy"], "sub")
    a8 = f.add(["桶回到列表，业务恢复正常访问"], "end")
    keep = f.add_side(["取消回收", "桶维持在用状态", "无任何变更"], "note", a3, 1340)
    stay = f.add_side(["保持静置、长期保留", "仍占用存储并正常计费"], "note", a6, 1340)
    f.down(a1, a2)
    f.down(a2, a3)
    f.down(a3, a4, "是")
    f.right(a3, keep, "否")
    f.down(a4, a5)
    f.down(a5, a6)
    f.down(a6, a7, "是")
    f.right(a6, stay, "否")
    f.down(a7, a8)
    f.render(os.path.join(OUT, "fig5_flow_main.png"))


# ================================================================ 图 6 回收流程
def fig6():
    f = Flow()
    a1 = f.add(["列表页点击该行“回收”"], "start")
    a2 = f.add(["打开“移入回收站确认”弹窗", "带入存储桶名称、资源组织、区域（只读）"])
    a3 = f.add(["是否确认回收？"], "decision")
    a4 = f.add(["GET /?policy", "读取并保存原桶策略快照", "404 NoSuchBucketPolicy 视为空策略"], "api")
    a5 = f.add(["生成 deny 策略",
                "Sid = deny-{桶名}-{时间戳}",
                "Effect = Deny，Action = 全部动作",
                "Resource = 桶名、桶名/*"], "sub")
    a6 = f.add(["PUT /?policy", "写入 deny 策略（覆盖式，原策略被替换）"], "api")
    a7 = f.add(["返回 204？"], "decision")
    a8 = f.add(["GET /?policy 读回校验", "确认存在本次写入的 deny 语句"], "api")
    a9 = f.add(["平台状态置“已回收”，记录审计", "列表移除，回收站出现该桶"])
    a10 = f.add(["桶进入静置状态，业务访问返回 403"], "end")
    cancel = f.add_side(["取消", "弹窗关闭", "不产生任何变更"], "note", a3, 1340)
    fail = f.add_side(["按错误码提示：",
                       "MalformedPolicy / EntityTooLarge /",
                       "403 / 404",
                       "已部分覆盖时按快照回写原策略"], "note", a7, 1340)
    f.down(a1, a2)
    f.down(a2, a3)
    f.down(a3, a4, "是")
    f.right(a3, cancel, "否")
    f.down(a4, a5)
    f.down(a5, a6)
    f.down(a6, a7)
    f.down(a7, a8, "是")
    f.right(a7, fail, "否")
    f.down(a8, a9)
    f.down(a9, a10)
    f.render(os.path.join(OUT, "fig6_flow_recycle.png"))


# ================================================================ 图 7 恢复流程
def fig7():
    f = Flow()
    a1 = f.add(["回收站列表点击该行“恢复”"], "start")
    a2 = f.add(["打开“恢复存储桶确认”弹窗", "带入资产名称、所属组织、区域（只读）"])
    a3 = f.add(["是否确认恢复？"], "decision")
    a4 = f.add(["GET /?policy", "校验 deny 语句是否为平台本次写入"], "api")
    a5 = f.add(["deny 语句是否存在？"], "decision")
    a6 = f.add(["回收前是否留存", "原策略快照？"], "decision")
    a7 = f.add(["PUT /?policy", "按快照回写原桶策略"], "api")
    a8 = f.add_side(["DELETE /?policy", "删除 deny 策略（无策略也返回 204）"], "api", a6, 1340)
    a9 = f.add(["GET /?policy 读回校验", "确认 deny 语句已消失"], "api")
    a10 = f.add(["平台状态置“正常”，记录审计", "回收站移除，列表出现该桶"], "end")
    cancel = f.add_side(["取消", "弹窗关闭，桶保持已回收"], "note", a3, 1340)
    manual = f.add_side(["提示“策略已被变更，无法自动恢复”",
                         "转人工核对，平台状态保持不变"], "note", a5, 1340)
    f.down(a1, a2)
    f.down(a2, a3)
    f.down(a3, a4, "是")
    f.right(a3, cancel, "否")
    f.down(a4, a5)
    f.down(a5, a6, "是")
    f.right(a5, manual, "否")
    f.down(a6, a7, "是")
    f.right(a6, a8, "否")
    f.down(a7, a9)
    f.from_side(a8, a9)
    f.down(a9, a10)
    f.render(os.path.join(OUT, "fig7_flow_restore.png"))


# ================================================================ 图 8 异常与回滚
def fig8():
    f = Flow()
    a1 = f.add(["回收 / 恢复提交，调用 OBS 桶策略接口"], "start")
    a2 = f.add(["云侧是否返回明确结果？"], "decision")
    a3 = f.add(["GET /?policy 读回实际状态", "（仅超时、5xx 等结果未知时执行）"], "api")
    a4 = f.add(["实际状态是否符合预期？"], "decision")
    a5 = f.add(["按成功收口，修正平台状态", "审计记录“超时但已生效”"])
    a6 = f.add(["定时对账：平台回收状态 / 桶策略实际状态", "逐桶比对 deny 语句是否存在"], "api")
    a7 = f.add(["平台状态与策略是否一致？"], "decision")
    a8 = f.add(["状态最终一致，操作全程可审计"], "end")
    clear = f.add_side(["204：更新状态并提示成功",
                        "4xx：按错误码提示，保持原状态"], "note", a2, 1340)
    retry = f.add_side(["指数退避重试，最多 3 次",
                        "仍失败则置“操作失败”并保持原状态"], "note", a4, 1340)
    fix = f.add_side(["告警并自动修正平台状态",
                      "差异明细留痕，支持人工介入"], "note", a7, 1340)
    f.down(a1, a2)
    f.down(a2, a3, "否")
    f.right(a2, clear, "是")
    f.down(a3, a4)
    f.down(a4, a5, "是")
    f.right(a4, retry, "否")
    f.down(a5, a6)
    f.down(a6, a7)
    f.down(a7, a8, "是")
    f.right(a7, fix, "否")
    f.render(os.path.join(OUT, "fig8_flow_exception.png"))


if __name__ == "__main__":
    fig5()
    fig6()
    fig7()
    fig8()
