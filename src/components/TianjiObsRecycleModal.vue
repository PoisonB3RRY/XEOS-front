<template>
  <div v-if="visible" class="modal-overlay" @click.self="close">
    <div class="modal-card">
      <div class="modal-header">
        <h3 class="modal-title">移入回收站确认</h3>
        <button class="modal-close-btn" @click="close">×</button>
      </div>

      <div class="modal-body">
        <div class="warning-banner">
          <div class="warning-icon">
            <svg viewBox="0 0 24 24" fill="#2468f2">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/>
            </svg>
          </div>
          <div class="warning-text">
            <strong>确定要将该存储桶放入回收站吗？</strong>
            <div>移入回收站后，存储桶将停止对外服务，并在回收站中保留。您可以在回收站中随时将其恢复。</div>
          </div>
        </div>

        <div class="info-table-wrap">
          <table class="info-table">
            <thead>
              <tr>
                <th>存储桶名称</th>
                <th>资源组织</th>
                <th>区域</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td class="text-bold">{{ bucket?.name }}</td>
                <td>{{ bucket?.org }}</td>
                <td>{{ bucket?.region || '上海' }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="modal-footer">
        <button class="btn btn-default" @click="close">取消</button>
        <button class="btn btn-primary" @click="handleConfirmRecycle">确认回收</button>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  },
  bucket: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['update:visible', 'confirm'])

const close = () => {
  emit('update:visible', false)
}

const handleConfirmRecycle = () => {
  if (!props.bucket) return
  emit('confirm', props.bucket)
  close()
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
  padding: 0;
  line-height: 1;
}

.modal-close-btn:hover {
  color: #303133;
}

.modal-body {
  padding: 20px;
}

.warning-banner {
  display: flex;
  gap: 12px;
  padding: 12px 14px;
  background-color: #f0f7ff;
  border: 1px solid #bae0ff;
  border-radius: 4px;
  margin-bottom: 18px;
}

.warning-icon svg {
  width: 22px;
  height: 22px;
  flex-shrink: 0;
}

.warning-text {
  font-size: 13px;
  color: #595959;
  line-height: 1.6;
}

.warning-text strong {
  display: block;
  color: #1f2d3d;
  font-size: 14px;
  margin-bottom: 4px;
}

.info-table-wrap {
  border: 1px solid #e8ecef;
  border-radius: 4px;
  overflow: hidden;
}

.info-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
  font-size: 13px;
}

.info-table thead th {
  background-color: #f7f9fb;
  color: #606266;
  font-weight: 500;
  padding: 10px 12px;
  border-bottom: 1px solid #e8ecef;
  white-space: nowrap;
}

.info-table tbody td {
  padding: 11px 12px;
  color: #303133;
  background-color: #ffffff;
  word-break: break-word;
}

.text-bold {
  font-weight: 600;
  color: #1f2d3d;
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
