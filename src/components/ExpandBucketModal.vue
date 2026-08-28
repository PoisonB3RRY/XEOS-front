<template>
  <div v-if="visible" class="modal-overlay" @click.self="close">
    <div class="modal-card">
      <div class="modal-header">
        <h3 class="modal-title">桶扩容</h3>
        <button class="modal-close-btn" @click="close">×</button>
      </div>

      <div class="modal-body">
        <!-- Warning Banner -->
        <div class="warning-banner">
          <div class="warning-icon">
            <svg viewBox="0 0 24 24" fill="#fa8c16">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/>
            </svg>
          </div>
          <div class="warning-text">
            若开启跨域复制，请同步扩容到对端，保持两桶桶容量一样。
          </div>
        </div>

        <div class="form-item">
          <label class="form-label">实例名称</label>
          <div class="form-content">
            <input type="text" :value="bucketData?.name" disabled class="form-input disabled" />
          </div>
        </div>

        <div class="form-item">
          <label class="form-label">扩容后桶容量(G)</label>
          <div class="form-content">
            <input 
              type="number" 
              v-model.number="capacity" 
              placeholder="请输入扩容后容量" 
              class="form-input" 
              min="1"
            />
          </div>
        </div>
      </div>

      <div class="modal-footer">
        <button class="btn btn-default" @click="close">取消</button>
        <button class="btn btn-primary" @click="handleSubmit">确定</button>
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
  bucketData: {
    type: Object,
    default: () => ({ name: '', capacity: 1024 })
  }
})

const emit = defineEmits(['update:visible', 'confirm'])

const capacity = ref(1024)

watch(() => props.bucketData, (newVal) => {
  if (newVal) {
    capacity.value = newVal.capacity || 1024
  }
}, { immediate: true })

const close = () => {
  emit('update:visible', false)
}

const handleSubmit = () => {
  emit('confirm', {
    ...props.bucketData,
    capacity: capacity.value
  })
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
  width: 580px;
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
  padding: 24px 32px 16px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.warning-banner {
  background-color: #fffbe6;
  border: 1px solid #ffe58f;
  border-radius: 4px;
  padding: 10px 14px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.warning-icon {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
}

.warning-icon svg {
  width: 16px;
  height: 16px;
}

.warning-text {
  font-size: 13px;
  color: #d46b08;
  line-height: 1.4;
}

.form-item {
  display: flex;
  align-items: center;
}

.form-label {
  width: 110px;
  font-size: 13px;
  color: #555555;
  flex-shrink: 0;
  text-align: right;
  margin-right: 16px;
}

.form-content {
  flex: 1;
}

.form-input {
  width: 100%;
  height: 34px;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  padding: 0 10px;
  font-size: 13px;
  color: #333333;
  background-color: #ffffff;
  outline: none;
  transition: border-color 0.2s;
}

.form-input:focus {
  border-color: #2468f2;
}

.form-input.disabled {
  background-color: #f5f5f5;
  color: #666666;
  cursor: not-allowed;
  border-color: #e4e7ed;
}

.modal-footer {
  padding: 16px 32px 24px;
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
