<template>
  <div class="recycle-bin-card">
    <!-- Breadcrumb / Header Bar -->
    <div class="recycle-header-nav">
      <div class="nav-left">
        <button class="btn-back-link" @click="handleBack" title="返回对象存储桶列表">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <polyline points="15 18 9 12 15 6" />
          </svg>
          <span>返回存储桶列表</span>
        </button>
        <div class="header-divider"></div>
        <span class="header-title">信创对象存储桶 - 回收站</span>
      </div>
    </div>

    <!-- Action Bar -->
    <div class="action-bar">
      <!-- Left side: empty -->
      <div class="left-actions"></div>

      <!-- Right: Search & Tool buttons -->
      <div class="right-tools">
        <div class="search-filter-wrap">
          <div class="combined-search-box">
            <select v-model="searchField" class="search-field-select">
              <option value="name">资产名称</option>
              <option value="org">资源组织名称</option>
              <option value="zone">区域</option>
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

    <!-- Table Container -->
    <div class="table-container">
      <table class="recycle-table">
        <thead>
          <tr>
            <th v-if="isColVisible('name')" class="col-name">资产名称</th>
            <th v-if="isColVisible('org')" class="col-org">资源组织名称</th>
            <th v-if="isColVisible('zone')" class="col-zone">区域</th>
            <th v-if="isColVisible('updateTime')" class="col-time">更新时间</th>
            <th v-if="isColVisible('op')" class="col-op">操作</th>
          </tr>
        </thead>
        <tbody>
          <tr 
            v-for="item in pagedList" 
            :key="item.name" 
            class="table-row"
          >
            <td v-if="isColVisible('name')" class="col-name">
              <span class="asset-name">{{ item.name }}</span>
            </td>
            <td v-if="isColVisible('org')" class="col-org">{{ item.org }}</td>
            <td v-if="isColVisible('zone')" class="col-zone">{{ item.zone || '上海' }}</td>
            <td v-if="isColVisible('updateTime')" class="col-time">{{ item.updateTime }}</td>
            <td v-if="isColVisible('op')" class="col-op">
              <div class="op-actions">
                <a class="op-link-restore" @click="handleOpenSingleRestore(item)">恢复</a>
              </div>
            </td>
          </tr>

          <tr v-if="pagedList.length === 0">
            <td :colspan="visibleColCount" class="empty-cell">
              <div class="empty-wrap">
                <div class="empty-icon">🗑️</div>
                <div class="empty-text">回收站暂无数据</div>
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
          v-for="p in visiblePages" 
          :key="p"
          :class="['pager-page', { active: currentPage === p }]" 
          @click="changePage(p)"
        >
          {{ p }}
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
            <option :value="10">10条/页</option>
            <option :value="20">20条/页</option>
            <option :value="50">50条/页</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Restore Confirmation Modal (去掉更新时间，可用区改为区域) -->
    <div v-if="showRestoreModal" class="modal-overlay" @click.self="showRestoreModal = false">
      <div class="modal-card">
        <div class="modal-header">
          <h3 class="modal-title">恢复存储桶确认</h3>
          <button class="modal-close-btn" @click="showRestoreModal = false">×</button>
        </div>

        <div class="modal-body">
          <div class="info-tip-banner">
            <div class="tip-icon">
              <svg viewBox="0 0 24 24" fill="#2468f2">
                <circle cx="12" cy="12" r="10" />
                <line x1="12" y1="16" x2="12" y2="12" />
                <line x1="12" y1="8" x2="12.01" y2="8" />
              </svg>
            </div>
            <div class="tip-text">
              <strong>确定要恢复存储桶【{{ currentRestoreItem?.name }}】吗？</strong>
              <div>恢复后，存储桶将重新出现在“信创对象存储-桶(OBS)”列表中，恢复正常服务与访问。</div>
            </div>
          </div>

          <div v-if="currentRestoreItem" class="detail-table-wrap">
            <table class="detail-table">
              <thead>
                <tr>
                  <th>资产名称</th>
                  <th>所属组织</th>
                  <th>区域</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td class="text-bold">{{ currentRestoreItem.name }}</td>
                  <td>{{ currentRestoreItem.org }}</td>
                  <td>{{ currentRestoreItem.zone || '上海' }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div class="modal-footer">
          <button class="btn btn-default" @click="showRestoreModal = false">取消</button>
          <button class="btn btn-primary" @click="confirmRestore">确认</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  recycleList: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['back', 'restore', 'notify'])

// Table columns (去掉了更新者、状态)
const columns = ref([
  { prop: 'name', label: '资产名称', visible: true },
  { prop: 'org', label: '资源组织名称', visible: true },
  { prop: 'zone', label: '区域', visible: true },
  { prop: 'updateTime', label: '更新时间', visible: true },
  { prop: 'op', label: '操作', visible: true }
])

const isColVisible = (prop) => {
  const col = columns.value.find(c => c.prop === prop)
  return col ? col.visible : true
}

const visibleColCount = computed(() => columns.value.filter(c => c.visible).length)
const showColSetting = ref(false)

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
    emit('notify', '信创对象存储桶回收站已刷新')
  }, 400)
}

// Data Filtering
const filteredList = computed(() => {
  const { field, keyword } = activeFilter.value
  if (!keyword) return props.recycleList

  return props.recycleList.filter(item => {
    if (field === 'name') return (item.name || '').toLowerCase().includes(keyword)
    if (field === 'org') return (item.org || '').toLowerCase().includes(keyword)
    if (field === 'zone') return (item.zone || '').toLowerCase().includes(keyword)
    return true
  })
})

// Pagination
const currentPage = ref(1)
const pageSize = ref(10)

const totalCountDisplay = computed(() => filteredList.value.length)

const totalPages = computed(() => {
  return Math.max(1, Math.ceil(filteredList.value.length / pageSize.value))
})

const visiblePages = computed(() => {
  const pages = []
  const max = Math.min(totalPages.value, 8)
  for (let i = 1; i <= max; i++) {
    pages.push(i)
  }
  return pages
})

const pagedList = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  return filteredList.value.slice(start, start + pageSize.value)
})

const changePage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
  }
}

// Modal State (仅单条恢复)
const showRestoreModal = ref(false)
const currentRestoreItem = ref(null)

const handleOpenSingleRestore = (item) => {
  currentRestoreItem.value = item
  showRestoreModal.value = true
}

const confirmRestore = () => {
  if (currentRestoreItem.value) {
    emit('restore', currentRestoreItem.value)
  }
  showRestoreModal.value = false
}

const handleBack = () => {
  emit('back')
}
</script>

<style scoped>
.recycle-bin-card {
  background: #ffffff;
  border-radius: 2px;
  box-shadow: 0 1px 3px rgba(0, 21, 41, 0.05);
  display: flex;
  flex-direction: column;
  min-height: calc(100vh - 110px);
}

/* Header Nav */
.recycle-header-nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 20px;
  border-bottom: 1px solid #f0f2f5;
  background-color: #fafbfc;
}

.nav-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.btn-back-link {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  background: none;
  border: 1px solid #dcdfe6;
  border-radius: 3px;
  padding: 4px 10px;
  font-size: 12px;
  color: #606266;
  cursor: pointer;
  background-color: #ffffff;
  transition: all 0.2s;
}

.btn-back-link:hover {
  color: #2468f2;
  border-color: #2468f2;
}

.btn-back-link svg {
  width: 14px;
  height: 14px;
}

.header-divider {
  width: 1px;
  height: 16px;
  background-color: #dcdfe6;
}

.header-title {
  font-size: 14px;
  font-weight: 600;
  color: #1f2d3d;
}

/* Action Bar */
.action-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 20px;
}

.left-actions {
  display: flex;
  align-items: center;
}

/* Right Tools */
.right-tools {
  display: flex;
  align-items: center;
}

.search-filter-wrap {
  display: flex;
  align-items: center;
  gap: 10px;
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
  height: 30px;
  border: none;
  outline: none;
  padding: 0 10px;
  font-size: 13px;
  color: #606266;
  background: transparent;
  cursor: pointer;
}

.search-divider {
  width: 1px;
  height: 18px;
  background-color: #e4e7ed;
}

.search-input {
  height: 30px;
  width: 170px;
  border: none;
  outline: none;
  padding: 0 12px;
  font-size: 13px;
  color: #303133;
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
  gap: 4px;
  font-size: 13px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-search:hover {
  background-color: #1b56ce;
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
  gap: 4px;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-reset:hover {
  color: #2468f2;
  border-color: #c6e2ff;
}

.reset-icon {
  width: 14px;
  height: 14px;
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
  color: #2468f2;
  border-color: #c6e2ff;
}

.tool-icon-btn svg {
  width: 15px;
  height: 15px;
}

.tool-icon-btn.spinning svg {
  animation: spin 0.8s linear infinite;
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
  width: 160px;
  background: #ffffff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  border-radius: 4px;
  padding: 10px 14px;
  z-index: 200;
  border: 1px solid #e8ecef;
}

.popover-title {
  font-size: 12px;
  font-weight: 600;
  color: #909399;
  margin-bottom: 8px;
  padding-bottom: 4px;
  border-bottom: 1px solid #f0f2f5;
}

.col-checkbox {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: #606266;
  margin-bottom: 6px;
  cursor: pointer;
}

/* Table */
.table-container {
  flex: 1;
  overflow-x: auto;
  padding: 0 20px;
}

.recycle-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
  font-size: 13px;
}

.recycle-table thead th {
  background-color: #f7f9fb;
  color: #606266;
  font-weight: 500;
  padding: 11px 12px;
  border-bottom: 1px solid #e8ecef;
  white-space: nowrap;
}

.recycle-table tbody td {
  padding: 12px 12px;
  border-bottom: 1px solid #f0f2f5;
  color: #303133;
  font-size: 13px;
}

.table-row:hover {
  background-color: #fafbfc;
}

.col-name {
  min-width: 180px;
}

.asset-name {
  color: #303133;
  font-weight: 500;
}

.col-org {
  min-width: 170px;
  color: #606266;
}

.col-zone {
  min-width: 120px;
  color: #606266;
}

.col-time {
  width: 170px;
  color: #909399;
}

.col-op {
  width: 80px;
}

.op-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.op-link-restore {
  color: #2468f2;
  cursor: pointer;
  text-decoration: none;
  font-size: 13px;
}

.op-link-restore:hover {
  text-decoration: underline;
  color: #1b56ce;
}

.empty-cell {
  padding: 60px 0 !important;
  text-align: center;
}

.empty-wrap {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.empty-icon {
  font-size: 36px;
}

.empty-text {
  font-size: 13px;
  color: #909399;
}

/* Pagination Bar */
.pagination-bar {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding: 16px 20px 20px;
  gap: 16px;
  border-top: 1px solid #f0f2f5;
}

.total-text {
  font-size: 13px;
  color: #606266;
}

.pager-controls {
  display: flex;
  align-items: center;
  gap: 6px;
}

.pager-btn, .pager-page {
  height: 28px;
  min-width: 28px;
  padding: 0 6px;
  border: 1px solid #dcdfe6;
  background-color: #ffffff;
  color: #606266;
  border-radius: 3px;
  font-size: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
}

.pager-btn:disabled {
  color: #c0c4cc;
  border-color: #ebeef5;
  cursor: not-allowed;
}

.pager-page:hover:not(.active), .pager-btn:hover:not(:disabled) {
  border-color: #2468f2;
  color: #2468f2;
}

.pager-page.active {
  background-color: #2468f2;
  color: #ffffff;
  border-color: #2468f2;
}

.page-size-wrap {
  margin-left: 6px;
}

.page-size-select {
  height: 28px;
  padding: 0 8px;
  border: 1px solid #dcdfe6;
  border-radius: 3px;
  font-size: 12px;
  color: #606266;
  background-color: #ffffff;
  outline: none;
  cursor: pointer;
}

/* Modals */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.15s ease-out;
}

.modal-card {
  width: 560px;
  max-width: 92vw;
  background: #ffffff;
  border-radius: 4px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.modal-header {
  height: 48px;
  padding: 0 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid #e8ecef;
}

.modal-title {
  font-size: 15px;
  font-weight: 600;
  color: #1f2d3d;
}

.modal-close-btn {
  background: none;
  border: none;
  font-size: 20px;
  color: #909399;
  cursor: pointer;
}

.modal-body {
  padding: 20px;
}

.info-tip-banner {
  display: flex;
  gap: 12px;
  padding: 12px 14px;
  background-color: #f0f7ff;
  border: 1px solid #bae0ff;
  border-radius: 4px;
  margin-bottom: 16px;
}

.tip-icon svg {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}

.tip-text {
  font-size: 13px;
  color: #303133;
  line-height: 1.6;
}

.tip-text strong {
  display: block;
  font-size: 14px;
  color: #1f2d3d;
  margin-bottom: 4px;
}

.detail-table-wrap {
  border: 1px solid #e8ecef;
  border-radius: 4px;
  overflow: hidden;
}

.detail-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
  font-size: 13px;
}

.detail-table thead th {
  background-color: #f7f9fb;
  color: #606266;
  font-weight: 500;
  padding: 10px 12px;
  border-bottom: 1px solid #e8ecef;
  white-space: nowrap;
}

.detail-table tbody td {
  padding: 11px 12px;
  color: #303133;
  background-color: #ffffff;
  word-break: break-word;
}

.text-bold {
  font-weight: 600;
}

.modal-footer {
  padding: 12px 20px;
  background: #fafbfc;
  border-top: 1px solid #e8ecef;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.btn {
  height: 32px;
  padding: 0 16px;
  border-radius: 3px;
  font-size: 13px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: 1px solid transparent;
  transition: all 0.2s;
}

.btn-default {
  background: #ffffff;
  border-color: #dcdfe6;
  color: #606266;
}

.btn-default:hover {
  color: #2468f2;
  border-color: #c6e2ff;
}

.btn-primary {
  background-color: #2468f2;
  color: #ffffff;
  border-color: #2468f2;
}

.btn-primary:hover {
  background-color: #1b56ce;
  border-color: #1b56ce;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
</style>
