<template>
  <div class="bucket-list-card">
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

      <!-- Right Search & Filter Bar -->
      <div class="right-tools">
        <div class="search-filter-wrap">
          <select v-model="searchField" class="search-select">
            <option value="name">实例名称</option>
            <option value="org">资源组织</option>
            <option value="cluster">所属集群</option>
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
          <button class="btn-reset" @click="handleReset">
            <svg class="reset-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/>
              <path d="M3 3v5h5"/>
            </svg>
            <span>重置</span>
          </button>
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

    <!-- Bucket Table -->
    <div class="table-card">
      <table class="bucket-table">
        <thead>
          <tr>
            <th class="col-name">实例名称</th>
            <th class="col-status">状态</th>
            <th class="col-org">资源组织</th>
            <th class="col-region">区域</th>
            <th class="col-cluster">所属集群</th>
            <th class="col-capacity">容量配额(GB)</th>
            <th class="col-time">创建时间</th>
            <th class="col-op">操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in filteredBuckets" :key="item.name + index">
            <td class="col-name">
              <a class="bucket-link" @click="handleOpenDetail(item)">{{ item.name }}</a>
            </td>
            <td class="col-status">
              <span :class="['status-badge', item.status === '可用' ? 'status-available' : 'status-deleting']">
                ● {{ item.status }}
              </span>
            </td>
            <td class="col-org">{{ item.org }}</td>
            <td class="col-region">{{ item.region }}</td>
            <td class="col-cluster">{{ item.cluster }}</td>
            <td class="col-capacity">{{ item.capacity }}</td>
            <td class="col-time">{{ item.createTime }}</td>
            <td class="col-op">
              <div class="op-links">
                <a class="op-link" @click="handleOpenAuth(item)">创建访问授权</a>
                <a class="op-link" @click="handleOpenExpand(item)">桶扩容</a>
                <a class="op-link" @click="handleOpenDelete(item)">删除</a>
              </div>
            </td>
          </tr>

          <!-- Empty State -->
          <tr v-if="filteredBuckets.length === 0">
            <td colspan="8" class="empty-cell">
              <div class="empty-wrap">
                <div class="empty-text">暂无符合条件的桶数据</div>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Table Footer / Pagination -->
    <div class="table-footer">
      <div class="total-info">共 {{ filteredBuckets.length }} 条</div>
      <div class="pagination">
        <button class="page-nav-btn disabled">&lt;</button>
        <button class="page-number active">1</button>
        <button class="page-nav-btn disabled">&gt;</button>
        <div class="page-size-select">10 条/页 ▾</div>
      </div>
    </div>

    <!-- Modals -->
    <CreateBucketModal 
      v-model:visible="showCreateModal"
      @create="handleCreateBucket"
    />

    <ExpandBucketModal 
      v-model:visible="showExpandModal"
      :bucket-data="currentBucket"
      @confirm="handleConfirmExpand"
    />

    <DeleteBucketModal 
      v-model:visible="showDeleteModal"
      :bucket-name="currentBucket?.name"
      @confirm="handleConfirmDelete"
    />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import CreateBucketModal from './CreateBucketModal.vue'
import ExpandBucketModal from './ExpandBucketModal.vue'
import DeleteBucketModal from './DeleteBucketModal.vue'

const emit = defineEmits(['select-bucket', 'open-auth'])

// Reference data matching photo/玄武云-对象存储桶 列表页.jpg exactly
const initialBuckets = [
  {
    name: 'test-1',
    status: '可用',
    org: '金融云门户系统',
    region: 'SH',
    cluster: 'cluster-stdcsp',
    capacity: 10,
    createTime: '2026-05-18 13:50:40'
  },
  {
    name: 'testdcsp',
    status: '可用',
    org: '浦发银行租户',
    region: '合肥',
    cluster: 'cluster-stdcsp',
    capacity: 1027,
    createTime: '2026-05-26 16:47:18'
  },
  {
    name: 'yangxw-test',
    status: '可用',
    org: '浦发银行租户',
    region: '合肥',
    cluster: 'cluster-stdcsp',
    capacity: 2,
    createTime: '2026-06-09 15:20:44'
  },
  {
    name: 'ystest-7-9',
    status: '可用',
    org: '浦发银行租户',
    region: '合肥',
    cluster: 'cluster-stdcsp',
    capacity: 1,
    createTime: '2026-07-31 15:11:26'
  },
  {
    name: 'yangxw-asset-name-testc',
    status: '可用',
    org: '浦发银行租户',
    region: '合肥',
    cluster: 'cluster-stdcsp',
    capacity: 2,
    createTime: '2026-08-13 17:13:29'
  },
  {
    name: 'xum3-test-20260603',
    status: '删除中',
    org: '浦发银行租户',
    region: '合肥',
    cluster: 'cluster-stdcsp',
    capacity: 5,
    createTime: '2026-06-03 16:26:18'
  }
]

const bucketList = ref([...initialBuckets])

// Filter & Search states
const searchField = ref('name')
const searchKeyword = ref('')
const activeFilterKeyword = ref('')

// Modals states
const showCreateModal = ref(false)
const showExpandModal = ref(false)
const showDeleteModal = ref(false)
const currentBucket = ref(null)

const filteredBuckets = computed(() => {
  if (!activeFilterKeyword.value) return bucketList.value
  const kw = activeFilterKeyword.value.toLowerCase().trim()
  return bucketList.value.filter(item => {
    const val = String(item[searchField.value] || '').toLowerCase()
    return val.includes(kw)
  })
})

const handleSearch = () => {
  activeFilterKeyword.value = searchKeyword.value
}

const handleReset = () => {
  searchKeyword.value = ''
  activeFilterKeyword.value = ''
}

const handleRefresh = () => {
  // Simulate refresh
}

const handleOpenDetail = (bucket) => {
  emit('select-bucket', bucket.name)
}

const handleOpenAuth = (bucket) => {
  emit('open-auth', bucket.name)
}

const handleOpenExpand = (bucket) => {
  currentBucket.value = bucket
  showExpandModal.value = true
}

const handleConfirmExpand = (updated) => {
  const target = bucketList.value.find(b => b.name === updated.name)
  if (target) {
    target.capacity = updated.capacity
  }
}

const handleOpenDelete = (bucket) => {
  currentBucket.value = bucket
  showDeleteModal.value = true
}

const handleConfirmDelete = (bucketName) => {
  bucketList.value = bucketList.value.filter(b => b.name !== bucketName)
}

const handleCreateBucket = (newBucket) => {
  bucketList.value.unshift(newBucket)
}
</script>

<style scoped>
.bucket-list-card {
  background-color: #ffffff;
  border-radius: 4px;
  min-height: calc(100vh - 110px);
  padding: 16px 20px 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
}

/* Action Bar */
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

/* Search Tools */
.right-tools {
  display: flex;
  align-items: center;
  gap: 12px;
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

.search-select:focus {
  border-color: #2468f2;
}

.search-input {
  height: 32px;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  padding: 0 10px;
  font-size: 13px;
  color: #333333;
  width: 180px;
  outline: none;
  transition: border-color 0.2s;
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
  gap: 6px;
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
  padding: 0 12px;
  background-color: #ffffff;
  color: #555555;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  cursor: pointer;
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

/* Table */
.table-card {
  border: 1px solid #e8ecef;
  border-radius: 4px;
  background: #ffffff;
  overflow: hidden;
  margin-bottom: 16px;
}

.bucket-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
  font-size: 13px;
}

.bucket-table th {
  background-color: #f7f9fb;
  color: #555555;
  font-weight: 500;
  padding: 12px 16px;
  border-bottom: 1px solid #e8ecef;
  white-space: nowrap;
}

.bucket-table td {
  padding: 12px 16px;
  color: #333333;
  border-bottom: 1px solid #f0f2f5;
}

.bucket-table tr:hover {
  background-color: #fafbfc;
}

.col-name { font-weight: 400; }
.bucket-link {
  color: #2468f2;
  cursor: pointer;
  text-decoration: none;
}

.bucket-link:hover {
  text-decoration: underline;
}

.status-badge {
  display: inline-flex;
  align-items: center;
  font-size: 12px;
  font-weight: 400;
}

.status-available {
  color: #52c41a;
}

.status-deleting {
  color: #1890ff;
}

.col-op {
  text-align: right;
  padding-right: 20px !important;
}

.op-links {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 14px;
}

.op-link {
  color: #2468f2;
  cursor: pointer;
  font-size: 13px;
  user-select: none;
}

.op-link:hover {
  text-decoration: underline;
}

.empty-cell {
  text-align: center;
  padding: 60px 0 !important;
  color: #909399;
}

/* Pagination / Footer */
.table-footer {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 16px;
  font-size: 13px;
  color: #606266;
  margin-top: auto;
  padding-top: 10px;
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
