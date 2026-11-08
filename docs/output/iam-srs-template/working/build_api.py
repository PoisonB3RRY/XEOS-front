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
