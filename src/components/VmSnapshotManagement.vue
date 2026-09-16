<template>
  <div class="vm-snapshot-container">
    <div class="action-bar">
      <button class="btn-create" @click="showCreateModal = true">
        <svg class="plus-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
          <line x1="12" y1="5" x2="12" y2="19" />
          <line x1="5" y1="12" x2="19" y2="12" />
        </svg>
        <span>创建快照</span>
      </button>
    </div>

    <div class="table-card">
      <table class="snapshot-table">
        <thead>
          <tr>
            <th>快照名称</th>
            <th>关联磁盘</th>
            <th>容量 (GB)</th>
            <th>状态</th>
            <th>创建时间</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in snapshotList" :key="item.id">
            <td>{{ item.name }}</td>
            <td>{{ item.diskName }}</td>
            <td>{{ item.size }}</td>
            <td>
              <span class="status-badge">● {{ item.status }}</span>
            </td>
            <td>{{ item.createTime }}</td>
            <td>
              <div class="op-links">
                <a class="op-link" @click="handleRollback(item)">回滚</a>
                <a class="op-link btn-del" @click="handleDelete(item)">删除</a>
              </div>
            </td>
          </tr>

          <tr v-if="snapshotList.length === 0">
            <td colspan="6" class="empty-cell">暂无快照数据</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="table-footer">
      <div class="total-info">共 {{ snapshotList.length }} 条</div>
      <div class="pagination">
        <button class="page-nav-btn disabled">&lt;</button>
        <button class="page-number active">1</button>
        <button class="page-nav-btn disabled">&gt;</button>
        <div class="page-size-select">10 条/页 ▾</div>
      </div>
    </div>

    <!-- Create Modal -->
    <div v-if="showCreateModal" class="modal-overlay" @click.self="showCreateModal = false">
      <div class="modal-card">
        <div class="modal-header">
          <h3>创建快照</h3>
          <button class="btn-close" @click="showCreateModal = false">×</button>
        </div>
        <div class="modal-body">
          <div class="form-item">
            <label>快照名称</label>
            <input v-model="newSnapshotName" class="form-input" placeholder="请输入快照名称" />
          </div>
          <div class="form-item">
            <label>目标磁盘</label>
            <select v-model="targetDisk" class="form-input">
              <option value="testlu01-disk0">testlu01-disk0 (系统盘 130G)</option>
            </select>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn-cancel" @click="showCreateModal = false">取消</button>
          <button class="btn-confirm" @click="confirmCreate">确认</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  instanceName: {
    type: String,
    default: 'testlu01'
  }
})

const snapshotList = ref([
  {
    id: 'snap-001',
    name: `${props.instanceName}-snap-init`,
    diskName: `${props.instanceName}-disk0`,
    size: 130,
    status: '正常',
    createTime: '2026-09-14 18:00:15'
  }
])

const showCreateModal = ref(false)
const newSnapshotName = ref(`${props.instanceName}-snap-bak`)
const targetDisk = ref('testlu01-disk0')

const confirmCreate = () => {
  if (newSnapshotName.value) {
    snapshotList.value.push({
      id: 'snap-' + Date.now(),
      name: newSnapshotName.value,
      diskName: targetDisk.value,
      size: 130,
      status: '正常',
      createTime: new Date().toISOString().replace('T', ' ').substring(0, 19)
    })
  }
  showCreateModal.value = false
}

const handleRollback = (item) => {
  alert(`快照 ${item.name} 回滚请求已提交！`)
}

const handleDelete = (item) => {
  if (confirm(`确定删除快照 ${item.name} 吗？`)) {
    snapshotList.value = snapshotList.value.filter(s => s.id !== item.id)
  }
}
</script>

<style scoped>
.vm-snapshot-container {
  padding: 16px 20px 24px;
}

.action-bar {
  display: flex;
  margin-bottom: 16px;
}

.btn-create {
  background-color: #2468f2;
  color: #ffffff;
  border: 1px solid #2468f2;
  height: 32px;
  padding: 0 16px;
  border-radius: 4px;
  font-size: 13px;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-create:hover {
  background-color: #1a56db;
}

.plus-icon {
  width: 14px;
  height: 14px;
}

.table-card {
  background-color: #ffffff;
  border: 1px solid #e8ecef;
  border-radius: 4px;
  overflow-x: auto;
}

.snapshot-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
  text-align: left;
}

.snapshot-table thead tr {
  background-color: #f7f9fb;
  border-bottom: 1px solid #e8ecef;
}

.snapshot-table th {
  padding: 12px 16px;
  color: #4a5568;
  font-weight: 600;
  white-space: nowrap;
}

.snapshot-table td {
  padding: 13px 16px;
  color: #333333;
  border-bottom: 1px solid #f0f2f5;
  white-space: nowrap;
}

.status-badge {
  color: #52c41a;
  font-weight: 500;
}

.op-links {
  display: flex;
  gap: 12px;
}

.op-link {
  color: #2468f2;
  cursor: pointer;
}

.btn-del {
  color: #606266;
}

.btn-del:hover {
  color: #f56c6c;
}

.empty-cell {
  text-align: center;
  padding: 40px;
  color: #909399;
}

.table-footer {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 16px;
  padding: 16px 4px 0;
  font-size: 13px;
  color: #606266;
}

.pagination {
  display: flex;
  align-items: center;
  gap: 6px;
}

.page-nav-btn, .page-number {
  min-width: 28px;
  height: 28px;
  padding: 0 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #dcdfe6;
  background-color: #ffffff;
  border-radius: 3px;
  color: #606266;
}

.page-number.active {
  border-color: #2468f2;
  color: #2468f2;
  font-weight: 600;
}

.page-size-select {
  border: 1px solid #dcdfe6;
  border-radius: 3px;
  padding: 4px 8px;
  font-size: 12px;
  background: #ffffff;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-card {
  background: #ffffff;
  border-radius: 6px;
  width: 440px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  overflow: hidden;
}

.modal-header {
  padding: 16px 20px;
  border-bottom: 1px solid #e8ecef;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.modal-header h3 {
  margin: 0;
  font-size: 15px;
}

.btn-close {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  color: #909399;
}

.modal-body {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  font-size: 13px;
}

.form-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-input {
  height: 34px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  padding: 0 10px;
}

.modal-footer {
  padding: 12px 20px;
  border-top: 1px solid #e8ecef;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  background-color: #fafbfc;
}

.btn-cancel, .btn-confirm {
  padding: 6px 16px;
  border-radius: 4px;
  cursor: pointer;
}

.btn-cancel {
  border: 1px solid #dcdfe6;
  background: #ffffff;
  color: #606266;
}

.btn-confirm {
  border: 1px solid #2468f2;
  background: #2468f2;
  color: #ffffff;
}
</style>
