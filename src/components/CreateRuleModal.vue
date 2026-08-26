<template>
  <div v-if="visible" class="modal-overlay" @click.self="close">
    <div class="modal-card">
      <div class="modal-header">
        <h3 class="modal-title">创建跨域复制</h3>
        <button class="modal-close-btn" @click="close">×</button>
      </div>

      <div class="modal-body">
        <div class="form-item">
          <label class="form-label"><span class="required">*</span> 源桶名称</label>
          <div class="form-content">
            <input type="text" :value="sourceBucket" disabled class="form-input disabled" />
          </div>
        </div>

        <div class="form-item">
          <label class="form-label"><span class="required">*</span> 目标桶名称</label>
          <div class="form-content">
            <select v-model="formData.targetBucket" class="form-select">
              <option value="" disabled>请选择目标桶</option>
              <option v-for="bucket in targetBucketOptions" :key="bucket" :value="bucket">
                {{ bucket }}
              </option>
            </select>
          </div>
        </div>

        <div class="form-item">
          <label class="form-label"><span class="required">*</span> 复制对象</label>
          <div class="form-content">
            <div class="radio-group">
              <label class="radio-label">
                <input type="radio" value="全部对象" v-model="formData.scopeType" />
                <span>全部对象</span>
              </label>
              <label class="radio-label">
                <input type="radio" value="指定前缀" v-model="formData.scopeType" />
                <span>指定前缀</span>
              </label>
            </div>
            <div v-if="formData.scopeType === '指定前缀'" class="prefix-input-wrap">
              <input 
                type="text" 
                v-model="formData.prefix" 
                placeholder="请输入前缀，例如：backup/ 或 logs/" 
                class="form-input" 
              />
            </div>
          </div>
        </div>

        <div class="form-item">
          <label class="form-label"><span class="required">*</span> 历史对象</label>
          <div class="form-content">
            <div class="radio-group">
              <label class="radio-label">
                <input type="radio" value="同步" v-model="formData.historySync" />
                <span>同步历史对象</span>
              </label>
              <label class="radio-label">
                <input type="radio" value="不同步" v-model="formData.historySync" />
                <span>仅同步新对象 (不同步)</span>
              </label>
            </div>
          </div>
        </div>

        <div class="form-item">
          <label class="form-label"><span class="required">*</span> 策略状态</label>
          <div class="form-content">
            <div class="radio-group">
              <label class="radio-label">
                <input type="radio" value="启用" v-model="formData.status" />
                <span>启用</span>
              </label>
              <label class="radio-label">
                <input type="radio" value="暂停" v-model="formData.status" />
                <span>暂停</span>
              </label>
            </div>
          </div>
        </div>
      </div>

      <div class="modal-footer">
        <button class="btn btn-default" @click="close">取消</button>
        <button class="btn btn-primary" :disabled="!formData.targetBucket" @click="handleSubmit">
          创建
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, watch } from 'vue'

const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  },
  sourceBucket: {
    type: String,
    default: 'jgh-kf-bucket-testpulsar2'
  }
})

const emit = defineEmits(['update:visible', 'submit'])

const targetBucketOptions = [
  'testdcsp',
  'test-1',
  'xum3-test-20260603',
  'yangxw-test-qu',
  'yangxw-test',
  'ystest-7-9'
]

const formData = reactive({
  targetBucket: '',
  scopeType: '全部对象',
  prefix: '',
  historySync: '同步',
  status: '启用'
})

watch(() => props.visible, (newVal) => {
  if (newVal) {
    formData.targetBucket = ''
    formData.scopeType = '全部对象'
    formData.prefix = ''
    formData.historySync = '同步'
    formData.status = '启用'
  }
})

const close = () => {
  emit('update:visible', false)
}

const handleSubmit = () => {
  if (!formData.targetBucket) return
  const replicateScope = formData.scopeType === '全部对象' 
    ? '全部对象' 
    : `前缀: ${formData.prefix || '/'}`

  emit('submit', {
    sourceBucket: props.sourceBucket,
    targetBucket: formData.targetBucket,
    scope: replicateScope,
    status: formData.status,
    historySync: formData.historySync
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
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
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
  gap: 18px;
}

.form-item {
  display: flex;
  align-items: flex-start;
}

.form-label {
  width: 100px;
  font-size: 13px;
  color: #555555;
  padding-top: 6px;
  flex-shrink: 0;
  text-align: right;
  margin-right: 16px;
}

.required {
  color: #ff4d4f;
  margin-right: 4px;
}

.form-content {
  flex: 1;
}

.form-input, .form-select {
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

.form-input:focus, .form-select:focus {
  border-color: #2468f2;
}

.form-input.disabled {
  background-color: #f5f5f5;
  color: #666666;
  cursor: not-allowed;
  border-color: #e4e7ed;
}

.radio-group {
  display: flex;
  align-items: center;
  gap: 24px;
  height: 34px;
}

.radio-label {
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  font-size: 13px;
  color: #333333;
}

.radio-label input[type="radio"] {
  accent-color: #2468f2;
  cursor: pointer;
}

.prefix-input-wrap {
  margin-top: 8px;
}

.modal-footer {
  padding: 12px 24px 20px;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  border-top: 1px solid transparent;
}

.btn {
  height: 32px;
  padding: 0 16px;
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

.btn-primary:disabled {
  background: #a0cfff;
  border-color: #a0cfff;
  cursor: not-allowed;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
</style>
