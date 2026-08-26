<template>
  <div class="ccr-container">
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

      <!-- Quick interactive toggle & search filters -->
      <div class="right-tools">
        <div class="view-mode-toggle" title="快速切换演示状态">
          <button 
            :class="['mode-btn', { active: rulesList.length === 0 }]"
            @click="clearData"
          >
            照片空状态 (暂无数据)
          </button>
          <button 
            :class="['mode-btn', { active: rulesList.length > 0 }]"
            @click="loadSampleData"
          >
            规则列表状态
          </button>
        </div>

        <div class="search-filter-wrap">
          <select v-model="searchType" class="search-select">
            <option value="target">目标桶名称</option>
            <option value="source">源桶名称</option>
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
      <table class="ccr-table">
        <thead>
          <tr>
            <th class="col-source">源桶名称</th>
            <th class="col-target">目标桶名称</th>
            <th class="col-scope">复制对象</th>
            <th class="col-status">状态</th>
            <th class="col-history">历史对象</th>
            <th v-if="filteredRules.length > 0" class="col-op">操作</th>
          </tr>
        </thead>
        <tbody v-if="filteredRules.length > 0">
          <tr v-for="(rule, index) in filteredRules" :key="index">
            <td class="col-source">
              <span class="bucket-link">{{ rule.sourceBucket }}</span>
            </td>
            <td class="col-target">
              <span class="bucket-link">{{ rule.targetBucket }}</span>
            </td>
            <td class="col-scope">{{ rule.scope }}</td>
            <td class="col-status">
              <span :class="['status-tag', rule.status === '启用' ? 'status-enabled' : 'status-disabled']">
                ● {{ rule.status }}
              </span>
            </td>
            <td class="col-history">{{ rule.historySync }}</td>
            <td class="col-op">
              <div class="op-links">
                <a class="op-link" @click="toggleRuleStatus(rule)">
                  {{ rule.status === '启用' ? '暂停' : '启用' }}
                </a>
                <a class="op-link delete" @click="openDeleteModal(rule)">删除</a>
              </div>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Empty State matching photo exactly -->
      <div v-if="filteredRules.length === 0" class="empty-state">
        <div class="empty-icon-wrap">
          <svg viewBox="0 0 120 100" class="empty-box-svg">
            <!-- Box Body -->
            <path d="M25 45 L95 45 L85 85 L35 85 Z" fill="#f0f3f6" stroke="#d5dbe2" stroke-width="1.5" />
            <!-- Box Front Flap -->
            <path d="M25 45 L40 60 L80 60 L95 45" fill="#e4e9f0" stroke="#d5dbe2" stroke-width="1.5" />
            <!-- Box Top Flaps Opened -->
            <path d="M25 45 L15 32 L48 32 L40 45" fill="#f5f7fa" stroke="#d5dbe2" stroke-width="1.5" />
            <path d="M95 45 L105 32 L72 32 L80 45" fill="#f5f7fa" stroke="#d5dbe2" stroke-width="1.5" />
            <!-- Inner Shadow / Document lines inside box -->
            <line x1="45" y1="52" x2="75" y2="52" stroke="#cbd5e1" stroke-width="2" stroke-linecap="round" />
            <line x1="50" y1="58" x2="70" y2="58" stroke="#cbd5e1" stroke-width="2" stroke-linecap="round" />
          </svg>
        </div>
        <div class="empty-text">暂无数据</div>
      </div>
    </div>

    <!-- Table Footer / Pagination (when rules exist) -->
    <div v-if="filteredRules.length > 0" class="table-footer">
      <div class="total-info">共 {{ filteredRules.length }} 条</div>
      <div class="pagination">
        <button class="page-nav-btn disabled">&lt;</button>
        <button class="page-number active">1</button>
        <button class="page-nav-btn disabled">&gt;</button>
        <div class="page-size-select">10 条/页 ▾</div>
      </div>
    </div>

    <!-- Create Rule Modal -->
    <CreateRuleModal 
      v-model:visible="showCreateModal"
      :source-bucket="currentBucketName"
      @submit="handleCreateRule"
    />

    <!-- Delete Confirmation Modal -->
    <DeleteConfirmModal 
      v-model:visible="showDeleteModal"
      :item-data="deletingRule"
      :warning-message="`存在以桶${deletingRule?.targetBucket || ''}为目标桶的跨域复制策略，该策略删除后将停止向目标桶同步数据。`"
      @confirm="handleConfirmDelete"
    />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import CreateRuleModal from './CreateRuleModal.vue'
import DeleteConfirmModal from './DeleteConfirmModal.vue'

const currentBucketName = 'jgh-kf-bucket-testpulsar2'

// Initial state is empty, matching photo/跨域复制管理列表页.jpeg
const rulesList = ref([])

const searchType = ref('target')
const searchKeyword = ref('')
const activeFilter = ref('')

const showCreateModal = ref(false)
const showDeleteModal = ref(false)
const deletingRule = ref(null)

const sampleRules = [
  {
    sourceBucket: 'jgh-kf-bucket-testpulsar2',
    targetBucket: 'testdcsp',
    scope: '全部对象',
    status: '启用',
    historySync: '同步'
  },
  {
    sourceBucket: 'jgh-kf-bucket-testpulsar2',
    targetBucket: 'test-1',
    scope: '前缀: logs/',
    status: '启用',
    historySync: '不同步'
  },
  {
    sourceBucket: 'jgh-kf-bucket-testpulsar2',
    targetBucket: 'xum3-test-20260603',
    scope: '前缀: backup/',
    status: '暂停',
    historySync: '同步'
  }
]

const loadSampleData = () => {
  rulesList.value = [...sampleRules]
}

const clearData = () => {
  rulesList.value = []
  searchKeyword.value = ''
  activeFilter.value = ''
}

const filteredRules = computed(() => {
  if (!activeFilter.value) return rulesList.value
  const kw = activeFilter.value.toLowerCase().trim()
  return rulesList.value.filter(r => {
    if (searchType.value === 'target') {
      return r.targetBucket.toLowerCase().includes(kw)
    } else {
      return r.sourceBucket.toLowerCase().includes(kw)
    }
  })
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

const toggleRuleStatus = (rule) => {
  rule.status = rule.status === '启用' ? '暂停' : '启用'
}

const openDeleteModal = (rule) => {
  deletingRule.value = rule
  showDeleteModal.value = true
}

const handleConfirmDelete = (rule) => {
  rulesList.value = rulesList.value.filter(r => r !== rule)
}
</script>

<style scoped>
.ccr-container {
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

.view-mode-toggle {
  display: flex;
  align-items: center;
  background-color: #eef2f8;
  border-radius: 4px;
  padding: 2px;
}

.mode-btn {
  background: transparent;
  border: none;
  font-size: 12px;
  padding: 4px 10px;
  color: #555555;
  border-radius: 3px;
  cursor: pointer;
  transition: all 0.15s;
}

.mode-btn.active {
  background: #ffffff;
  color: #2468f2;
  font-weight: 600;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
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

.ccr-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
  font-size: 13px;
}

.ccr-table th {
  background-color: #f7f9fb;
  color: #555555;
  font-weight: 500;
  padding: 12px 16px;
  border-bottom: 1px solid #e8ecef;
}

.ccr-table td {
  padding: 12px 16px;
  color: #333333;
  border-bottom: 1px solid #f0f2f5;
}

.col-source { width: 25%; }
.col-target { width: 25%; }
.col-scope { width: 18%; }
.col-status { width: 14%; }
.col-history { width: 10%; }
.col-op { width: 12%; text-align: right; }

.bucket-link {
  color: #2468f2;
  cursor: pointer;
}

.bucket-link:hover {
  text-decoration: underline;
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
  color: #faad14;
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
  color: #f5222d;
}

/* Empty State */
.empty-state {
  min-height: 280px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 0 60px;
}

.empty-icon-wrap {
  width: 90px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 12px;
}

.empty-box-svg {
  width: 80px;
  height: 70px;
  opacity: 0.85;
}

.empty-text {
  color: #909399;
  font-size: 13px;
  letter-spacing: 0.5px;
}

/* Table Footer / Pagination */
.table-footer {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 16px;
  margin-top: 14px;
  font-size: 13px;
  color: #606266;
}

.pagination {
  display: flex;
  align-items: center;
  gap: 6px;
}

.page-nav-btn {
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #dcdfe6;
  background: #ffffff;
  border-radius: 4px;
  cursor: pointer;
  color: #606266;
}

.page-nav-btn.disabled {
  color: #c0c4cc;
  cursor: not-allowed;
  background: #f5f7fa;
}

.page-number {
  min-width: 28px;
  height: 28px;
  padding: 0 4px;
  border: 1px solid #dcdfe6;
  background: #ffffff;
  border-radius: 4px;
  font-size: 13px;
  cursor: pointer;
  color: #606266;
}

.page-number.active {
  background-color: #2468f2;
  border-color: #2468f2;
  color: #ffffff;
  font-weight: 500;
}

.page-size-select {
  border: 1px solid #dcdfe6;
  background: #ffffff;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  cursor: pointer;
}
</style>
