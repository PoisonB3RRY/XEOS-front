<template>
  <div v-if="visible" class="modal-overlay" @click.self="close">
    <div class="modal-card">
      <div class="modal-header">
        <h3 class="modal-title">创建信创云硬盘(EVS)</h3>
        <button class="modal-close-btn" @click="close">×</button>
      </div>

      <div class="modal-body">
        <div class="form-item">
          <label class="form-label"><span class="required">*</span> 资源组织</label>
          <div class="form-content">
            <select v-model="form.org" class="form-select">
              <option value="境外分行会计核算及总账系统">境外分行会计核算及总账系统</option>
              <option value="统一客户关系管理系统">统一客户关系管理系统</option>
              <option value="客户财富分析及规划系统">客户财富分析及规划系统</option>
              <option value="Cloud-Transfer-IaaS">Cloud-Transfer-IaaS</option>
              <option value="个人网银系统">个人网银系统</option>
            </select>
          </div>
        </div>

        <div class="form-row-2">
          <div class="form-item flex-1">
            <label class="form-label"><span class="required">*</span> 区域</label>
            <div class="form-content">
              <select v-model="form.region" class="form-select">
                <option value="上海">上海</option>
                <option value="北京">北京</option>
                <option value="合肥">合肥</option>
              </select>
            </div>
          </div>

          <div class="form-item flex-1">
            <label class="form-label"><span class="required">*</span> 可用区</label>
            <div class="form-content">
              <select v-model="form.zone" class="form-select">
                <option value="上海通用二区L1（赵巷）">上海通用二区L1（赵巷）</option>
                <option value="上海通用二区L2（赵巷）">上海通用二区L2（赵巷）</option>
              </select>
            </div>
          </div>
        </div>

        <div class="form-item">
          <label class="form-label"><span class="required">*</span> 磁盘类型</label>
          <div class="form-content">
            <select v-model="form.type" class="form-select">
              <option value="高IO">高IO (SAS)</option>
              <option value="超高IO">超高IO (SSD)</option>
              <option value="极速型">极速型 (NVMe SSD)</option>
            </select>
          </div>
        </div>

        <div class="form-item">
          <label class="form-label"><span class="required">*</span> 硬盘容量 (GB)</label>
          <div class="form-content">
            <input 
              type="number" 
              v-model.number="form.capacity" 
              class="form-input" 
              placeholder="请输入容量 (10 - 32768 GB)"
              min="10"
              max="32768"
              step="10"
            />
          </div>
        </div>

        <div class="form-item">
          <label class="form-label"><span class="required">*</span> 硬盘名称</label>
          <div class="form-content">
            <input 
              type="text" 
              v-model="form.name" 
              class="form-input" 
              placeholder="例如: ucrm-prod-volume-0001"
            />
          </div>
        </div>

        <div class="form-item">
          <label class="form-label"><span class="required">*</span> 预挂载点</label>
          <div class="form-content">
            <select v-model="form.mountPoint" class="form-select">
              <option value="/dev/vda">/dev/vda (系统盘)</option>
              <option value="/dev/vdb">/dev/vdb (数据盘)</option>
              <option value="/dev/vdc">/dev/vdc (数据盘)</option>
              <option value="/dev/vdd">/dev/vdd (数据盘)</option>
            </select>
          </div>
        </div>
      </div>

      <div class="modal-footer">
        <button class="btn btn-default" @click="close">取消</button>
        <button class="btn btn-primary" :disabled="!isValid" @click="handleSubmit">确定创建</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'

const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:visible', 'success'])

const form = reactive({
  org: '统一客户关系管理系统',
  region: '上海',
  zone: '上海通用二区L1（赵巷）',
  type: '高IO',
  capacity: 100,
  name: 'ucrm-volume-new01',
  mountPoint: '/dev/vdb'
})

const isValid = computed(() => {
  return form.org && form.region && form.zone && form.name.trim() && form.capacity > 0
})

const close = () => {
  emit('update:visible', false)
}

const generateUUID = () => {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    const r = Math.random() * 16 | 0
    const v = c === 'x' ? r : (r & 0x3 | 0x8)
    return v.toString(16)
  })
}

const handleSubmit = () => {
  if (!isValid.value) return
  const newInstance = {
    id: generateUUID(),
    name: form.name.trim(),
    status: '已挂载',
    org: form.org,
    region: form.region,
    zone: form.zone,
    mountPoint: form.mountPoint,
    capacity: String(form.capacity),
    env: 'SIT'
  }
  emit('success', newInstance)
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

.form-row-2 {
  display: flex;
  gap: 16px;
}

.flex-1 {
  flex: 1;
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
  background: #ffffff;
  transition: border-color 0.2s;
  width: 100%;
}

.form-input:focus, .form-select:focus {
  border-color: #2468f2;
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
