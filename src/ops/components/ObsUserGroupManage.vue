<template>
  <div class="ug-wrapper">
    <div class="ug-card">
      <!-- 操作按钮区 -->
      <div class="action-bar">
        <div class="left-actions">
          <span class="btn-tip-wrap" :title="selectedCount === 0 ? '请先勾选用户' : ''">
            <button
              class="btn-primary"
              :disabled="selectedCount === 0"
              @click="openBatchJoinConfirm"
            >
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
                <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
                <circle cx="8.5" cy="7" r="4" />
                <line x1="20" y1="8" x2="20" y2="14" />
                <line x1="23" y1="11" x2="17" y2="11" />
              </svg>
              <span>批量迁入（已选 {{ selectedCount }}/{{ MAX_SELECT }}）</span>
            </button>
          </span>
          <span class="limit-hint">单次最多勾选 {{ MAX_SELECT }} 个用户</span>
        </div>

        <div class="right-tools">
          <div class="search-box">
            <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="11" cy="11" r="8" />
              <line x1="21" y1="21" x2="16.65" y2="16.65" />
            </svg>
            <input
              v-model="keywordInput"
              class="search-input"
              placeholder="按用户名筛选，回车查询"
              @keyup.enter="applySearch"
            />
            <span v-if="keywordInput" class="search-clear" @click="clearSearch">×</span>
          </div>
        </div>
      </div>

      <!-- 数据表格 -->
      <div class="table-container">
        <table class="ug-table">
          <thead>
            <tr>
              <th class="col-check">
                <input
                  ref="headerCheckRef"
                  type="checkbox"
                  :checked="headerChecked"
                  :disabled="headerDisabled"
                  :title="headerDisabled ? `单次最多勾选 ${MAX_SELECT} 个用户` : ''"
                  @change="toggleAllOnPage"
                />
              </th>
              <th>用户名</th>
              <th class="col-group">当前用户组</th>
              <th>资源组织</th>
              <th>区域</th>
              <th class="col-op">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="u in pagedList"
              :key="u.id"
              :class="['table-row', { selected: isSelected(u.id), locked: !!u.lockReason }]"
            >
              <td class="col-check">
                <input
                  type="checkbox"
                  :checked="isSelected(u.id)"
                  :disabled="isRowDisabled(u)"
                  :title="rowDisabledTip(u)"
                  @change="toggleRow(u)"
                />
              </td>
              <td>
                <span class="user-name">{{ u.name }}</span>
                <span v-if="u.lockReason" class="lock-tag">{{ u.lockReason }}</span>
              </td>
              <!-- 当前用户组列：异步调用接口查询获取，仅保留详情按钮 -->
              <td class="col-group">
                <a class="op-btn detail-btn" @click="openGroupDetailModal(u)">详情</a>
              </td>
              <td>{{ u.org }}</td>
              <td>{{ u.region }}</td>
              <td class="col-op">
                <div class="row-ops-wrap">
                  <a
                    :class="['op-btn', { disabled: !!u.lockReason }]"
                    :title="u.lockReason ? `${u.lockReason}，不可操作` : '点击加入用户组'"
                    @click="!u.lockReason && openJoinGroupModal(u)"
                  >加入用户组</a>
                  <span class="op-divider">|</span>
                  <a
                    :class="['op-btn', 'danger-link', { disabled: !!u.lockReason || !u.groups || u.groups.length === 0 }]"
                    :title="(!u.groups || u.groups.length === 0) ? '当前未加入任何用户组，无需退出' : (u.lockReason ? `${u.lockReason}，不可操作` : '点击退出一个或多个用户组')"
                    @click="!u.lockReason && u.groups && u.groups.length > 0 && openLeaveGroupModal(u)"
                  >退出用户组</a>
                </div>
              </td>
            </tr>
            <tr v-if="pagedList.length === 0">
              <td colspan="6" class="empty-cell">没有找到匹配的用户</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- 分页区 -->
      <div class="pagination-bar">
        <div class="total-text">共 {{ filteredList.length }} 条</div>
        <div class="pager-controls">
          <button class="pager-btn" :disabled="currentPage <= 1" @click="currentPage--">&lt;</button>
          <button
            v-for="p in pageNumbers"
            :key="p"
            :class="['pager-page', { active: currentPage === p }]"
            @click="currentPage = p"
          >{{ p }}</button>
          <button class="pager-btn" :disabled="currentPage >= totalPages" @click="currentPage++">&gt;</button>
        </div>
        <div class="selected-info">
          <span>已选 <b :class="{ full: selectedCount >= MAX_SELECT }">{{ selectedCount }}</b>/{{ MAX_SELECT }}</span>
          <a :class="['clear-link', { disabled: selectedCount === 0 }]" @click="clearSelection">清空已选</a>
        </div>
      </div>
    </div>

    <!-- 弹窗 1：当前用户组详情弹窗（异步接口查询） -->
    <div v-if="groupDetailVisible" class="modal-mask" @click.self="groupDetailVisible = false">
      <div class="modal modal-detail">
        <div class="modal-header">
          <span>用户所属用户组详情</span>
          <span class="modal-close" @click="groupDetailVisible = false">×</span>
        </div>
        <div class="modal-body">
          <div class="user-info-banner">
            <span class="banner-label">用户：</span>
            <b class="banner-val">{{ currentDetailUser?.name }}</b>
            <span class="banner-divider">|</span>
            <span class="banner-label">资源组织：</span>
            <span class="banner-val">{{ currentDetailUser?.org }}</span>
            <span class="banner-divider">|</span>
            <span class="banner-label">已加入组数量：</span>
            <span class="badge-count">{{ groupDetailLoading ? '...' : (detailUserGroups?.length || 0) }}</span>
          </div>

          <!-- 异步加载状态 -->
          <div v-if="groupDetailLoading" class="modal-loading-wrap">
            <div class="loading-spinner"></div>
            <span>正在异步查询用户组数据...</span>
          </div>

          <div v-else-if="detailUserGroups?.length" class="modal-table-wrap">
            <table class="ug-table modal-table">
              <thead>
                <tr>
                  <th>所属用户组</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="g in detailUserGroups" :key="g">
                  <td><span class="group-tag">{{ g }}</span></td>
                </tr>
              </tbody>
            </table>
          </div>

          <div v-else class="empty-modal-state">
            <div class="empty-icon">📁</div>
            <p>该用户当前暂未加入任何 OBS 用户组</p>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn-primary" @click="groupDetailVisible = false">关闭</button>
        </div>
      </div>
    </div>

    <!-- 弹窗 2：“加入用户组”弹窗 -->
    <div v-if="joinModalVisible" class="modal-mask" @click.self="joinModalVisible = false">
      <div class="modal">
        <div class="modal-header">
          <span>加入用户组</span>
          <span class="modal-close" @click="joinModalVisible = false">×</span>
        </div>
        <div class="modal-body">
          <div class="user-info-banner">
            <span class="banner-label">目标用户：</span>
            <b class="banner-val">{{ currentOperUser?.name }}</b>
            <span class="banner-divider">|</span>
            <span class="banner-label">当前所属组：</span>
            <span v-if="currentOperUser?.groups?.length" class="banner-groups">
              <span v-for="g in currentOperUser.groups" :key="g" class="mini-tag">{{ g }}</span>
            </span>
            <span v-else class="text-muted">无</span>
          </div>

          <div class="form-row">
            <label class="form-label required">选择目标用户组</label>
            <select v-model="joinTargetGroup" class="form-select">
              <option value="" disabled>请选择要加入的目标用户组</option>
              <option
                v-for="g in availableGroupsToJoin"
                :key="g.name"
                :value="g.name"
              >
                {{ g.name }} - {{ g.desc }}
              </option>
            </select>
            <div v-if="availableGroupsToJoin.length === 0" class="field-error-tip">
              该用户已加入所有可选用户组，无需重复加入。
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn-cancel-modal" @click="joinModalVisible = false">取消</button>
          <button
            class="btn-primary"
            :disabled="!joinTargetGroup || isExecuting"
            @click="submitJoinGroup"
          >
            {{ isExecuting ? '加入中...' : '确认加入' }}
          </button>
        </div>
      </div>
    </div>

    <!-- 弹窗 3：“退出用户组”弹窗（支持退出一个或多个用户组） -->
    <div v-if="leaveModalVisible" class="modal-mask" @click.self="leaveModalVisible = false">
      <div class="modal">
        <div class="modal-header">
          <span class="danger-header">退出用户组</span>
          <span class="modal-close" @click="leaveModalVisible = false">×</span>
        </div>
        <div class="modal-body">
          <div class="user-info-banner">
            <span class="banner-label">目标用户：</span>
            <b class="banner-val">{{ currentOperUser?.name }}</b>
            <span class="banner-divider">|</span>
            <span class="banner-label">待选择退出组（共 {{ currentOperUser?.groups?.length || 0 }} 个）：</span>
          </div>

          <!-- 用户组勾选列表表格（支持退出一个或多个） -->
          <div class="leave-groups-select-wrap">
            <table class="ug-table leave-table">
              <thead>
                <tr>
                  <th class="col-check">
                    <input
                      type="checkbox"
                      :checked="isAllLeaveGroupsSelected"
                      @change="toggleSelectAllLeaveGroups"
                    />
                  </th>
                  <th>所属用户组</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="g in currentOperUser?.groups || []"
                  :key="g"
                  :class="{ selected: selectedLeaveGroups.includes(g) }"
                >
                  <td class="col-check">
                    <input
                      type="checkbox"
                      :checked="selectedLeaveGroups.includes(g)"
                      @change="toggleLeaveGroupItem(g)"
                    />
                  </td>
                  <td><span class="group-tag-danger">{{ g }}</span></td>
                </tr>
              </tbody>
            </table>
          </div>

          <div class="leave-count-tip">
            已选中待退出用户组：<b>{{ selectedLeaveGroups.length }}</b> 个
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn-cancel-modal" @click="leaveModalVisible = false">取消</button>
          <button
            class="btn-danger-submit"
            :disabled="selectedLeaveGroups.length === 0 || isExecuting"
            @click="submitLeaveGroups"
          >
            {{ isExecuting ? '退组中...' : `确认退出选中的 ${selectedLeaveGroups.length} 个用户组` }}
          </button>
        </div>
      </div>
    </div>

    <!-- 弹窗 4：批量迁入确认弹窗 -->
    <div v-if="batchJoinVisible" class="modal-mask" @click.self="closeBatchJoin">
      <div class="modal">
        <div class="modal-header">
          <span>批量迁入用户组</span>
          <span class="modal-close" @click="closeBatchJoin">×</span>
        </div>
        <div class="modal-body">
          <div class="form-row">
            <label class="form-label">待迁入用户（已选 {{ selectedCount }} 人）</label>
            <div class="user-chip-list">
              <span v-for="u in selectedUsers" :key="u.id" class="user-chip">
                {{ u.name }}
              </span>
            </div>
          </div>
          <div class="form-row">
            <label class="form-label required">目标迁入用户组</label>
            <select v-model="batchTargetGroup" class="form-select">
              <option value="" disabled>请选择要统一迁入的目标用户组</option>
              <option v-for="g in groupOptions" :key="g.name" :value="g.name">
                {{ g.name }} - {{ g.desc }}
              </option>
            </select>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn-cancel-modal" @click="closeBatchJoin">取消</button>
          <button class="btn-primary" :disabled="!batchTargetGroup || isExecuting" @click="executeBatchJoin">
            {{ isExecuting ? '迁入中...' : '确认批量迁入' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Toast -->
    <transition name="toast-fade">
      <div v-if="toast.msg" :class="['ug-toast', toast.type]">{{ toast.msg }}</div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, watch, watchEffect } from 'vue'

const MAX_SELECT = 10
const PAGE_SIZE = 10

/* ---------------- 基础定义与 Mock 用户组策略 ---------------- */
const groupOptions = [
  { name: 'obs-group-default', desc: '标准业务存取组', level: 'primary', levelText: '读写' },
  { name: 'obs-group-readonly', desc: '审计分析只读组', level: 'info', levelText: '只读' },
  { name: 'obs-group-dev', desc: '开发与SIT联调组', level: 'warning', levelText: '读写' },
  { name: 'obs-group-ops', desc: '运维与安全保障组', level: 'danger', levelText: '管理' },
  { name: 'obs-group-bigdata', desc: '数仓大数据集成组', level: 'primary', levelText: '高吞吐读写' }
]

const getGroupPolicy = (groupName) => {
  const g = groupOptions.find(item => item.name === groupName)
  return g || { desc: '自定义组策略', level: 'info', levelText: '标准' }
}

const orgs = ['默认组织', '智能投研系统', '影像内容管理服务平台', '数智化贷后管理系统', '信用卡网络系统', '金融云门户系统']
const surnames = ['zhang', 'li', 'wang', 'liu', 'chen', 'yang', 'zhao', 'huang', 'zhou', 'wu', 'xu', 'sun', 'ma', 'zhu', 'hu', 'guo']

const genUsers = () => {
  const list = []
  for (let i = 1; i <= 46; i++) {
    const s = surnames[i % surnames.length]
    let lockReason = ''
    if (i % 13 === 0) lockReason = '已完成迁移'
    else if (i % 17 === 0) lockReason = '无操作权限'

    // 模拟多用户组归属 (有0个、1个、2个或3个用户组)
    let userGroups = []
    if (i % 7 === 0) {
      userGroups = []
    } else if (i % 3 === 0) {
      userGroups = ['obs-group-default', 'obs-group-dev']
    } else if (i % 5 === 0) {
      userGroups = ['obs-group-default', 'obs-group-ops', 'obs-group-bigdata']
    } else {
      userGroups = [groupOptions[i % groupOptions.length].name]
    }

    list.push({
      id: `u-${i}`,
      name: `${s}${String(i).padStart(2, '0')}`,
      groups: userGroups,
      org: orgs[i % orgs.length],
      region: '上海',
      env: i % 4 === 0 ? 'UAT' : 'SIT',
      createTime: `2025-${String((i % 12) + 1).padStart(2, '0')}-${String((i % 27) + 1).padStart(2, '0')}`,
      lockReason
    })
  }
  return list
}

const users = ref(genUsers())

/* ---------------- Toast ---------------- */
const toast = ref({ msg: '', type: 'info' })
let toastTimer = null
const showToast = (msg, type = 'info') => {
  toast.value = { msg, type }
  clearTimeout(toastTimer)
  toastTimer = setTimeout(() => (toast.value.msg = ''), 2600)
}

/* ---------------- 搜索 & 分页 ---------------- */
const keywordInput = ref('')
const keyword = ref('')
const currentPage = ref(1)

const applySearch = () => {
  keyword.value = keywordInput.value.trim()
  currentPage.value = 1
}
const clearSearch = () => {
  keywordInput.value = ''
  applySearch()
}

const filteredList = computed(() => {
  const k = keyword.value.toLowerCase()
  return k ? users.value.filter(u => u.name.toLowerCase().includes(k)) : users.value
})
const totalPages = computed(() => Math.max(1, Math.ceil(filteredList.value.length / PAGE_SIZE)))
const pagedList = computed(() => {
  const start = (currentPage.value - 1) * PAGE_SIZE
  return filteredList.value.slice(start, start + PAGE_SIZE)
})
const pageNumbers = computed(() => Array.from({ length: totalPages.value }, (_, i) => i + 1))
watch(totalPages, (n) => { if (currentPage.value > n) currentPage.value = n })

/* ---------------- 勾选（跨页保留，全局 10 封顶） ---------------- */
const selectedMap = ref(new Map())
const selectedCount = computed(() => selectedMap.value.size)
const selectedUsers = computed(() => Array.from(selectedMap.value.values()))
const isFull = computed(() => selectedCount.value >= MAX_SELECT)

const isSelected = (id) => selectedMap.value.has(id)
const isRowDisabled = (u) => !!u.lockReason || (isFull.value && !isSelected(u.id))
const rowDisabledTip = (u) => {
  if (u.lockReason) return `${u.lockReason}，不可勾选`
  if (isFull.value && !isSelected(u.id)) return `单次最多勾选 ${MAX_SELECT} 个用户`
  return ''
}

const setSelected = (mutator) => {
  const m = new Map(selectedMap.value)
  mutator(m)
  selectedMap.value = m
}

const toggleRow = (u) => {
  if (isSelected(u.id)) {
    setSelected(m => m.delete(u.id))
  } else {
    if (isFull.value) {
      showToast(`单次最多勾选 ${MAX_SELECT} 个用户`, 'warn')
      return
    }
    setSelected(m => m.set(u.id, u))
  }
}

// 表头全选：按剩余额度生效
const pageSelectable = computed(() => pagedList.value.filter(u => !u.lockReason))
const pageSelectedCount = computed(() => pageSelectable.value.filter(u => isSelected(u.id)).length)
const headerChecked = computed(() =>
  pageSelectable.value.length > 0 && pageSelectedCount.value === pageSelectable.value.length
)
const headerIndeterminate = computed(() => pageSelectedCount.value > 0 && !headerChecked.value)
const headerDisabled = computed(() =>
  pageSelectable.value.length === 0 || (isFull.value && pageSelectedCount.value === 0)
)

const headerCheckRef = ref(null)
watchEffect(() => {
  if (headerCheckRef.value) headerCheckRef.value.indeterminate = headerIndeterminate.value
})

const toggleAllOnPage = () => {
  if (headerChecked.value || isFull.value) {
    setSelected(m => pageSelectable.value.forEach(u => m.delete(u.id)))
    return
  }
  const remaining = MAX_SELECT - selectedCount.value
  const candidates = pageSelectable.value.filter(u => !isSelected(u.id))
  const toAdd = candidates.slice(0, remaining)
  setSelected(m => toAdd.forEach(u => m.set(u.id, u)))
  if (candidates.length > remaining) {
    showToast(`已勾选 ${MAX_SELECT} 个用户（单次上限）`, 'warn')
  }
}

const clearSelection = () => {
  if (selectedCount.value === 0) return
  selectedMap.value = new Map()
}

/* ---------------- 模拟异步接口：查询用户的当前用户组 ---------------- */
const mockFetchUserGroupsApi = (userId) => {
  return new Promise((resolve) => {
    // 模拟 350ms 异步网络接口请求
    setTimeout(() => {
      const u = users.value.find(item => item.id === userId)
      resolve(u?.groups ? [...u.groups] : [])
    }, 350)
  })
}

/* ---------------- 弹窗 1：当前用户组详情 (异步查询) ---------------- */
const groupDetailVisible = ref(false)
const groupDetailLoading = ref(false)
const currentDetailUser = ref(null)
const detailUserGroups = ref([])

const openGroupDetailModal = async (user) => {
  currentDetailUser.value = user
  detailUserGroups.value = []
  groupDetailVisible.value = true
  groupDetailLoading.value = true

  try {
    const fetchedGroups = await mockFetchUserGroupsApi(user.id)
    user.groups = fetchedGroups
    detailUserGroups.value = fetchedGroups
  } catch (err) {
    showToast('异步查询用户组失败', 'error')
  } finally {
    groupDetailLoading.value = false
  }
}

/* ---------------- 弹窗 2：加入用户组 ---------------- */
const joinModalVisible = ref(false)
const currentOperUser = ref(null)
const joinTargetGroup = ref('')
const isExecuting = ref(false)

const availableGroupsToJoin = computed(() => {
  if (!currentOperUser.value) return groupOptions
  const userGroups = currentOperUser.value.groups || []
  return groupOptions.filter(g => !userGroups.includes(g.name))
})

const openJoinGroupModal = (user) => {
  currentOperUser.value = user
  joinTargetGroup.value = ''
  joinModalVisible.value = true
}

const submitJoinGroup = () => {
  if (!joinTargetGroup.value || !currentOperUser.value) return
  isExecuting.value = true

  setTimeout(() => {
    isExecuting.value = false
    const u = users.value.find(item => item.id === currentOperUser.value.id)
    if (u) {
      if (!u.groups) u.groups = []
      if (!u.groups.includes(joinTargetGroup.value)) {
        u.groups.push(joinTargetGroup.value)
      }
    }
    joinModalVisible.value = false
    showToast(`用户【${currentOperUser.value.name}】已成功加入用户组【${joinTargetGroup.value}】`, 'success')
  }, 500)
}

/* ---------------- 弹窗 3：退出用户组 (支持选择一个或多个) ---------------- */
const leaveModalVisible = ref(false)
const selectedLeaveGroups = ref([])

const isAllLeaveGroupsSelected = computed(() => {
  if (!currentOperUser.value || !currentOperUser.value.groups) return false
  return currentOperUser.value.groups.length > 0 &&
    selectedLeaveGroups.value.length === currentOperUser.value.groups.length
})

const openLeaveGroupModal = (user) => {
  currentOperUser.value = user
  selectedLeaveGroups.value = []
  leaveModalVisible.value = true
}

const toggleLeaveGroupItem = (g) => {
  const index = selectedLeaveGroups.value.indexOf(g)
  if (index >= 0) {
    selectedLeaveGroups.value.splice(index, 1)
  } else {
    selectedLeaveGroups.value.push(g)
  }
}

const toggleSelectAllLeaveGroups = () => {
  if (isAllLeaveGroupsSelected.value) {
    selectedLeaveGroups.value = []
  } else {
    selectedLeaveGroups.value = [...(currentOperUser.value?.groups || [])]
  }
}

const submitLeaveGroups = () => {
  if (selectedLeaveGroups.value.length === 0 || !currentOperUser.value) return
  isExecuting.value = true

  setTimeout(() => {
    isExecuting.value = false
    const u = users.value.find(item => item.id === currentOperUser.value.id)
    if (u && u.groups) {
      u.groups = u.groups.filter(g => !selectedLeaveGroups.value.includes(g))
    }
    const count = selectedLeaveGroups.value.length
    leaveModalVisible.value = false
    showToast(`用户【${currentOperUser.value.name}】已成功退出 ${count} 个用户组`, 'success')
  }, 500)
}

/* ---------------- 弹窗 4：批量迁入 ---------------- */
const batchJoinVisible = ref(false)
const batchTargetGroup = ref('')

const openBatchJoinConfirm = () => {
  if (selectedCount.value === 0) {
    showToast('请先勾选用户', 'warn')
    return
  }
  batchTargetGroup.value = ''
  batchJoinVisible.value = true
}

const closeBatchJoin = () => {
  if (isExecuting.value) return
  batchJoinVisible.value = false
}

const executeBatchJoin = () => {
  if (!batchTargetGroup.value || selectedUsers.value.length === 0) return
  isExecuting.value = true

  const target = batchTargetGroup.value
  const count = selectedUsers.value.length

  setTimeout(() => {
    isExecuting.value = false
    selectedUsers.value.forEach(sel => {
      const u = users.value.find(x => x.id === sel.id)
      if (u) {
        if (!u.groups) u.groups = []
        if (!u.groups.includes(target)) {
          u.groups.push(target)
        }
      }
    })
    batchJoinVisible.value = false
    clearSelection()
    showToast(`已成功将选中的 ${count} 名用户迁入用户组【${target}】`, 'success')
  }, 500)
}
</script>

<style scoped>
.ug-wrapper {
  position: relative;
}

.ug-card {
  background: #ffffff;
  border-radius: 2px;
  box-shadow: 0 1px 3px rgba(0, 21, 41, 0.05);
  display: flex;
  flex-direction: column;
  min-height: calc(100vh - 114px);
  position: relative;
}

/* 操作按钮区 */
.action-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px 14px;
}

.left-actions {
  display: flex;
  align-items: center;
  gap: 14px;
}

.btn-tip-wrap {
  display: inline-flex;
}

.btn-primary {
  height: 32px;
  padding: 0 16px;
  border-radius: 3px;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  font-size: 13px;
  transition: all 0.2s;
  background-color: #2468f2;
  color: #ffffff;
  border: 1px solid #2468f2;
}

.btn-primary svg {
  width: 14px;
  height: 14px;
}

.btn-primary:hover:not(:disabled) {
  background-color: #1855d1;
  border-color: #1855d1;
}

.btn-primary:disabled {
  background-color: #a3c0f9;
  border-color: #a3c0f9;
  cursor: not-allowed;
  pointer-events: none;
}

.limit-hint {
  font-size: 12px;
  color: #909399;
}

.search-box {
  position: relative;
  display: flex;
  align-items: center;
  width: 260px;
  height: 32px;
  border: 1px solid #dcdfe6;
  border-radius: 3px;
  background: #ffffff;
  transition: border-color 0.2s;
}

.search-box:focus-within {
  border-color: #2468f2;
}

.search-icon {
  width: 14px;
  height: 14px;
  color: #a0a4ab;
  margin-left: 10px;
  flex-shrink: 0;
}

.search-input {
  flex: 1;
  height: 100%;
  border: none;
  outline: none;
  padding: 0 8px;
  font-size: 13px;
  background: transparent;
}

.search-clear {
  margin-right: 8px;
  color: #c0c4cc;
  cursor: pointer;
  font-size: 14px;
}

.search-clear:hover {
  color: #909399;
}

/* 表格 */
.table-container {
  flex: 1;
  padding: 0 20px;
  overflow-x: auto;
}

.ug-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}

.ug-table th {
  background-color: #f5f7fa;
  color: #303133;
  font-weight: 500;
  text-align: left;
  padding: 10px 12px;
  border-bottom: 1px solid #ebeef5;
  white-space: nowrap;
}

.ug-table td {
  padding: 11px 12px;
  border-bottom: 1px solid #ebeef5;
  color: #606266;
  white-space: nowrap;
}

.table-row:hover td {
  background-color: #f5f8ff;
}

.table-row.selected td {
  background-color: #ecf3ff;
}

.table-row.locked td {
  color: #a8abb2;
}

.col-check {
  width: 44px;
  text-align: center !important;
}

.col-check input {
  width: 14px;
  height: 14px;
  cursor: pointer;
  accent-color: #2468f2;
  vertical-align: middle;
}

.col-check input:disabled {
  cursor: not-allowed;
}

.col-group {
  width: 130px;
}

.group-cell-wrap {
  display: flex;
  align-items: center;
  gap: 8px;
}

.group-summary-badge {
  font-size: 11px;
  padding: 1px 6px;
  border-radius: 2px;
  background: #e6f7ff;
  border: 1px solid #91d5ff;
  color: #1890ff;
}

.text-muted-tag {
  font-size: 11px;
  color: #bfbfbf;
}

.detail-btn {
  font-weight: 500;
}

.col-op {
  width: 160px;
}

.row-ops-wrap {
  display: flex;
  align-items: center;
  gap: 8px;
}

.op-divider {
  color: #dcdfe6;
  font-size: 12px;
}

.user-name {
  color: #303133;
  font-weight: 500;
}

.table-row.locked .user-name {
  color: #a8abb2;
}

.lock-tag {
  margin-left: 8px;
  font-size: 11px;
  padding: 1px 6px;
  border-radius: 2px;
  background: #f4f4f5;
  border: 1px solid #e9e9eb;
  color: #909399;
}

.group-tag {
  font-size: 12px;
  padding: 2px 8px;
  border-radius: 2px;
  background: #ecf5ff;
  border: 1px solid #d9ecff;
  color: #2468f2;
}

.group-tag-danger {
  font-size: 12px;
  padding: 2px 8px;
  border-radius: 2px;
  background: #fff1f0;
  border: 1px solid #ffa39e;
  color: #f5222d;
}

.level-tag {
  font-size: 11px;
  padding: 1px 6px;
  border-radius: 2px;
}

.level-tag.primary {
  background: #f6ffed;
  border: 1px solid #b7eb8f;
  color: #52c41a;
}

.level-tag.info {
  background: #e6f7ff;
  border: 1px solid #91d5ff;
  color: #1890ff;
}

.level-tag.warning {
  background: #fffbe6;
  border: 1px solid #ffe58f;
  color: #faad14;
}

.level-tag.danger {
  background: #fff1f0;
  border: 1px solid #ffa39e;
  color: #f5222d;
}

.op-btn {
  color: #2468f2;
  cursor: pointer;
  font-size: 13px;
  transition: color 0.15s;
}

.op-btn:hover {
  color: #1855d1;
  text-decoration: underline;
}

.op-btn.danger-link {
  color: #f5222d;
}

.op-btn.danger-link:hover {
  color: #cf1322;
}

.op-btn.disabled {
  color: #c0c4cc !important;
  cursor: not-allowed;
  text-decoration: none !important;
}

.empty-cell {
  text-align: center;
  padding: 60px 0 !important;
  color: #909399;
}

/* 分页 */
.pagination-bar {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px 20px;
  border-top: 1px solid #f0f2f5;
  font-size: 13px;
  color: #606266;
  user-select: none;
}

.total-text {
  color: #606266;
}

.pager-controls {
  display: flex;
  align-items: center;
  gap: 6px;
}

.pager-btn,
.pager-page {
  min-width: 28px;
  height: 28px;
  padding: 0 6px;
  background-color: #ffffff;
  border: 1px solid #dcdfe6;
  border-radius: 2px;
  color: #606266;
  cursor: pointer;
  font-size: 12px;
  transition: all 0.2s;
}

.pager-btn:hover:not(:disabled),
.pager-page:hover {
  border-color: #2468f2;
  color: #2468f2;
}

.pager-btn:disabled {
  color: #c0c4cc;
  cursor: not-allowed;
  border-color: #ebeef5;
}

.pager-page.active {
  border-color: #2468f2;
  color: #2468f2;
  font-weight: 600;
}

.selected-info {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 12px;
}

.selected-info b {
  color: #2468f2;
}

.selected-info b.full {
  color: #e6a23c;
}

.clear-link {
  color: #2468f2;
  cursor: pointer;
}

.clear-link.disabled {
  color: #c0c4cc;
  cursor: not-allowed;
}

/* 弹窗通用样式 */
.modal-mask {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}

.modal {
  width: 580px;
  max-width: 92vw;
  background: #ffffff;
  border-radius: 4px;
  box-shadow: 0 6px 24px rgba(0, 0, 0, 0.18);
  display: flex;
  flex-direction: column;
  max-height: 86vh;
}

.modal-wide {
  width: 680px;
}

.modal-detail {
  width: 620px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 20px;
  border-bottom: 1px solid #ebeef5;
  font-size: 15px;
  font-weight: 600;
  color: #303133;
}

.danger-header {
  color: #f5222d;
}

.modal-close {
  font-size: 20px;
  color: #909399;
  cursor: pointer;
  font-weight: 400;
}

.modal-body {
  padding: 18px 20px;
  overflow-y: auto;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  padding: 12px 20px;
  border-top: 1px solid #ebeef5;
  background: #fafafa;
}

.btn-cancel-modal {
  height: 32px;
  padding: 0 16px;
  border-radius: 3px;
  background-color: #ffffff;
  color: #606266;
  border: 1px solid #dcdfe6;
  cursor: pointer;
  font-size: 13px;
  transition: all 0.2s;
}

.btn-cancel-modal:hover {
  border-color: #2468f2;
  color: #2468f2;
}

.btn-danger-submit {
  height: 32px;
  padding: 0 20px;
  background: #f5222d;
  border: 1px solid #f5222d;
  border-radius: 3px;
  color: #ffffff;
  cursor: pointer;
  font-size: 13px;
  font-weight: 500;
  transition: all 0.2s;
}

.btn-danger-submit:hover:not(:disabled) {
  background: #cf1322;
  border-color: #cf1322;
}

.btn-danger-submit:disabled {
  background: #ffccc7;
  border-color: #ffccc7;
  cursor: not-allowed;
}

/* 用户信息横幅 */
.user-info-banner {
  background: #f5f7fa;
  padding: 10px 14px;
  border-radius: 3px;
  font-size: 13px;
  color: #606266;
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 16px;
}

.banner-label {
  color: #909399;
}

.banner-val {
  color: #303133;
}

.banner-divider {
  color: #dcdfe6;
  margin: 0 4px;
}

.badge-count {
  background: #2468f2;
  color: #ffffff;
  font-size: 11px;
  padding: 1px 6px;
  border-radius: 10px;
  font-weight: 600;
}

.banner-groups {
  display: inline-flex;
  gap: 4px;
  flex-wrap: wrap;
}

.mini-tag {
  font-size: 11px;
  background: #e6f7ff;
  border: 1px solid #91d5ff;
  color: #1890ff;
  padding: 0 4px;
  border-radius: 2px;
}

.text-muted {
  color: #909399;
}

.empty-modal-state {
  text-align: center;
  padding: 40px 0;
  color: #909399;
}

.modal-loading-wrap {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 40px 0;
  color: #909399;
  font-size: 13px;
}

.loading-spinner {
  width: 26px;
  height: 26px;
  border: 2px solid #e8eaec;
  border-top-color: #2468f2;
  border-radius: 50%;
  animation: modal-spin 0.8s linear infinite;
}

@keyframes modal-spin {
  to { transform: rotate(360deg); }
}

.empty-modal-state .empty-icon {
  font-size: 32px;
  margin-bottom: 8px;
}

/* 表单字段 */
.form-row {
  margin-bottom: 16px;
}

.form-label {
  display: block;
  font-size: 13px;
  color: #606266;
  margin-bottom: 8px;
  font-weight: 500;
}

.form-label.required::before {
  content: '*';
  color: #f56c6c;
  margin-right: 4px;
}

.form-select,
.form-input {
  width: 100%;
  height: 34px;
  border: 1px solid #dcdfe6;
  border-radius: 3px;
  padding: 0 10px;
  font-size: 13px;
  outline: none;
  background: #ffffff;
  transition: border-color 0.2s;
}

.form-select:focus,
.form-input:focus {
  border-color: #2468f2;
}

.field-error-tip {
  font-size: 12px;
  color: #f56c6c;
  margin-top: 4px;
}

.radio-group {
  display: flex;
  gap: 16px;
}

.radio-label {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: #303133;
  cursor: pointer;
}

.radio-label input {
  accent-color: #2468f2;
}

/* 退出组多选表格 */
.leave-groups-select-wrap {
  border: 1px solid #ebeef5;
  border-radius: 3px;
  max-height: 180px;
  overflow-y: auto;
  margin-bottom: 10px;
}

.leave-table th {
  background-color: #fafafa;
}

.leave-count-tip {
  font-size: 12px;
  color: #606266;
  margin-bottom: 12px;
}

.leave-count-tip b {
  color: #f5222d;
}

.danger-warning-card {
  background-color: #fffbe6;
  border: 1px solid #ffe58f;
  border-radius: 4px;
  padding: 12px 16px;
  margin-bottom: 16px;
}

.danger-title-row {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 6px;
}

.warning-icon {
  font-size: 15px;
}

.warning-title {
  font-size: 13px;
  font-weight: 600;
  color: #d46b08;
}

.warning-desc {
  font-size: 12px;
  color: #595959;
  line-height: 1.6;
}

.warning-list {
  margin: 4px 0 0 16px;
  padding: 0;
}

.confirm-agree-box {
  margin-top: 14px;
  padding: 10px 14px;
  background-color: #fff2f0;
  border: 1px dashed #ffccc7;
  border-radius: 3px;
}

.checkbox-label {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  cursor: pointer;
}

.checkbox-label input {
  margin-top: 3px;
  accent-color: #f5222d;
}

.confirm-text {
  font-size: 12px;
  color: #cf1322;
  line-height: 1.5;
}

.user-chip-list {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  max-height: 120px;
  overflow-y: auto;
  padding: 8px;
  background: #f5f7fa;
  border-radius: 3px;
}

.user-chip {
  font-size: 12px;
  padding: 2px 8px;
  background: #ffffff;
  border: 1px solid #dcdfe6;
  border-radius: 2px;
  color: #303133;
}

.user-chip em {
  font-style: normal;
  color: #909399;
  margin-left: 6px;
}

.impact-tip {
  font-size: 12px;
  line-height: 1.7;
  color: #33598a;
  background: #f0f7ff;
  border: 1px solid #c8e1ff;
  padding: 8px 12px;
  border-radius: 3px;
}

.result-summary {
  display: flex;
  gap: 16px;
  margin-bottom: 12px;
  font-size: 13px;
  color: #606266;
}

.sum-item.success {
  color: #52c41a;
  font-weight: 600;
}

.sum-item.fail {
  color: #f5222d;
  font-weight: 600;
}

.result-table td,
.result-table th {
  padding: 8px 12px;
}

.status-dot {
  display: inline-block;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  margin-right: 6px;
  vertical-align: middle;
}

.status-dot.ok {
  background: #52c41a;
}

.status-dot.err {
  background: #f5222d;
}

.err-text {
  color: #f5222d !important;
}

/* Toast */
.ug-toast {
  position: fixed;
  top: 70px;
  left: 50%;
  transform: translateX(-50%);
  padding: 8px 18px;
  border-radius: 4px;
  font-size: 13px;
  z-index: 3000;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
  background: #edf2fc;
  color: #606266;
  border: 1px solid #ebeef5;
}

.ug-toast.success {
  background: #f0f9eb;
  color: #52c41a;
  border-color: #e1f3d8;
}

.ug-toast.warn {
  background: #fffbe6;
  color: #d46b08;
  border-color: #ffe58f;
}

.ug-toast.error {
  background: #fff1f0;
  color: #f5222d;
  border-color: #ffa39e;
}

.toast-fade-enter-active,
.toast-fade-leave-active {
  transition: opacity 0.2s, transform 0.2s;
}

.toast-fade-enter-from,
.toast-fade-leave-to {
  opacity: 0;
  transform: translate(-50%, -8px);
}
</style>
