<template>
  <div v-if="visible" class="modal-overlay" @click.self="close">
    <div class="modal-card">
      <div class="modal-header">
        <h3 class="modal-title">创建访问授权</h3>
        <button class="modal-close-btn" @click="close">×</button>
      </div>

      <div class="modal-body">
        <div class="info-banner">
          <span>为信创对象存储桶【{{ bucket?.name }}】授予用户的访问与读写控制权限。</span>
        </div>

        <div class="form-item">
          <label class="form-label">桶名称</label>
          <div class="form-content">
            <input type="text" :value="bucket?.name" disabled class="form-input disabled" />
          </div>
        </div>

        <div class="form-item">
          <label class="form-label"><span class="required">*</span> 被授权用户</label>
          <div class="form-content">
            <select v-model="form.user" class="form-select">
              <option value="" disabled>请选择授权对象用户</option>
              <option value="admin_obs">admin_obs (系统管理员用户)</option>
              <option value="oaml_kf_user">oaml_kf_user (业务应用主账号)</option>
              <option value="spsd_user">spsd_user (只读审计账号)</option>
              <option value="app_service_user">app_service_user (服务间调用账号)</option>
            </select>
          </div>
        </div>

        <div class="form-item">
          <label class="form-label"><span class="required">*</span> 授权权限</label>
          <div class="form-content">
            <div class="perm-options">
              <label class="perm-radio">
                <input type="radio" value="read-only" v-model="form.permission" />
                <span>只读访问 (GetObject / ListBucket)</span>
              </label>
              <label class="perm-radio">
                <input type="radio" value="read-write" v-model="form.permission" />
                <span>读写权限 (PutObject / DeleteObject / GetObject)</span>
              </label>
              <label class="perm-radio">
                <input type="radio" value="full-control" v-model="form.permission" />
                <span>完全控制 (Full Control)</span>
              </label>
            </div>
          </div>
        </div>
      </div>

      <div class="modal-footer">
        <button class="btn btn-default" @click="close">取消</button>
        <button class="btn btn-primary" :disabled="!form.user" @click="handleSubmit">确定授权</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'

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

const emit = defineEmits(['update:visible', 'success'])

const form = reactive({
  user: 'oaml_kf_user',
  permission: 'read-write'
})

const close = () => {
  emit('update:visible', false)
}

const handleSubmit = () => {
  if (!form.user) return
  emit('success', {
    bucketName: props.bucket?.name,
    user: form.user,
    permission: form.permission
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
  margin-bottom: 18px;
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

.form-input, .form-select {
  height: 32px;
  padding: 0 10px;
  border: 1px solid #dcdfe6;
  border-radius: 3px;
  font-size: 13px;
  color: #333333;
  outline: none;
  background-color: #ffffff;
  transition: border-color 0.2s;
  width: 100%;
}

.form-input.disabled {
  background-color: #f5f7fa;
  color: #909399;
  cursor: not-allowed;
}

.perm-options {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 4px;
}

.perm-radio {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12.5px;
  color: #333333;
  cursor: pointer;
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
