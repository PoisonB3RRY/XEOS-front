<template>
  <div class="cors-container">
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

      <div class="right-tools">
        <button class="btn-refresh" @click="handleRefresh" title="刷新列表">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="23 4 23 10 17 10"/>
            <polyline points="1 20 1 14 7 14"/>
            <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/>
          </svg>
        </button>
      </div>
    </div>

    <!-- Table Container -->
    <div class="table-card">
      <table class="cors-table">
        <thead>
          <tr>
            <th class="col-origin">允许的来源</th>
            <th class="col-methods">允许的方法</th>
            <th class="col-headers">允许的头域</th>
            <th class="col-expose">补充头域</th>
            <th class="col-maxage">缓存时间(秒)</th>
            <th v-if="rulesList.length > 0" class="col-op">操作</th>
          </tr>
        </thead>
        <tbody v-if="rulesList.length > 0">
          <tr v-for="(rule, index) in rulesList" :key="index">
            <td class="col-origin">{{ rule.origins }}</td>
            <td class="col-methods">{{ rule.methods }}</td>
            <td class="col-headers">{{ rule.headers || '--' }}</td>
            <td class="col-expose">{{ rule.exposeHeaders || '--' }}</td>
            <td class="col-maxage">{{ rule.maxAge }}</td>
            <td class="col-op">
              <a class="op-link delete" @click="openDeleteModal(rule)">删除</a>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Empty State -->
      <div v-if="rulesList.length === 0" class="empty-state">
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
    <div v-if="rulesList.length > 0" class="table-footer">
      <div class="total-info">共 {{ rulesList.length }} 条</div>
      <div class="pagination">
        <button class="page-nav-btn disabled">&lt;</button>
        <button class="page-number active">1</button>
        <button class="page-nav-btn disabled">&gt;</button>
        <div class="page-size-select">10 条/页 ▾</div>
      </div>
    </div>

    <!-- Create CORS Modal -->
    <CreateCorsModal 
      v-model:visible="showCreateModal"
      :bucket-name="bucketName"
      @submit="handleCreateRule"
    />

    <!-- Delete Confirmation Modal -->
    <DeleteConfirmModal 
      v-model:visible="showDeleteModal"
      action-type="delete"
      :item-data="deletingRule"
      title="删除CORS规则"
      warning-message="删除CORS规则后，跨域访问该存储桶的相关跨域请求将受到限制。"
      confirm-message="确认要删除该CORS规则吗？"
      @confirm="handleConfirmDelete"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import CreateCorsModal from './CreateCorsModal.vue'
import DeleteConfirmModal from './DeleteConfirmModal.vue'

const props = defineProps({
  bucketName: {
    type: String,
    default: 'yangxw-kf-bucket-mul'
  }
})

// Sample initial data matching Image 2
const sampleRules = [
  {
    origins: 'https://www.com.com',
    methods: 'Delete',
    headers: '--',
    exposeHeaders: '--',
    maxAge: 100
  }
]

const rulesList = ref([...sampleRules])
const showCreateModal = ref(false)
const showDeleteModal = ref(false)
const deletingRule = ref(null)

const handleRefresh = () => {
  // Simulates reload
}

const handleCreateRule = (newRule) => {
  rulesList.value.unshift(newRule)
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
.cors-container {
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

.cors-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
  font-size: 13px;
}

.cors-table th {
  background-color: #f7f9fb;
  color: #555555;
  font-weight: 500;
  padding: 12px 16px;
  border-bottom: 1px solid #e8ecef;
}

.cors-table td {
  padding: 12px 16px;
  color: #333333;
  border-bottom: 1px solid #f0f2f5;
}

.col-origin { width: 26%; }
.col-methods { width: 18%; }
.col-headers { width: 18%; }
.col-expose { width: 18%; }
.col-maxage { width: 12%; }
.col-op { width: 8%; text-align: right; }

.op-link {
  color: #2468f2;
  cursor: pointer;
  font-size: 13px;
}

.op-link.delete:hover {
  color: #ff4d4f;
  text-decoration: underline;
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
