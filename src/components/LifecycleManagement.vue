<template>
  <div class="lifecycle-container">
    <!-- Top Action Bar -->
    <div class="action-bar">
      <div class="left-actions">
        <button class="btn-create" @click="showCreateModal = true">
          <svg class="plus-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <line x1="12" y1="5" x2="12" y2="19"/>
            <line x1="5" y1="12" x2="19" y2="12"/>
          </svg>
          <span>创建</span>
        </button>
      </div>

      <!-- Search filters -->
      <div class="right-tools">
        <div class="search-filter-wrap">
          <select v-model="searchType" class="search-select">
            <option value="ruleName">规则名称</option>
          </select>
          <input 
            type="text" 
            v-model="searchKeyword" 
            placeholder="请输入" 
            class="search-input"
            @keyup.enter="handleSearch"
          />
          <button class="btn-search" @click="handleSearch">
            <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="11" cy="11" r="8"/>
              <line x1="21" y1="21" x2="16.65" y2="16.65"/>
            </svg>
            <span>查询</span>
          </button>
          <button class="btn-reset" @click="handleReset">重置</button>
          <button class="btn-refresh" @click="handleRefresh" title="刷新列表">
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
    <div class="table-card">
      <table class="lifecycle-table">
        <thead>
          <tr>
            <th class="col-name">规则名称</th>
            <th class="col-status">状态</th>
            <th class="col-scope">规则生效范围</th>
            <th class="col-prefix">前缀</th>
            <th class="col-version">对象版本</th>
            <th class="col-expire">对象过期删除天数</th>
            <th v-if="filteredRules.length > 0" class="col-op">操作</th>
          </tr>
        </thead>
        <tbody v-if="filteredRules.length > 0">
          <tr v-for="(rule, index) in filteredRules" :key="index">
            <td class="col-name">
              <span class="rule-name-text">{{ rule.ruleName }}</span>
            </td>
            <td class="col-status">
              <span :class="['status-tag', rule.status === '启用' ? 'status-enabled' : 'status-disabled']">
                ● {{ rule.status === '启用' ? '已启用' : '已禁用' }}
              </span>
            </td>
            <td class="col-scope">{{ rule.scope || '整桶' }}</td>
            <td class="col-prefix">{{ rule.prefix || '-' }}</td>
            <td class="col-version">{{ rule.objectVersion || '历史版本' }}</td>
            <td class="col-expire">{{ rule.expireDays }}</td>
            <td class="col-op">
              <div class="op-links">
                <a class="op-link delete" @click="openActionModal(rule, 'delete')">删除</a>
                <a 
                  class="op-link" 
                  @click="openActionModal(rule, rule.status === '启用' ? 'disable' : 'enable')"
                >
                  {{ rule.status === '启用' ? '禁用' : '启用' }}
                </a>
              </div>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Empty State -->
      <div v-if="filteredRules.length === 0" class="empty-state">
        <div class="empty-icon-wrap">
          <svg viewBox="0 0 120 100" class="empty-box-svg">
            <path d="M25 45 L95 45 L85 85 L35 85 Z" fill="#f0f3f6" stroke="#d5dbe2" stroke-width="1.5" />
            <path d="M25 45 L40 60 L80 60 L95 45" fill="#e4e9f0" stroke="#d5dbe2" stroke-width="1.5" />
            <path d="M25 45 L15 32 L48 32 L40 45" fill="#f5f7fa" stroke="#d5dbe2" stroke-width="1.5" />
            <path d="M95 45 L105 32 L72 32 L80 45" fill="#f5f7fa" stroke="#d5dbe2" stroke-width="1.5" />
            <line x1="45" y1="52" x2="75" y2="52" stroke="#cbd5e1" stroke-width="2" stroke-linecap="round" />
            <line x1="50" y1="58" x2="70" y2="58" stroke="#cbd5e1" stroke-width="2" stroke-linecap="round" />
          </svg>
        </div>
        <div class="empty-text">暂无数据</div>
      </div>
    </div>

    <!-- Table Footer / Pagination -->
    <div v-if="filteredRules.length > 0" class="table-footer">
      <div class="total-info">共 {{ filteredRules.length }} 条</div>
      <div class="pagination">
        <button class="page-nav-btn disabled">&lt;</button>
        <button class="page-number active">1</button>
        <button class="page-nav-btn disabled">&gt;</button>
        <div class="page-size-select">10 条/页 ▾</div>
      </div>
    </div>

    <!-- Create Lifecycle Rule Modal -->
    <CreateLifecycleModal 
      v-model:visible="showCreateModal"
      :bucket-name="bucketName"
      @submit="handleCreateRule"
    />

    <!-- Action Confirmation Modal -->
    <DeleteConfirmModal 
      v-model:visible="showActionModal"
      :action-type="actionType"
      :item-data="targetRule"
      :title="actionModalConfig.title"
      :warning-message="actionModalConfig.warningMessage"
      :confirm-message="actionModalConfig.confirmMessage"
      @confirm="handleConfirmAction"
    />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import CreateLifecycleModal from './CreateLifecycleModal.vue'
import DeleteConfirmModal from './DeleteConfirmModal.vue'

const props = defineProps({
  bucketName: {
    type: String,
    default: 'yangxw-kf-bucket-mul'
  }
})

// Initial sample data matching Image 2
const sampleRules = [
  {
    ruleName: 'yangxwtest',
    status: '启用',
    scope: '整桶',
    prefix: '-',
    objectVersion: '历史版本',
    expireDays: 1
  }
]

const rulesList = ref([...sampleRules])

const searchType = ref('ruleName')
const searchKeyword = ref('')
const activeFilter = ref('')

const showCreateModal = ref(false)
const showActionModal = ref(false)
const actionType = ref('delete')
const targetRule = ref(null)

const filteredRules = computed(() => {
  if (!activeFilter.value) return rulesList.value
  const kw = activeFilter.value.toLowerCase().trim()
  return rulesList.value.filter(r => r.ruleName.toLowerCase().includes(kw))
})

const handleSearch = () => {
  activeFilter.value = searchKeyword.value
}

const handleReset = () => {
  searchKeyword.value = ''
  activeFilter.value = ''
}

const handleRefresh = () => {
  // Simulates reload
}

const handleCreateRule = (newRule) => {
  rulesList.value.unshift(newRule)
}

const openActionModal = (rule, type) => {
  targetRule.value = rule
  actionType.value = type
  showActionModal.value = true
}

const actionModalConfig = computed(() => {
  const name = targetRule.value?.ruleName || ''
  if (actionType.value === 'delete') {
    return {
      title: '删除生命周期规则',
      warningMessage: '删除生命周期规则后，相关对象的自动生命周期策略将停止执行。',
      confirmMessage: `确认要删除生命周期规则“${name}”吗？`
    }
  } else if (actionType.value === 'disable') {
    return {
      title: '禁用生命周期规则',
      warningMessage: '禁用后该生命周期规则将暂停执行。',
      confirmMessage: `确认要禁用生命周期规则“${name}”吗？`
    }
  } else {
    return {
      title: '启用生命周期规则',
      warningMessage: '启用后该生命周期规则将恢复执行。',
      confirmMessage: `确认要启用生命周期规则“${name}”吗？`
    }
  }
})

const handleConfirmAction = (rule, type) => {
  const currentRule = rulesList.value.find(r => r.ruleName === rule.ruleName)
  if (!currentRule) return

  if (type === 'delete') {
    rulesList.value = rulesList.value.filter(r => r.ruleName !== rule.ruleName)
  } else if (type === 'disable') {
    currentRule.status = '禁用'
  } else if (type === 'enable') {
    currentRule.status = '启用'
  }
}
</script>

<style scoped>
.lifecycle-container {
  padding: 16px 20px 24px;
}

.action-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
  flex-wrap: wrap;
  gap: 12px;
}

.left-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.btn-create {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background-color: #2468f2;
  color: #ffffff;
  border: 1px solid #2468f2;
  height: 32px;
  padding: 0 16px;
  border-radius: 4px;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 2px 4px rgba(36, 104, 242, 0.15);
}

.btn-create:hover {
  background-color: #1d53c7;
  border-color: #1d53c7;
}

.plus-icon {
  width: 14px;
  height: 14px;
}

.right-tools {
  display: flex;
  align-items: center;
  gap: 16px;
}

.search-filter-wrap {
  display: flex;
  align-items: center;
  gap: 8px;
}

.search-select {
  height: 32px;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  padding: 0 8px;
  font-size: 13px;
  color: #333333;
  outline: none;
  background: #ffffff;
}

.search-input {
  height: 32px;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  padding: 0 10px;
  font-size: 13px;
  color: #333333;
  width: 160px;
  outline: none;
}

.search-input:focus {
  border-color: #2468f2;
}

.btn-search {
  height: 32px;
  padding: 0 14px;
  background-color: #2468f2;
  color: #ffffff;
  border: 1px solid #2468f2;
  border-radius: 4px;
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-search:hover {
  background-color: #1d53c7;
}

.search-icon {
  width: 14px;
  height: 14px;
}

.btn-reset {
  height: 32px;
  padding: 0 14px;
  background-color: #ffffff;
  color: #666666;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-reset:hover {
  border-color: #2468f2;
  color: #2468f2;
}

.btn-refresh {
  height: 32px;
  width: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #ffffff;
  color: #666666;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-refresh:hover {
  border-color: #2468f2;
  color: #2468f2;
}

.btn-refresh svg {
  width: 15px;
  height: 15px;
}

/* Table styling */
.table-card {
  border: 1px solid #e8ecef;
  border-radius: 4px;
  background: #ffffff;
  overflow: hidden;
}

.lifecycle-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
  font-size: 13px;
}

.lifecycle-table th {
  background-color: #f7f9fb;
  color: #555555;
  font-weight: 500;
  padding: 12px 16px;
  border-bottom: 1px solid #e8ecef;
}

.lifecycle-table td {
  padding: 12px 16px;
  color: #333333;
  border-bottom: 1px solid #f0f2f5;
}

.col-name { width: 20%; }
.col-status { width: 14%; }
.col-scope { width: 15%; }
.col-prefix { width: 15%; }
.col-version { width: 14%; }
.col-expire { width: 12%; }
.col-op { width: 10%; text-align: right; }

.rule-name-text {
  color: #333333;
}

.status-tag {
  display: inline-flex;
  align-items: center;
  font-size: 12px;
}

.status-enabled {
  color: #52c41a;
}

.status-disabled {
  color: #8c8c8c;
}

.op-links {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 12px;
}

.op-link {
  color: #2468f2;
  cursor: pointer;
  font-size: 13px;
}

.op-link:hover {
  text-decoration: underline;
}

.op-link.delete {
  color: #2468f2;
}

.op-link.delete:hover {
  color: #ff4d4f;
}

/* Empty state */
.empty-state {
  padding: 64px 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.empty-icon-wrap {
  width: 80px;
  height: 64px;
  margin-bottom: 12px;
}

.empty-box-svg {
  width: 100%;
  height: 100%;
}

.empty-text {
  color: #999999;
  font-size: 13px;
}

/* Pagination */
.table-footer {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 16px;
  margin-top: 16px;
  font-size: 13px;
  color: #666666;
}

.pagination {
  display: flex;
  align-items: center;
  gap: 8px;
}

.page-nav-btn {
  width: 28px;
  height: 28px;
  border: 1px solid #d9d9d9;
  background: #ffffff;
  border-radius: 4px;
  color: #666666;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
}

.page-nav-btn.disabled {
  color: #cccccc;
  cursor: not-allowed;
  background: #f5f5f5;
}

.page-number {
  min-width: 28px;
  height: 28px;
  padding: 0 6px;
  border: 1px solid #2468f2;
  background: #2468f2;
  color: #ffffff;
  border-radius: 4px;
  font-size: 12px;
  cursor: pointer;
}

.page-size-select {
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  padding: 4px 8px;
  font-size: 12px;
  background: #ffffff;
  cursor: pointer;
}
</style>
