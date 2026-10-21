<template>
  <div v-if="visible" class="modal-overlay" @click.self="close">
    <div class="modal-card">
      <div class="modal-header">
        <h3 class="modal-title">删除信创对象存储桶</h3>
        <button class="modal-close-btn" @click="close">×</button>
      </div>

      <div class="modal-body">
        <div class="danger-banner">
          <div class="danger-icon">
            <svg viewBox="0 0 24 24" fill="#f5222d">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/>
            </svg>
          </div>
          <div class="danger-text">
            <strong>警告：此操作无法撤销！</strong>
            <div>删除桶后，桶内的所有对象数据将被彻底销毁。请在删除前确认桶内已清空或数据已有完整备份。</div>
          </div>
        </div>

        <div class="instance-info-box">
          <div class="info-row">
            <span class="info-label">桶名称：</span>
            <span class="info-value text-bold">{{ bucket?.name }}</span>
          </div>
          <div class="info-row">
            <span class="info-label">所属组织：</span>
            <span class="info-value">{{ bucket?.org }}</span>
          </div>
          <div class="info-row">
            <span class="info-label">OBS资源池：</span>
            <span class="info-value">{{ bucket?.pool || 'ZH_DEV' }}</span>
          </div>
          <div class="info-row">
            <span class="info-label">配额容量：</span>
            <span class="info-value">{{ bucket?.quota }}</span>
          </div>
          <div class="info-row">
            <span class="info-label">部署环境：</span>
            <span class="info-value">{{ bucket?.env || 'SIT' }}</span>
          </div>
        </div>

        <div class="confirm-checkbox-wrap">
          <label class="checkbox-label">
            <input type="checkbox" v-model="hasConfirmed" />
            <span>我已了解上述风险，确认删除该存储桶</span>
          </label>
        </div>
      </div>

      <div class="modal-footer">
        <button class="btn btn-default" @click="close">取消</button>
        <button class="btn btn-danger" :disabled="!hasConfirmed" @click="handleDelete">确认删除</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

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

const hasConfirmed = ref(false)

watch(() => props.visible, (val) => {
  if (val) hasConfirmed.value = false
})

const close = () => {
  emit('update:visible', false)
}

const handleDelete = () => {
  if (!hasConfirmed.value || !props.bucket) return
  emit('confirm', props.bucket.name)
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
  width: 520px;
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

.danger-banner {
  background-color: #fff2f0;
  border: 1px solid #ffccc7;
  border-radius: 3px;
  padding: 12px 14px;
  display: flex;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 18px;
}

.danger-icon svg {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}

.danger-text {
  font-size: 12.5px;
  color: #cf1322;
  line-height: 1.5;
}

.instance-info-box {
  background-color: #f7f9fb;
  border: 1px solid #e8ecef;
  border-radius: 4px;
  padding: 12px 16px;
  margin-bottom: 16px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.info-row {
  display: flex;
  font-size: 13px;
}

.info-label {
  width: 85px;
  color: #606266;
}

.info-value {
  flex: 1;
  color: #303133;
}

.text-bold {
  font-weight: 600;
  color: #1f2d3d;
}

.confirm-checkbox-wrap {
  margin-top: 14px;
  font-size: 13px;
  color: #333333;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  user-select: none;
}

.modal-footer {
  height: 52px;
  padding: 0 20px;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 12px;
  border-top: 1px solid #e8ecef;
  background-color: #fafbfc;
}

.btn {
  height: 32px;
  padding: 0 16px;
  border-radius: 3px;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-default {
  background: #ffffff;
  border: 1px solid #dcdfe6;
  color: #606266;
}

.btn-default:hover {
  border-color: #2468f2;
  color: #2468f2;
}

.btn-danger {
  background: #f5222d;
  border: 1px solid #f5222d;
  color: #ffffff;
}

.btn-danger:hover:not(:disabled) {
  background: #d91c25;
}

.btn-danger:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
</style>
