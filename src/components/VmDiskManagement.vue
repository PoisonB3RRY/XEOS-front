<template>
  <div class="vm-disk-container">
    <!-- Top Action Bar -->
    <div class="action-bar">
      <div class="left-actions">
        <!-- 创建按钮 -->
        <button class="btn-create" @click="showCreateDiskModal = true">
          <svg class="plus-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <line x1="12" y1="5" x2="12" y2="19" />
            <line x1="5" y1="12" x2="19" y2="12" />
          </svg>
          <span>创建</span>
        </button>

        <!-- 【用户定制需求】在创建按钮右侧添加回收站按钮 -->
        <button class="btn-trash" @click="showRecycleModal = true">
          <svg class="trash-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="3 6 5 6 21 6" />
            <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
            <line x1="10" y1="11" x2="10" y2="17" />
            <line x1="14" y1="11" x2="14" y2="17" />
          </svg>
          <span>回收站</span>
        </button>
      </div>
    </div>

    <!-- Disk Table -->
    <div class="table-card">
      <table class="disk-table">
        <thead>
          <tr>
            <th class="col-type">硬盘类型</th>
            <th class="col-name">硬盘名称</th>
            <th class="col-size">硬盘大小 (GB)</th>
            <th class="col-id">ID</th>
            <th class="col-mount">挂载点</th>
            <th class="col-status">状态</th>
            <th class="col-time">创建时间</th>
            <th class="col-op">操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="disk in diskList" :key="disk.id">
            <td class="col-type">{{ disk.type }}</td>
            <td class="col-name">{{ disk.name }}</td>
            <td class="col-size">{{ disk.size }}</td>
            <td class="col-id">{{ disk.id }}</td>
            <td class="col-mount">{{ disk.mount }}</td>
            <td class="col-status">
              <span class="status-text">{{ disk.status }}</span>
            </td>
            <td class="col-time">{{ disk.createTime }}</td>
            <td class="col-op">
              <div class="op-links">
                <a class="op-link" @click="handleExpand(disk)">扩容</a>
                <a class="op-link btn-del" @click="handleDelete(disk)">删除</a>
              </div>
            </td>
          </tr>

          <tr v-if="diskList.length === 0">
            <td colspan="8" class="empty-cell">
              <div class="empty-wrap">
                <p>暂无硬盘数据</p>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Table Footer / Pagination -->
    <div class="table-footer">
      <div class="total-info">共 {{ diskList.length }} 条</div>
      <div class="pagination">
        <button class="page-nav-btn disabled">&lt;</button>
        <button class="page-number active">1</button>
        <button class="page-nav-btn disabled">&gt;</button>
        <div class="page-size-select">10 条/页 ▾</div>
      </div>
    </div>

    <!-- Create Disk Modal -->
    <div v-if="showCreateDiskModal" class="modal-overlay" @click.self="showCreateDiskModal = false">
      <div class="modal-card">
        <div class="modal-header">
          <h3>创建硬盘</h3>
          <button class="btn-close" @click="showCreateDiskModal = false">×</button>
        </div>
        <div class="modal-body">
          <div class="form-item">
            <label>硬盘类型</label>
            <select v-model="newDisk.type" class="form-input">
              <option value="数据盘">数据盘</option>
              <option value="系统盘">系统盘</option>
            </select>
          </div>
          <div class="form-item">
            <label>硬盘名称</label>
            <input v-model="newDisk.name" class="form-input" placeholder="请输入硬盘名称" />
          </div>
          <div class="form-item">
            <label>容量大小 (GB)</label>
            <input v-model.number="newDisk.size" type="number" class="form-input" placeholder="请输入容量大小" />
          </div>
          <div class="form-item">
            <label>挂载点</label>
            <input v-model="newDisk.mount" class="form-input" placeholder="如 sdb, sdc" />
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn-cancel" @click="showCreateDiskModal = false">取消</button>
          <button class="btn-confirm" @click="confirmCreateDisk">确认</button>
        </div>
      </div>
    </div>

    <!-- Recycle Bin Modal -->
    <div v-if="showRecycleModal" class="modal-overlay" @click.self="showRecycleModal = false">
      <div class="modal-card modal-lg">
        <div class="modal-header">
          <h3>磁盘回收站</h3>
          <button class="btn-close" @click="showRecycleModal = false">×</button>
        </div>
        <div class="modal-body">
          <p class="recycle-tip">回收站保留已解绑或已删除的磁盘，支持快速恢复挂载或彻底销毁。</p>
          <table class="disk-table inner-table">
            <thead>
              <tr>
                <th>硬盘名称</th>
                <th>类型</th>
                <th>大小(GB)</th>
                <th>删除时间</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, idx) in recycledDisks" :key="idx">
                <td>{{ item.name }}</td>
                <td>{{ item.type }}</td>
                <td>{{ item.size }}</td>
                <td>{{ item.deleteTime }}</td>
                <td>
                  <a class="op-link" @click="restoreDisk(item, idx)">恢复挂载</a>
                  <a class="op-link btn-del" @click="purgeDisk(idx)">彻底删除</a>
                </td>
              </tr>
              <tr v-if="recycledDisks.length === 0">
                <td colspan="5" class="empty-cell">回收站内暂无磁盘</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="modal-footer">
          <button class="btn-cancel" @click="showRecycleModal = false">关闭</button>
        </div>
      </div>
    </div>

    <!-- Expand Disk Modal -->
    <div v-if="showExpandModal" class="modal-overlay" @click.self="showExpandModal = false">
      <div class="modal-card">
        <div class="modal-header">
          <h3>硬盘扩容 - {{ currentDisk?.name }}</h3>
          <button class="btn-close" @click="showExpandModal = false">×</button>
        </div>
        <div class="modal-body">
          <div class="form-item">
            <label>当前容量</label>
            <span>{{ currentDisk?.size }} GB</span>
          </div>
          <div class="form-item">
            <label>扩容后大小 (GB)</label>
            <input v-model.number="expandNewSize" type="number" class="form-input" :min="currentDisk?.size + 10" />
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn-cancel" @click="showExpandModal = false">取消</button>
          <button class="btn-confirm" @click="confirmExpand">确认扩容</button>
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

const diskList = ref([
  {
    type: '系统盘',
    name: `${props.instanceName}-disk0`,
    size: 130,
    id: '163bc5e3-46ad-41b5-ab17-f007d29885cb',
    mount: 'sda',
    status: '正常',
    createTime: '2026-09-14 17:31:03'
  }
])

const recycledDisks = ref([
  {
    name: `${props.instanceName}-data-bak01`,
    type: '数据盘',
    size: 100,
    deleteTime: '2026-09-13 11:20:45'
  }
])

// Modal states
const showCreateDiskModal = ref(false)
const showRecycleModal = ref(false)
const showExpandModal = ref(false)
const currentDisk = ref(null)
const expandNewSize = ref(150)

const newDisk = ref({
  type: '数据盘',
  name: `${props.instanceName}-disk1`,
  size: 50,
  mount: 'sdb'
})

const handleExpand = (disk) => {
  currentDisk.value = disk
  expandNewSize.value = disk.size + 50
  showExpandModal.value = true
}

const confirmExpand = () => {
  if (currentDisk.value && expandNewSize.value > currentDisk.value.size) {
    currentDisk.value.size = expandNewSize.value
  }
  showExpandModal.value = false
}

const handleDelete = (disk) => {
  if (confirm(`确定删除硬盘 ${disk.name} 吗？`)) {
    recycledDisks.value.push({
      name: disk.name,
      type: disk.type,
      size: disk.size,
      deleteTime: new Date().toISOString().replace('T', ' ').substring(0, 19)
    })
    diskList.value = diskList.value.filter(d => d.id !== disk.id)
  }
}

const confirmCreateDisk = () => {
  diskList.value.push({
    type: newDisk.value.type,
    name: newDisk.value.name,
    size: newDisk.value.size,
    id: 'a' + Math.random().toString(16).substring(2, 10) + '-46ad-41b5-ab17-' + Math.random().toString(16).substring(2, 14),
    mount: newDisk.value.mount,
    status: '正常',
    createTime: new Date().toISOString().replace('T', ' ').substring(0, 19)
  })
  showCreateDiskModal.value = false
}

const restoreDisk = (item, idx) => {
  recycledDisks.value.splice(idx, 1)
  diskList.value.push({
    type: item.type,
    name: item.name,
    size: item.size,
    id: 'b' + Math.random().toString(16).substring(2, 10) + '-46ad-41b5-ab17-' + Math.random().toString(16).substring(2, 14),
    mount: 'sdb',
    status: '正常',
    createTime: new Date().toISOString().replace('T', ' ').substring(0, 19)
  })
}

const purgeDisk = (idx) => {
  recycledDisks.value.splice(idx, 1)
}
</script>

<style scoped>
.vm-disk-container {
  padding: 16px 20px 24px;
}

/* Action Bar */
.action-bar {
  display: flex;
  align-items: center;
  margin-bottom: 16px;
}

.left-actions {
  display: flex;
  align-items: center;
  gap: 10px;
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
  border-color: #1a56db;
}

.plus-icon {
  width: 14px;
  height: 14px;
}

/* 回收站按钮 (用户定制需求) */
.btn-trash {
  background-color: #ffffff;
  color: #606266;
  border: 1px solid #dcdfe6;
  height: 32px;
  padding: 0 14px;
  border-radius: 4px;
  font-size: 13px;
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-trash:hover {
  color: #2468f2;
  border-color: #2468f2;
  background-color: #f5f8ff;
}

.trash-icon {
  width: 14px;
  height: 14px;
}

/* Table */
.table-card {
  background-color: #ffffff;
  border: 1px solid #e8ecef;
  border-radius: 4px;
  overflow-x: auto;
}

.disk-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
  text-align: left;
}

.disk-table thead tr {
  background-color: #f7f9fb;
  border-bottom: 1px solid #e8ecef;
}

.disk-table th {
  padding: 12px 16px;
  color: #4a5568;
  font-weight: 600;
  white-space: nowrap;
}

.disk-table td {
  padding: 13px 16px;
  color: #333333;
  border-bottom: 1px solid #f0f2f5;
  white-space: nowrap;
}

.disk-table tbody tr:hover {
  background-color: #fcfdfe;
}

.col-type {
  width: 120px;
}

.col-name {
  min-width: 160px;
}

.col-size {
  width: 140px;
}

.col-id {
  min-width: 280px;
  color: #606266;
}

.col-mount {
  width: 100px;
}

.col-status {
  width: 100px;
}

.col-time {
  width: 180px;
  color: #606266;
}

.col-op {
  width: 120px;
}

.op-links {
  display: flex;
  align-items: center;
  gap: 14px;
}

.op-link {
  color: #2468f2;
  cursor: pointer;
  text-decoration: none;
}

.op-link:hover {
  text-decoration: underline;
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

/* Pagination */
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

.page-nav-btn {
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #dcdfe6;
  background-color: #ffffff;
  border-radius: 3px;
  cursor: pointer;
  color: #606266;
}

.page-nav-btn.disabled {
  color: #c0c4cc;
  cursor: not-allowed;
  background-color: #f5f7fa;
  border-color: #e4e7ed;
}

.page-number {
  min-width: 28px;
  height: 28px;
  padding: 0 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #dcdfe6;
  background-color: #ffffff;
  border-radius: 3px;
  cursor: pointer;
  color: #606266;
}

.page-number.active {
  background-color: #ffffff;
  border-color: #2468f2;
  color: #2468f2;
  font-weight: 600;
}

.page-size-select {
  border: 1px solid #dcdfe6;
  border-radius: 3px;
  padding: 4px 8px;
  font-size: 12px;
  cursor: pointer;
  background: #ffffff;
}

/* Modals */
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
  width: 480px;
  max-width: 90vw;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  overflow: hidden;
}

.modal-lg {
  width: 680px;
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
  color: #1f2d3d;
  font-weight: 600;
}

.btn-close {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  color: #909399;
}

.btn-close:hover {
  color: #303133;
}

.modal-body {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  font-size: 13px;
}

.recycle-tip {
  margin: 0 0 12px;
  color: #909399;
  font-size: 12px;
}

.inner-table {
  border: 1px solid #e8ecef;
}

.form-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-item label {
  color: #606266;
  font-weight: 500;
}

.form-input {
  height: 34px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  padding: 0 10px;
  font-size: 13px;
  color: #303133;
}

.form-input:focus {
  border-color: #2468f2;
  outline: none;
}

.modal-footer {
  padding: 12px 20px;
  border-top: 1px solid #e8ecef;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  background-color: #fafbfc;
}

.btn-cancel {
  padding: 6px 16px;
  border: 1px solid #dcdfe6;
  background: #ffffff;
  color: #606266;
  border-radius: 4px;
  cursor: pointer;
}

.btn-cancel:hover {
  color: #2468f2;
  border-color: #2468f2;
}

.btn-confirm {
  padding: 6px 16px;
  border: 1px solid #2468f2;
  background: #2468f2;
  color: #ffffff;
  border-radius: 4px;
  cursor: pointer;
}

.btn-confirm:hover {
  background: #1a56db;
}
</style>
