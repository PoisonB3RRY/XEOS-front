<template>
  <div v-if="visible" class="modal-overlay" @click.self="close">
    <div class="modal-card">
      <div class="modal-header">
        <h3 class="modal-title">信创对象存储-桶配额扩容</h3>
        <button class="modal-close-btn" @click="close">×</button>
      </div>

      <div class="modal-body">
        <div class="warning-banner">
          <div class="warning-icon">
            <svg viewBox="0 0 24 24" fill="#fa8c16">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/>
            </svg>
          </div>
          <div class="warning-text">
            桶配额扩容即时生效，若配置了跨区域复制，请同步核对目标端存储桶容量。
          </div>
        </div>

        <div class="form-item">
          <label class="form-label">实例名称</label>
          <div class="form-content">
            <input type="text" :value="bucket?.name" disabled class="form-input disabled" />
          </div>
        </div>

        <div class="form-item">
          <label class="form-label">当前配额</label>
          <div class="form-content">
            <input type="text" :value="bucket?.quota" disabled class="form-input disabled" />
          </div>
        </div>

        <div class="form-item">
          <label class="form-label"><span class="required">*</span> 扩容后配额 (GB)</label>
          <div class="form-content">
            <input 
              type="number" 
              v-model.number="newQuota" 
              :min="currentNum"
              step="50"
              class="form-input" 
              placeholder="请输入扩容后配额"
            />
            <div class="form-tip">扩容配额需大于当前配额，单位为 GB</div>
          </div>
        </div>
      </div>

      <div class="modal-footer">
        <button class="btn btn-default" @click="close">取消</button>
        <button class="btn btn-primary" :disabled="!isValid" @click="handleSubmit">确定扩容</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

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

const newQuota = ref(0)

const currentNum = computed(() => {
  if (!props.bucket?.quota) return 100
  return parseInt(props.bucket.quota.replace(/[^0-9]/g, '')) || 100
})

watch(() => props.bucket, (val) => {
  if (val) {
    const cur = currentNum.value
    newQuota.value = cur + 100
  }
}, { immediate: true })

const isValid = computed(() => {
  return newQuota.value > currentNum.value
})

const close = () => {
  emit('update:visible', false)
}

const handleSubmit = () => {
  if (!isValid.value) return
  emit('confirm', {
    name: props.bucket.name,
    quota: `${newQuota.value}G`
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
  animation: fadeIn 0.15s ease-out;
}

.modal-card {
  width: 500px;
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
  background-color: #fffbe6;
  border: 1px solid #ffe58f;
  border-radius: 3px;
  padding: 10px 14px;
  display: flex;
  align-items: flex-start;
  gap: 10px;
  margin-bottom: 18px;
}

.warning-icon svg {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
}

.warning-text {
  font-size: 12.5px;
  color: #d46b08;
  line-height: 1.5;
}

.form-item {
  margin-bottom: 16px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-label {
  font-size: 13px;
  color: #4a5568;
}

.required {
  color: #f5222d;
  margin-right: 2px;
}

.form-content {
  display: flex;
  flex-direction: column;
}

.form-input {
  height: 32px;
  padding: 0 10px;
  border: 1px solid #dcdfe6;
  border-radius: 3px;
  font-size: 13px;
  color: #333333;
  outline: none;
  transition: border-color 0.2s;
}

.form-input:focus {
  border-color: #2468f2;
}

.form-input.disabled {
  background-color: #f5f7fa;
  color: #909399;
  cursor: not-allowed;
}

.form-tip {
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
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

.btn-primary {
  background: #2468f2;
  border: 1px solid #2468f2;
  color: #ffffff;
}

.btn-primary:hover:not(:disabled) {
  background: #1855d1;
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
</style>
