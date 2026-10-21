<template>
  <div v-if="visible" class="modal-overlay" @click.self="close">
    <div class="modal-card wide">
      <div class="modal-header">
        <h3 class="modal-title">云硬盘回收站</h3>
        <button class="modal-close-btn" @click="close">×</button>
      </div>

      <div class="modal-body">
        <div class="info-banner">
          <span>回收站内的云硬盘保留期限为 7 天。在此期间内您可以随时将云硬盘恢复使用；逾期后系统将自动永久清理。</span>
        </div>

        <table class="recycle-table">
          <thead>
            <tr>
              <th>硬盘名称</th>
              <th>容量</th>
              <th>原挂载虚机</th>
              <th>放入回收站时间</th>
              <th>剩余保留时间</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in trashList" :key="item.id">
              <td class="font-bold">{{ item.name }}</td>
              <td>{{ item.capacity }} GB</td>
              <td>{{ item.vm }}</td>
              <td>{{ item.deleteTime }}</td>
              <td class="text-warning">{{ item.remainDays }} 天</td>
              <td>
                <div class="op-links">
                  <a class="op-link" @click="handleRestore(item)">恢复</a>
                  <a class="op-link text-danger" @click="handlePermanentDelete(item)">彻底删除</a>
                </div>
              </td>
            </tr>
            <tr v-if="trashList.length === 0">
              <td colspan="6" class="empty-cell">回收站暂无数据</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="modal-footer">
        <button class="btn btn-default" @click="close">关闭</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:visible', 'restore'])

const trashList = ref([
  {
    id: 'trash-01',
    name: 'ogls-uatap-bak-volume-0003',
    capacity: '100',
    vm: 'ogls-uatap-hkg02',
    deleteTime: '2026-10-19 14:20:11',
    remainDays: 5
  },
  {
    id: 'trash-02',
    name: 'plan-zk-tmp-volume-0005',
    capacity: '50',
    vm: 'plan-zookeeper-test02',
    deleteTime: '2026-10-20 09:12:44',
    remainDays: 6
  }
])

const close = () => {
  emit('update:visible', false)
}

const handleRestore = (item) => {
  trashList.value = trashList.value.filter(t => t.id !== item.id)
  emit('restore', item)
}

const handlePermanentDelete = (item) => {
  trashList.value = trashList.value.filter(t => t.id !== item.id)
}
</script>

<style scoped>
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

.modal-card.wide {
  width: 720px;
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
  padding: 0;
  line-height: 1;
}

.modal-close-btn:hover {
  color: #303133;
}

.modal-body {
  padding: 20px;
}

.info-banner {
  background: #e6f7ff;
  border: 1px solid #91d5ff;
  border-radius: 3px;
  padding: 10px 14px;
  font-size: 12.5px;
  color: #1890ff;
  margin-bottom: 16px;
}

.recycle-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 12.5px;
}

.recycle-table th {
  background: #f7f9fa;
  border-top: 1px solid #ebeef5;
  border-bottom: 1px solid #ebeef5;
  padding: 9px 12px;
  text-align: left;
  color: #555555;
  font-weight: 500;
}

.recycle-table td {
  padding: 10px 12px;
  border-bottom: 1px solid #f0f2f5;
  color: #333333;
}

.font-bold {
  font-weight: 600;
}

.text-warning {
  color: #fa8c16;
}

.op-links {
  display: flex;
  align-items: center;
  gap: 12px;
}

.op-link {
  color: #2468f2;
  cursor: pointer;
}

.op-link:hover {
  text-decoration: underline;
}

.op-link.text-danger {
  color: #f5222d;
}

.empty-cell {
  text-align: center;
  color: #909399;
  padding: 30px 0;
}

.modal-footer {
  height: 52px;
  padding: 0 20px;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  border-top: 1px solid #e8ecef;
  background-color: #fafbfc;
}

.btn {
  height: 32px;
  padding: 0 16px;
  border-radius: 3px;
  font-size: 13px;
  cursor: pointer;
}

.btn-default {
  background: #ffffff;
  border: 1px solid #dcdfe6;
  color: #606266;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
</style>
