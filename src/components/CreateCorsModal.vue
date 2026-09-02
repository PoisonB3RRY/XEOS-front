<template>
  <div v-if="visible" class="modal-overlay" @click.self="close">
    <div class="modal-card">
      <div class="modal-header">
        <div class="title-wrap">
          <h3 class="modal-title">创建CORS规则</h3>
        </div>
        <button class="modal-close-btn" @click="close">×</button>
      </div>

      <div class="modal-body">
        <!-- 1. 允许的来源 -->
        <div class="form-item">
          <label class="form-label">
            <span class="required">*</span> 允许的来源
            <span class="label-info-icon" title="指定允许跨域请求的来源域名，如 https://www.example.com，支持通配符 *">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
                <line x1="12" y1="16" x2="12" y2="12"/>
                <line x1="12" y1="8" x2="12.01" y2="8"/>
              </svg>
            </span>
          </label>
          <div class="form-content">
            <textarea 
              v-model="formData.origins" 
              placeholder="https://www.example.com" 
              class="form-textarea"
              rows="3"
            ></textarea>
          </div>
        </div>

        <!-- 2. 允许的方法 -->
        <div class="form-item">
          <label class="form-label">
            <span class="required">*</span> 允许的方法
            <span class="label-info-icon" title="指定允许的跨域 HTTP 方法">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
                <line x1="12" y1="16" x2="12" y2="12"/>
                <line x1="12" y1="8" x2="12.01" y2="8"/>
              </svg>
            </span>
          </label>
          <div class="form-content">
            <select v-model="formData.methods" class="form-select">
              <option value="" disabled>请选择</option>
              <option value="GET">GET</option>
              <option value="PUT">PUT</option>
              <option value="POST">POST</option>
              <option value="DELETE">DELETE</option>
              <option value="HEAD">HEAD</option>
              <option value="GET, PUT, POST, DELETE, HEAD">全部方法 (GET, PUT, POST, DELETE, HEAD)</option>
            </select>
          </div>
        </div>

        <!-- 3. 允许的头域 -->
        <div class="form-item">
          <label class="form-label">
            允许的头域
            <span class="label-info-icon" title="指定允许客户端在跨域请求中携带的请求头">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
                <line x1="12" y1="16" x2="12" y2="12"/>
                <line x1="12" y1="8" x2="12.01" y2="8"/>
              </svg>
            </span>
          </label>
          <div class="form-content">
            <textarea 
              v-model="formData.headers" 
              placeholder="请输入" 
              class="form-textarea"
              rows="3"
            ></textarea>
          </div>
        </div>

        <!-- 4. 补充头域 -->
        <div class="form-item">
          <label class="form-label">
            补充头域
            <span class="label-info-icon" title="指定允许客户端访问的响应头（暴露给浏览器的头域）">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
                <line x1="12" y1="16" x2="12" y2="12"/>
                <line x1="12" y1="8" x2="12.01" y2="8"/>
              </svg>
            </span>
          </label>
          <div class="form-content">
            <textarea 
              v-model="formData.exposeHeaders" 
              placeholder="请输入" 
              class="form-textarea"
              rows="3"
            ></textarea>
          </div>
        </div>

        <!-- 5. 缓存时间(秒) -->
        <div class="form-item">
          <label class="form-label">
            <span class="required">*</span> 缓存时间(秒)
            <span class="label-info-icon" title="指定浏览器对特定预检请求返回结果的缓存时间（秒）">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
                <line x1="12" y1="16" x2="12" y2="12"/>
                <line x1="12" y1="8" x2="12.01" y2="8"/>
              </svg>
            </span>
          </label>
          <div class="form-content">
            <input 
              type="number" 
              v-model.number="formData.maxAge" 
              placeholder="100" 
              class="form-input"
              min="0"
            />
          </div>
        </div>
      </div>

      <div class="modal-footer">
        <button class="btn btn-default" @click="close">取消</button>
        <button 
          class="btn btn-primary" 
          :disabled="!isFormValid" 
          @click="handleSubmit"
        >
          创建
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, computed, watch } from 'vue'

const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  },
  bucketName: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:visible', 'submit'])

const formData = reactive({
  origins: '',
  methods: '',
  headers: '',
  exposeHeaders: '',
  maxAge: 100
})

watch(() => props.visible, (val) => {
  if (val) {
    formData.origins = ''
    formData.methods = ''
    formData.headers = ''
    formData.exposeHeaders = ''
    formData.maxAge = 100
  }
})

const isFormValid = computed(() => {
  if (!formData.origins.trim()) return false
  if (!formData.methods) return false
  if (formData.maxAge === '' || formData.maxAge === null || formData.maxAge < 0) return false
  return true
})

const close = () => {
  emit('update:visible', false)
}

const handleSubmit = () => {
  if (!isFormValid.value) return

  emit('submit', {
    origins: formData.origins.trim(),
    methods: formData.methods,
    headers: formData.headers.trim() || '--',
    exposeHeaders: formData.exposeHeaders.trim() || '--',
    maxAge: Number(formData.maxAge)
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
}

.modal-card {
  width: 580px;
  max-height: 90vh;
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
  flex-shrink: 0;
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
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-item {
  display: flex;
  align-items: flex-start;
}

.form-label {
  width: 135px;
  font-size: 13px;
  color: #555555;
  padding-top: 6px;
  flex-shrink: 0;
  text-align: right;
  margin-right: 18px;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 4px;
}

.required {
  color: #ff4d4f;
  margin-right: 2px;
}

.label-info-icon {
  display: inline-flex;
  align-items: center;
  color: #999999;
  cursor: pointer;
}

.label-info-icon svg {
  width: 14px;
  height: 14px;
}

.label-info-icon:hover {
  color: #2468f2;
}

.form-content {
  flex: 1;
}

.form-input,
.form-select {
  width: 100%;
  height: 32px;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  padding: 0 10px;
  font-size: 13px;
  color: #333333;
  outline: none;
  background-color: #ffffff;
  transition: all 0.2s;
  box-sizing: border-box;
}

.form-input:focus,
.form-select:focus,
.form-textarea:focus {
  border-color: #2468f2;
  box-shadow: 0 0 0 2px rgba(36, 104, 242, 0.1);
}

.form-textarea {
  width: 100%;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  padding: 8px 10px;
  font-size: 12px;
  line-height: 1.5;
  color: #333333;
  outline: none;
  background-color: #ffffff;
  transition: all 0.2s;
  resize: vertical;
  box-sizing: border-box;
}

.modal-footer {
  height: 56px;
  padding: 0 20px;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 12px;
  border-top: 1px solid #f0f0f0;
  background: #fafafa;
  flex-shrink: 0;
}

.btn {
  height: 32px;
  padding: 0 16px;
  border-radius: 4px;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
  display: inline-flex;
  align-items: center;
  justify-content: center;
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

.btn-primary:hover:not(:disabled) {
  background: #1d53c7;
  border-color: #1d53c7;
}

.btn-primary:disabled {
  background: #bae7ff;
  border-color: #bae7ff;
  color: #ffffff;
  cursor: not-allowed;
}
</style>
