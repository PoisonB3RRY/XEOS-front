<template>
  <div v-if="visible" class="modal-overlay" @click.self="close">
    <div class="modal-card">
      <div class="modal-header">
        <h3 class="modal-title">删除</h3>
        <button class="modal-close-btn" @click="close">×</button>
      </div>

      <div class="modal-body">
        <!-- Warning Alert Banner -->
        <div class="warning-banner">
          <div class="warning-icon">
            <svg viewBox="0 0 24 24" fill="#fa8c16">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/>
            </svg>
          </div>
          <div class="warning-text">
            <span>{{ warningMessage }}</span>
          </div>
        </div>

        <!-- Strategy Details Table -->
        <div class="strategy-table-wrapper">
          <table class="strategy-table">
            <thead>
              <tr>
                <th>源桶</th>
                <th>目标桶</th>
                <th>跨域复制策略状态</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>{{ itemData?.sourceBucket || 'test-1' }}</td>
                <td>{{ itemData?.targetBucket || 'testdcsp' }}</td>
                <td>
                  <span class="status-badge" :class="itemData?.status === '禁用' ? 'status-disabled' : 'status-active'">
                    ● {{ itemData?.status || '启用' }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="modal-footer">
        <button class="btn btn-default" @click="close">取消</button>
        <button class="btn btn-primary" @click="handleConfirm">确定</button>
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
  itemData: {
    type: Object,
    default: () => ({
      sourceBucket: 'jgh-kf-bucket-testpulsar2',
      targetBucket: 'testdcsp',
      status: '启用'
    })
  },
  warningMessage: {
    type: String,
    default: '确定删除该跨域复制策略？删除后将停止跨区域对象复制。'
  }
})

const emit = defineEmits(['update:visible', 'confirm'])

const close = () => {
  emit('update:visible', false)
}

const handleConfirm = () => {
  emit('confirm', props.itemData)
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
  animation: fadeIn 0.2s ease;
}

.modal-card {
  width: 640px;
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
  border-bottom: 1px solid #f0f0f0;
}

.modal-title {
  font-size: 15px;
  font-weight: 600;
  color: #333333;
}

.modal-close-btn {
  background: none;
  border: none;
  font-size: 18px;
  color: #999999;
  cursor: pointer;
  padding: 4px;
  line-height: 1;
}

.modal-close-btn:hover {
  color: #333333;
}

.modal-body {
  padding: 24px 28px 16px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.warning-banner {
  background-color: #fffbe6;
  border: 1px solid #ffe58f;
  border-radius: 4px;
  padding: 12px 16px;
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.warning-icon {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
  margin-top: 2px;
}

.warning-icon svg {
  width: 18px;
  height: 18px;
}

.warning-text {
  font-size: 13px;
  color: #333333;
  line-height: 1.6;
}

.strategy-table-wrapper {
  border: 1px solid #f0f0f0;
  border-radius: 4px;
  overflow: hidden;
}

.strategy-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}

.strategy-table th {
  background-color: #fafafa;
  color: #555555;
  text-align: left;
  padding: 10px 16px;
  font-weight: 500;
  border-bottom: 1px solid #f0f0f0;
}

.strategy-table td {
  padding: 12px 16px;
  color: #333333;
  border-bottom: 1px solid #f0f0f0;
}

.status-badge {
  display: inline-flex;
  align-items: center;
  font-size: 12px;
}

.status-active {
  color: #52c41a;
}

.status-disabled {
  color: #faad14;
}

.modal-footer {
  padding: 16px 28px 24px;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.btn {
  height: 32px;
  padding: 0 20px;
  border-radius: 4px;
  font-size: 13px;
  cursor: pointer;
  font-weight: 400;
  transition: all 0.2s;
}

.btn-default {
  background: #ffffff;
  border: 1px solid #d9d9d9;
  color: #666666;
}

.btn-default:hover {
  border-color: #2468f2;
  color: #2468f2;
}

.btn-primary {
  background: #2468f2;
  border: 1px solid #2468f2;
  color: #ffffff;
}

.btn-primary:hover {
  background: #1d53c7;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
</style>
