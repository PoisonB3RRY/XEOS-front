# -*- coding: utf-8 -*-
"""绘制需求文档用的业务流程图（PIL 直绘，无外部依赖）。"""
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
    """按像素宽度折行；英文单词与标识符不拆开。"""
    out, cur = [], ""
    for tok in TOKEN_RE.findall(s):
        if font.getlength(cur + tok) <= maxw or not cur:
            if font.getlength(tok) > maxw:          # 超长标识符强制按字符拆
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
    def __init__(self, width=1600, cx=740, nw=700, pad_top=46, pad_bottom=46):
        self.W, self.cx, self.nw = width, cx, nw
        self.pad_top, self.pad_bottom = pad_top, pad_bottom
        self.nodes = []
        self.edges = []
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

    def add_side(self, lines, kind, ref, cx, w=420, dy=0):
        """在参考节点同一行右侧放一个节点。"""
        rb = self.nodes[ref]["box"]
        cy = (rb[1] + rb[3]) // 2 + dy
        txt, h = self._measure(lines, w)
        box = [cx - w // 2, cy - h // 2, cx + w // 2, cy + h // 2]
        self.nodes.append(dict(kind=kind, lines=txt, box=box))
        return len(self.nodes) - 1

    # ------------------------------------------------------------ 连线
    def _poly(self, pts, label=None, lpos=None, dashed=False):
        self.edges.append(dict(pts=pts, label=label, lpos=lpos, dashed=dashed))

    def down(self, a, b, label=None):
        ab, bb = self.nodes[a]["box"], self.nodes[b]["box"]
        x = (ab[0] + ab[2]) // 2
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

    def note_below(self, ref, text, dy=34):
        ab = self.nodes[ref]["box"]
        cx = (ab[0] + ab[2]) // 2
        self.notes.append((cx, ab[3] + dy, text, "middle"))

    # ------------------------------------------------------------ 渲染
    def render(self, path, notes=()):
        W = self.W
        H = self.y - 54 + self.pad_bottom
        img = Image.new("RGB", (W, H), "white")
        d = ImageDraw.Draw(img)

        for e in self.edges:
            pts = e["pts"]
            for i in range(len(pts) - 1):
                d.line([pts[i], pts[i + 1]], fill=ARROW, width=3)
            # 箭头
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

        for cx, y, text, align in notes:
            w = FL.getlength(text)
            d.text((cx - w / 2, y), text, font=FL, fill=(110, 116, 126))

        img.save(path)
        print("saved", path, img.size)


# ================================================================ 图 7 总体流程
def fig7():
    f = Flow()
    a1 = f.add(["运维人员进入“存储服务—OBS用户组管理”"], "start")
    a2 = f.add(["加载 OBS 用户列表", "（用户名、当前用户组、资源组织、区域）"])
    a3 = f.add(["按用户名检索，定位待迁移用户"])
    a4 = f.add(["ListGroupMembershipsForMember、ListGroups",
                "打开“详情”，核对用户当前所属用户组"], "api")
    a5 = f.add(["逐用户执行迁移：先加入、后退出",
                "① 加入目标组：CreateGroupMembership",
                "② 退出原组：DeleteGroupMembership",
                "顺序不可颠倒，否则出现权限空档"], "sub")
    a6 = f.add(["是否还有待迁移用户？"], "decision")
    a7 = f.add(["迁移完成，结果可逐用户核对"], "end")
    f.down(a1, a2)
    f.down(a2, a3)
    f.down(a3, a4)
    f.down(a4, a5)
    f.down(a5, a6)
    f.down(a6, a7, "否")
    f.loop_left(a6, a3, 240, "是")
    f.render(os.path.join(OUT, "fig7_flow_main.png"))


# ================================================================ 图 8 加入
def fig8():
    f = Flow()
    a1 = f.add(["列表页点击该行“加入用户组”"], "start")
    a2 = f.add(["ListGroupMembershipsForMember", "查询该用户当前所属组，带入弹窗信息条"], "api")
    a3 = f.add(["ListGroups", "加载目标用户组下拉候选（按身份源查询）"], "api")
    a4 = f.add(["选择目标用户组（单选、必填）"])
    a5 = f.add(["是否已选择目标组？"], "decision")
    a6 = f.add(["CreateGroupMembership", "提交 group_id 与 member_id.user_id"], "api")
    a7 = f.add(["是否成功？", "200 成功；409 视为已加入"], "decision")
    a8 = f.add(["提示失败原因（无权限、组不存在、超时等）", "弹窗保持打开，修正后可再次提交"])
    a9 = f.add(["提示加入成功，关闭弹窗并刷新列表"])
    a10 = f.add(["详情弹窗可见新组，已加入组数量加一"], "end")
    f.down(a1, a2)
    f.down(a2, a3)
    f.down(a3, a4)
    f.down(a4, a5)
    f.down(a5, a6, "是")
    f.loop_left(a5, a4, 260, "否")
    f.down(a6, a7)
    f.down(a7, a8, "否")
    f.skip_right(a7, a9, 1200, "是")
    f.loop_left(a8, a6, 220)
    f.render(os.path.join(OUT, "fig8_flow_join.png"))


# ================================================================ 图 9 退出
def fig9():
    f = Flow()
    a1 = f.add(["列表页点击该行“退出用户组”"], "start")
    a2 = f.add(["该用户是否有", "所属用户组？"], "decision")
    a3 = f.add(["ListGroupMembershipsForMember", "取用户全部所属组，得到 group_id 与 membership_id"], "api")
    a4 = f.add(["ListGroups", "将 group_id 映射为组名，供弹窗展示"], "api")
    a5 = f.add(["弹窗列示所属用户组，勾选待退出的组", "按钮文案随勾选数量变化"])
    a6 = f.add(["勾选数量是否大于 0？"], "decision")
    a7 = f.add(["DeleteGroupMembership", "按 membership_id 逐个提交解绑请求"], "api")
    a8 = f.add(["逐项记录结果：成功数、失败数及失败原因", "404（关系已不存在）按成功处理"])
    a9 = f.add(["刷新列表与详情，已加入组数量相应减少"])
    a10 = f.add(["退出完成，原组权限已收回"], "end")
    side = f.add_side(["“退出用户组”置灰", "不可点击（无组可退）"], "note", a2, 1330)
    f.down(a1, a2)
    f.down(a2, a3, "是")
    f.right(a2, side, "否")
    f.down(a3, a4)
    f.down(a4, a5)
    f.down(a5, a6)
    f.down(a6, a7, "是")
    f.loop_left(a6, a5, 260, "否")
    f.down(a7, a8)
    f.down(a8, a9)
    f.down(a9, a10)
    f.render(os.path.join(OUT, "fig9_flow_leave.png"))


# ================================================================ 图 10 批量
def fig10():
    f = Flow()
    a1 = f.add(["列表页勾选 1—10 个用户", "点击“批量迁入（已选 N/10）”"], "start")
    a2 = f.add(["弹窗回显待迁入用户（打开时快照，弹窗内不可增删）"])
    a3 = f.add(["ListGroups", "加载目标用户组下拉候选"], "api")
    a4 = f.add(["选择本次统一迁入的目标用户组"])
    a5 = f.add(["是否已选择目标组？"], "decision")
    a6 = f.add(["按用户串行循环：i = 1 … N"])
    a7 = f.add(["CreateGroupMembership", "为第 i 个用户建立目标组成员关系"], "api")
    a8 = f.add(["记录该用户结果：成功数加一（409 计成功）", "失败数加一并记录原因，不中断整批"])
    a9 = f.add(["i 是否小于 N ？"], "decision")
    a10 = f.add(["汇总结果：共 N 个，成功 X 个，失败 Y 个", "校验 X ＋ Y ＝ N，失败项列出用户名与原因"])
    a11 = f.add(["关闭弹窗并刷新列表；本次不退出原组"], "end")
    f.down(a1, a2)
    f.down(a2, a3)
    f.down(a3, a4)
    f.down(a4, a5)
    f.down(a5, a6, "是")
    f.loop_left(a5, a4, 260, "否")
    f.down(a6, a7)
    f.down(a7, a8)
    f.down(a8, a9)
    f.down(a9, a10, "否")
    f.loop_left(a9, a6, 200, "是")
    f.down(a10, a11)
    f.render(os.path.join(OUT, "fig10_flow_batch.png"))


if __name__ == "__main__":
    fig7()
    fig8()
    fig9()
    fig10()
