<template>
  <div class="evs-list-card">
    <!-- Top Action Bar -->
    <div class="action-bar">
      <!-- Left Action Buttons -->
      <div class="left-actions">
        <button class="btn-create" @click="showCreateModal = true">
          <span class="icon-circle-plus">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
              <circle cx="12" cy="12" r="9"/>
              <line x1="12" y1="8" x2="12" y2="16"/>
              <line x1="8" y1="12" x2="16" y2="12"/>
            </svg>
          </span>
          <span>创建</span>
        </button>

        <button class="btn-outline" @click="showTrashModal = true">
          <span>回收站</span>
        </button>

        <button class="btn-outline" @click="handleExport">
          <span>导出清单</span>
        </button>

        <div class="dropdown-wrapper">
          <button class="btn-outline btn-dropdown" @click="showBatchDropdown = !showBatchDropdown">
            <span>批量操作</span>
            <span class="arrow-down">▾</span>
          </button>
          <div v-if="showBatchDropdown" class="dropdown-menu">
            <div class="dropdown-item" @click="handleBatchAction('批量扩容')">批量扩容</div>
            <div class="dropdown-item" @click="handleBatchAction('批量卸载')">批量卸载</div>
            <div class="dropdown-item text-danger" @click="handleBatchAction('批量删除')">批量删除</div>
          </div>
        </div>
      </div>

      <!-- Right Search & Tool Bar -->
      <div class="right-tools">
        <div class="search-filter-wrap">
          <div class="combined-search-box">
            <select v-model="searchField" class="search-field-select">
              <option value="name">实例名称</option>
              <option value="org">资源组织</option>
              <option value="env">部署环境</option>
              <option value="mount">挂载点</option>
              <option value="id">ID</option>
            </select>
            <div class="search-divider"></div>
            <input 
              type="text" 
              v-model="searchKeyword" 
              placeholder="请输入" 
              class="search-input"
              @keyup.enter="handleSearch"
            />
          </div>

          <button class="btn-search" @click="handleSearch">
            <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="11" cy="11" r="8"/>
              <line x1="21" y1="21" x2="16.65" y2="16.65"/>
            </svg>
            <span>查询</span>
          </button>

          <button class="btn-reset" @click="handleReset">
            <svg class="reset-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/>
              <path d="M3 3v5h5"/>
            </svg>
            <span>重置</span>
          </button>

          <!-- Column Setting Icon -->
          <div class="col-setting-wrapper">
            <button class="tool-icon-btn" title="列表列设置" @click="showColSetting = !showColSetting">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="3"></circle>
                <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
              </svg>
            </button>
            <div v-if="showColSetting" class="col-setting-popover">
              <div class="popover-title">自定义显示列</div>
              <label v-for="col in columns" :key="col.prop" class="col-checkbox">
                <input type="checkbox" v-model="col.visible" :disabled="col.prop === 'name' || col.prop === 'op'" />
                <span>{{ col.label }}</span>
              </label>
            </div>
          </div>

          <!-- Refresh Icon -->
          <button :class="['tool-icon-btn', { spinning: isRefreshing }]" @click="handleRefresh" title="刷新列表">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="23 4 23 10 17 10"/>
              <polyline points="1 20 1 14 7 14"/>
              <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/>
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- EVS Table -->
    <div class="table-container">
      <table class="evs-table">
        <thead>
          <tr>
            <th class="col-checkbox">
              <input 
                type="checkbox" 
                :checked="isAllSelected" 
                @change="toggleSelectAll" 
              />
            </th>
            <th v-if="isColVisible('name')" class="col-name">实例名称</th>
            <th v-if="isColVisible('status')" class="col-status">状态</th>
            <th v-if="isColVisible('org')" class="col-org">资源组织</th>
            <th v-if="isColVisible('region')" class="col-region">区域</th>
            <th v-if="isColVisible('zone')" class="col-zone">可用区</th>
            <th v-if="isColVisible('mountPoint')" class="col-mount">挂载点</th>
            <th v-if="isColVisible('env')" class="col-env">部署环境</th>
            <th v-if="isColVisible('id')" class="col-id">ID</th>
            <th v-if="isColVisible('op')" class="col-op">操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in pagedList" :key="item.id" class="table-row">
            <td class="col-checkbox">
              <input 
                type="checkbox" 
                :value="item.id" 
                v-model="selectedRows" 
              />
            </td>
            <td v-if="isColVisible('name')" class="col-name">
              <a class="evs-name-link" @click="handleOpenDetail(item)" :title="'查看详情: ' + item.name">
                {{ item.name }}
              </a>
            </td>
            <td v-if="isColVisible('status')" class="col-status">
              <span class="status-wrap">
                <span class="status-dot"></span>
                <span class="status-text">{{ item.status || '已挂载' }}</span>
              </span>
            </td>
            <td v-if="isColVisible('org')" class="col-org">{{ item.org }}</td>
            <td v-if="isColVisible('region')" class="col-region">{{ item.region }}</td>
            <td v-if="isColVisible('zone')" class="col-zone">{{ item.zone }}</td>
            <td v-if="isColVisible('mountPoint')" class="col-mount font-mono">{{ item.mountPoint || '/dev/vda' }}</td>
            <td v-if="isColVisible('env')" class="col-env">{{ item.env || 'SIT' }}</td>
            <td v-if="isColVisible('id')" class="col-id font-mono">{{ item.id }}</td>
            <td v-if="isColVisible('op')" class="col-op">
              <div class="op-actions">
                <a class="op-btn" @click="handleOpenExpand(item)">扩容</a>
                <a class="op-btn" @click="handleOpenDelete(item)">删除</a>
                
                <!-- More Action Dropdown -->
                <div class="more-action-wrap">
                  <a class="op-btn more-btn" @click.stop="toggleMoreMenu(item.id)">
                    <span>更多</span>
                    <span class="arrow-down">▾</span>
                  </a>
                  <div v-if="activeMoreId === item.id" class="more-dropdown-menu">
                    <div class="more-item" @click="handleActionItem('卸载', item)">卸载</div>
                    <div class="more-item" @click="handleActionItem('创建快照', item)">创建快照</div>
                    <div class="more-item" @click="handleActionItem('修改属性', item)">修改属性</div>
                  </div>
                </div>
              </div>
            </td>
          </tr>

          <tr v-if="pagedList.length === 0">
            <td :colspan="visibleColCount + 1" class="empty-cell">
              <div class="empty-wrap">
                <div class="empty-icon">💾</div>
                <div class="empty-text">没有找到匹配的信创云硬盘数据</div>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Pagination Bar -->
    <div class="pagination-bar">
      <div class="total-text">共 {{ totalCountDisplay }} 条</div>

      <div class="pager-controls">
        <button 
          class="pager-btn" 
          :disabled="currentPage <= 1" 
          @click="changePage(currentPage - 1)"
        >
          &lt;
        </button>

        <button 
          class="pager-page" 
          :class="{ active: currentPage === 1 }" 
          @click="changePage(1)"
        >
          1
        </button>

        <button 
          class="pager-page" 
          :class="{ active: currentPage === 2 }" 
          @click="changePage(2)"
        >
          2
        </button>

        <button 
          class="pager-page" 
          :class="{ active: currentPage === 3 }" 
          @click="changePage(3)"
        >
          3
        </button>

        <button 
          class="pager-page" 
          :class="{ active: currentPage === 4 }" 
          @click="changePage(4)"
        >
          4
        </button>

        <button 
          class="pager-page" 
          :class="{ active: currentPage === 5 }" 
          @click="changePage(5)"
        >
          5
        </button>

        <span class="pager-ellipsis">...</span>

        <button 
          class="pager-page" 
          :class="{ active: currentPage === totalPages }" 
          @click="changePage(totalPages)"
        >
          {{ totalPages }}
        </button>

        <button 
          class="pager-btn" 
          :disabled="currentPage >= totalPages" 
          @click="changePage(currentPage + 1)"
        >
          &gt;
        </button>

        <div class="page-size-wrap">
          <select v-model="pageSize" class="page-size-select" @change="currentPage = 1">
            <option :value="10">10 条/页</option>
            <option :value="20">20 条/页</option>
            <option :value="50">50 条/页</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Modals & Drawers -->
    <EvsCreateModal 
      v-model:visible="showCreateModal" 
      @success="handleCreateSuccess" 
    />

    <EvsExpandModal 
      v-model:visible="showExpandModal" 
      :instance="currentInstance" 
      @confirm="handleConfirmExpand" 
    />

    <EvsDeleteModal 
      v-model:visible="showDeleteModal" 
      :instance="currentInstance" 
      @confirm="handleConfirmDelete" 
    />

    <EvsDetailDrawer 
      v-model:visible="showDetailDrawer" 
      :instance="currentInstance" 
      @expand="handleOpenExpandFromDetail"
    />

    <EvsRecycleModal 
      v-model:visible="showTrashModal" 
      @restore="handleRestoreFromTrash" 
    />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import EvsExpandModal from './EvsExpandModal.vue'
import EvsDeleteModal from './EvsDeleteModal.vue'
import EvsDetailDrawer from './EvsDetailDrawer.vue'
import EvsCreateModal from './EvsCreateModal.vue'
import EvsRecycleModal from './EvsRecycleModal.vue'

const props = defineProps({
  instances: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['create', 'delete', 'expand', 'notify'])

// Table columns
const columns = ref([
  { prop: 'name', label: '实例名称', visible: true },
  { prop: 'status', label: '状态', visible: true },
  { prop: 'org', label: '资源组织', visible: true },
  { prop: 'region', label: '区域', visible: true },
  { prop: 'zone', label: '可用区', visible: true },
  { prop: 'mountPoint', label: '挂载点', visible: true },
  { prop: 'env', label: '部署环境', visible: true },
  { prop: 'id', label: 'ID', visible: true },
  { prop: 'op', label: '操作', visible: true }
])

const isColVisible = (prop) => {
  const col = columns.value.find(c => c.prop === prop)
  return col ? col.visible : true
}

const visibleColCount = computed(() => columns.value.filter(c => c.visible).length)
const showColSetting = ref(false)

// Row Selection
const selectedRows = ref([])
const isAllSelected = computed(() => {
  return pagedList.value.length > 0 && selectedRows.value.length === pagedList.value.length
})

const toggleSelectAll = (e) => {
  if (e.target.checked) {
    selectedRows.value = pagedList.value.map(item => item.id)
  } else {
    selectedRows.value = []
  }
}

// Search & Filter
const searchField = ref('name')
const searchKeyword = ref('')
const activeFilter = ref({ field: 'name', keyword: '' })
const isRefreshing = ref(false)

const handleSearch = () => {
  activeFilter.value = {
    field: searchField.value,
    keyword: searchKeyword.value.trim().toLowerCase()
  }
  currentPage.value = 1
}

const handleReset = () => {
  searchKeyword.value = ''
  activeFilter.value = { field: 'name', keyword: '' }
  currentPage.value = 1
}

const handleRefresh = () => {
  isRefreshing.value = true
  setTimeout(() => {
    isRefreshing.value = false
    emit('notify', '云硬盘列表已刷新')
  }, 400)
}

// Data List Filtering
const filteredList = computed(() => {
  const { field, keyword } = activeFilter.value
  if (!keyword) return props.instances

  return props.instances.filter(item => {
    if (field === 'name') return (item.name || '').toLowerCase().includes(keyword)
    if (field === 'org') return (item.org || '').toLowerCase().includes(keyword)
    if (field === 'env') return (item.env || 'SIT').toLowerCase().includes(keyword)
    if (field === 'mount') return (item.mountPoint || '').toLowerCase().includes(keyword)
    if (field === 'id') return (item.id || '').toLowerCase().includes(keyword)
    return true
  })
})

// Pagination
const currentPage = ref(1)
const pageSize = ref(10)

// Total count display matching screenshot: 48296
const totalCountDisplay = computed(() => {
  if (activeFilter.value.keyword) {
    return filteredList.value.length
  }
  return 48296
})

const totalPages = computed(() => 4830)

const pagedList = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  return filteredList.value.slice(start, start + pageSize.value)
})

const changePage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
    selectedRows.value = []
  }
}

// Dropdown & Modal States
const showBatchDropdown = ref(false)
const activeMoreId = ref(null)
const showCreateModal = ref(false)
const showTrashModal = ref(false)
const showExpandModal = ref(false)
const showDeleteModal = ref(false)
const showDetailDrawer = ref(false)
const currentInstance = ref(null)

const toggleMoreMenu = (id) => {
  activeMoreId.value = activeMoreId.value === id ? null : id
}

// Global click listener to close more dropdown
if (typeof window !== 'undefined') {
  window.addEventListener('click', () => {
    activeMoreId.value = null
    showBatchDropdown.value = false
  })
}

const handleBatchAction = (action) => {
  showBatchDropdown.value = false
  if (selectedRows.value.length === 0) {
    emit('notify', '请先勾选需要操作的云硬盘', 'warning')
    return
  }
  emit('notify', `已对选中的 ${selectedRows.value.length} 个云硬盘执行【${action}】操作`)
}

const handleExport = () => {
  emit('notify', '云硬盘清单导出中，文件将保存为 EVS_List.xlsx')
}

const handleActionItem = (action, item) => {
  activeMoreId.value = null
  emit('notify', `实例【${item.name}】已成功执行【${action}】`)
}

const handleOpenExpand = (item) => {
  currentInstance.value = item
  showExpandModal.value = true
}

const handleOpenExpandFromDetail = (item) => {
  showDetailDrawer.value = false
  currentInstance.value = item
  showExpandModal.value = true
}

const handleConfirmExpand = (payload) => {
  emit('expand', payload)
}

const handleOpenDelete = (item) => {
  currentInstance.value = item
  showDeleteModal.value = true
}

const handleConfirmDelete = (id) => {
  emit('delete', id)
}

const handleOpenDetail = (item) => {
  currentInstance.value = item
  showDetailDrawer.value = true
}

const handleCreateSuccess = (newInstance) => {
  emit('create', newInstance)
}

const handleRestoreFromTrash = (item) => {
  emit('notify', `已从回收站恢复云硬盘【${item.name}】`)
}
</script>

<style scoped>
.evs-list-card {
  background: #ffffff;
  border-radius: 2px;
  box-shadow: 0 1px 3px rgba(0, 21, 41, 0.05);
  display: flex;
  flex-direction: column;
  min-height: calc(100vh - 110px);
}

/* Action Bar */
.action-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px 14px;
}

.left-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.btn-create {
  height: 32px;
  padding: 0 16px;
  background-color: #2468f2;
  color: #ffffff;
  border: 1px solid #2468f2;
  border-radius: 3px;
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  font-size: 13px;
  font-weight: 400;
  transition: all 0.2s;
}

.btn-create:hover {
  background-color: #1855d1;
  border-color: #1855d1;
}

.icon-circle-plus svg {
  width: 14px;
  height: 14px;
}

.btn-outline {
  height: 32px;
  padding: 0 14px;
  background-color: #ffffff;
  color: #606266;
  border: 1px solid #dcdfe6;
  border-radius: 3px;
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  font-size: 13px;
  transition: all 0.2s;
}

.btn-outline:hover {
  border-color: #2468f2;
  color: #2468f2;
}

.dropdown-wrapper {
  position: relative;
}

.btn-dropdown {
  padding-right: 10px;
}

.arrow-down {
  font-size: 11px;
  color: #909399;
}

.dropdown-menu {
  position: absolute;
  top: 36px;
  left: 0;
  background: #ffffff;
  border: 1px solid #e4e7ed;
  border-radius: 4px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  padding: 4px 0;
  z-index: 100;
  min-width: 110px;
}

.dropdown-item {
  padding: 8px 16px;
  font-size: 12.5px;
  color: #333333;
  cursor: pointer;
  transition: background-color 0.15s;
}

.dropdown-item:hover {
  background-color: #f0f5ff;
  color: #2468f2;
}

.dropdown-item.text-danger {
  color: #f5222d;
}

.dropdown-item.text-danger:hover {
  background-color: #fff1f0;
}

/* Right Tools */
.right-tools {
  display: flex;
  align-items: center;
}

.search-filter-wrap {
  display: flex;
  align-items: center;
  gap: 8px;
}

.combined-search-box {
  display: flex;
  align-items: center;
  height: 32px;
  border: 1px solid #dcdfe6;
  border-radius: 3px;
  background-color: #ffffff;
  transition: border-color 0.2s;
}

.combined-search-box:focus-within {
  border-color: #2468f2;
}

.search-field-select {
  height: 100%;
  border: none;
  background: transparent;
  padding: 0 10px;
  font-size: 13px;
  color: #333333;
  outline: none;
  cursor: pointer;
}

.search-divider {
  width: 1px;
  height: 18px;
  background-color: #e4e7ed;
}

.search-input {
  height: 100%;
  border: none;
  background: transparent;
  padding: 0 12px;
  font-size: 13px;
  color: #333333;
  outline: none;
  width: 200px;
}

.search-input::placeholder {
  color: #c0c4cc;
}

.btn-search {
  height: 32px;
  padding: 0 14px;
  background-color: #2468f2;
  color: #ffffff;
  border: 1px solid #2468f2;
  border-radius: 3px;
  display: flex;
  align-items: center;
  gap: 5px;
  cursor: pointer;
  font-size: 13px;
  transition: all 0.2s;
}

.btn-search:hover {
  background-color: #1855d1;
  border-color: #1855d1;
}

.search-icon {
  width: 14px;
  height: 14px;
}

.btn-reset {
  height: 32px;
  padding: 0 14px;
  background-color: #ffffff;
  color: #606266;
  border: 1px solid #dcdfe6;
  border-radius: 3px;
  display: flex;
  align-items: center;
  gap: 5px;
  cursor: pointer;
  font-size: 13px;
  transition: all 0.2s;
}

.btn-reset:hover {
  border-color: #2468f2;
  color: #2468f2;
}

.reset-icon {
  width: 13px;
  height: 13px;
}

.tool-icon-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #ffffff;
  border: 1px solid #dcdfe6;
  border-radius: 3px;
  color: #606266;
  cursor: pointer;
  transition: all 0.2s;
}

.tool-icon-btn:hover {
  border-color: #2468f2;
  color: #2468f2;
}

.tool-icon-btn svg {
  width: 15px;
  height: 15px;
}

.tool-icon-btn.spinning svg {
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.col-setting-wrapper {
  position: relative;
}

.col-setting-popover {
  position: absolute;
  top: 38px;
  right: 0;
  width: 170px;
  background: #ffffff;
  border: 1px solid #e4e7ed;
  border-radius: 4px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  padding: 10px 14px;
  z-index: 100;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.popover-title {
  font-size: 12px;
  font-weight: 600;
  color: #909399;
  border-bottom: 1px solid #f0f2f5;
  padding-bottom: 4px;
}

.col-checkbox {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: #333333;
  cursor: pointer;
}

/* Table Container */
.table-container {
  flex: 1;
  overflow-x: auto;
  padding: 0 20px;
}

.evs-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
  font-size: 12.5px;
}

.evs-table thead tr {
  background-color: #f7f9fa;
  border-top: 1px solid #ebeef5;
  border-bottom: 1px solid #ebeef5;
}

.evs-table th {
  padding: 10px 12px;
  color: #555555;
  font-weight: 500;
  white-space: nowrap;
}

.evs-table tbody tr {
  border-bottom: 1px solid #f0f2f5;
  transition: background-color 0.15s;
}

.evs-table tbody tr:hover {
  background-color: #f8faff;
}

.evs-table td {
  padding: 11px 12px;
  color: #333333;
  vertical-align: middle;
}

.col-checkbox {
  width: 32px;
  text-align: center;
  padding-left: 10px;
}

.col-name {
  max-width: 240px;
}

.evs-name-link {
  color: #2468f2;
  cursor: pointer;
  text-decoration: none;
  font-weight: 400;
}

.evs-name-link:hover {
  text-decoration: underline;
}

.status-wrap {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background-color: #19be6b;
  display: inline-block;
}

.status-text {
  color: #19be6b;
}

.font-mono {
  font-family: monospace;
  font-size: 12px;
  color: #4a5568;
}

.col-id {
  max-width: 220px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.col-op {
  width: 140px;
  text-align: right;
}

.op-actions {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 12px;
}

.op-btn {
  color: #2468f2;
  cursor: pointer;
  text-decoration: none;
  font-size: 12.5px;
}

.op-btn:hover {
  color: #1855d1;
  text-decoration: underline;
}

.more-action-wrap {
  position: relative;
}

.more-btn {
  display: flex;
  align-items: center;
  gap: 2px;
}

.more-dropdown-menu {
  position: absolute;
  top: 24px;
  right: 0;
  background: #ffffff;
  border: 1px solid #e4e7ed;
  border-radius: 4px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  padding: 4px 0;
  z-index: 100;
  min-width: 90px;
  text-align: left;
}

.more-item {
  padding: 6px 12px;
  font-size: 12px;
  color: #333333;
  cursor: pointer;
  transition: background-color 0.15s;
}

.more-item:hover {
  background-color: #f0f5ff;
  color: #2468f2;
}

.empty-cell {
  text-align: center;
  padding: 60px 0;
}

.empty-wrap {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.empty-icon {
  font-size: 32px;
}

.empty-text {
  color: #909399;
  font-size: 13px;
}

/* Pagination Bar */
.pagination-bar {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 16px;
  padding: 16px 20px;
  border-top: 1px solid #f0f2f5;
  font-size: 13px;
  color: #606266;
  user-select: none;
}

.total-text {
  margin-right: auto;
  color: #606266;
}

.pager-controls {
  display: flex;
  align-items: center;
  gap: 6px;
}

.pager-btn {
  min-width: 28px;
  height: 28px;
  padding: 0 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #ffffff;
  border: 1px solid #dcdfe6;
  border-radius: 2px;
  color: #606266;
  cursor: pointer;
  font-size: 12px;
  transition: all 0.2s;
}

.pager-btn:hover:not(:disabled) {
  border-color: #2468f2;
  color: #2468f2;
}

.pager-btn:disabled {
  color: #c0c4cc;
  cursor: not-allowed;
  border-color: #ebeef5;
}

.pager-page {
  min-width: 28px;
  height: 28px;
  padding: 0 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #ffffff;
  border: 1px solid #dcdfe6;
  border-radius: 2px;
  color: #606266;
  cursor: pointer;
  font-size: 12px;
  transition: all 0.2s;
}

.pager-page:hover {
  border-color: #2468f2;
  color: #2468f2;
}

.pager-page.active {
  border-color: #2468f2;
  color: #2468f2;
  font-weight: 600;
  background-color: #ffffff;
}

.pager-ellipsis {
  padding: 0 4px;
  color: #909399;
}

.page-size-wrap {
  margin-left: 6px;
}

.page-size-select {
  height: 28px;
  padding: 0 8px;
  border: 1px solid #dcdfe6;
  border-radius: 2px;
  font-size: 12px;
  color: #606266;
  outline: none;
  cursor: pointer;
  background: #ffffff;
}

.page-size-select:focus {
  border-color: #2468f2;
}
</style>
