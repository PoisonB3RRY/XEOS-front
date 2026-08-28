<template>
  <div v-if="visible" class="modal-overlay" @click.self="close">
    <div class="modal-card">
      <div class="modal-header">
        <h3 class="modal-title">创建对象存储桶</h3>
        <button class="modal-close-btn" @click="close">×</button>
      </div>

      <div class="modal-body">
        <!-- Steps Header -->
        <div class="steps-header">
          <div :class="['step-item', { active: currentStep === 1, completed: currentStep > 1 }]">
            <span class="step-num">1</span>
            <span class="step-label">服务配置</span>
          </div>
          <div class="step-line"></div>
          <div :class="['step-item', { active: currentStep === 2 }]">
            <span class="step-num">2</span>
            <span class="step-label">确认信息</span>
          </div>
        </div>

        <!-- Step 1: Configuration Form -->
        <div v-if="currentStep === 1" class="form-container">
          <div class="form-item">
            <label class="form-label"><span class="required">*</span> 资源组织</label>
            <div class="form-content">
              <select v-model="formData.org" class="form-select">
                <option value="浦发银行租户">浦发银行租户</option>
                <option value="金融云门户系统">金融云门户系统</option>
              </select>
            </div>
          </div>

          <div class="form-item">
            <label class="form-label"><span class="required">*</span> 区域</label>
            <div class="form-content">
              <select v-model="formData.region" class="form-select">
                <option value="上海">上海 (SH)</option>
                <option value="合肥">合肥 (HF)</option>
                <option value="武汉">武汉 (WH)</option>
              </select>
            </div>
          </div>

          <div class="form-item">
            <label class="form-label"><span class="required">*</span> 存储集群</label>
            <div class="form-content">
              <select v-model="formData.cluster" class="form-select">
                <option value="cluster-stdcsp">cluster-stdcsp</option>
                <option value="xhgs-stfk">xhgs-stfk</option>
              </select>
            </div>
          </div>

          <div class="form-item">
            <label class="form-label"><span class="required">*</span> 实例名称</label>
            <div class="form-content">
              <div class="bucket-name-composite">
                <input type="text" v-model="formData.prefix1" class="composite-input short" placeholder="前缀" />
                <span class="dash">-</span>
                <input type="text" v-model="formData.prefix2" class="composite-input short" placeholder="业务" />
                <span class="dash">- bucket -</span>
                <input type="text" v-model="formData.suffix" class="composite-input flex-1" placeholder="自定义标识" />
              </div>
              <div class="form-hint">完整名称: {{ computedBucketName }}</div>
            </div>
          </div>

          <div class="form-item">
            <label class="form-label"><span class="required">*</span> 桶容量(单个)</label>
            <div class="form-content">
              <div class="input-with-unit">
                <input type="number" v-model.number="formData.capacity" class="form-input" min="1" />
                <span class="unit">GB</span>
              </div>
            </div>
          </div>

          <div class="form-item">
            <label class="form-label"><span class="required">*</span> 多版本</label>
            <div class="form-content switch-row">
              <label class="switch">
                <input type="checkbox" v-model="formData.versioning" />
                <span class="slider"></span>
              </label>
              <span class="switch-status">{{ formData.versioning ? '开启' : '关闭' }}</span>
            </div>
          </div>

          <div class="form-item">
            <label class="form-label"><span class="required">*</span> 高权限用户</label>
            <div class="form-content">
              <select v-model="formData.adminUser" class="form-select">
                <option value="dsfgdsdg-kf-0324">dsfgdsdg-kf-0324</option>
                <option value="xum-kf-20260702001">xum-kf-20260702001</option>
                <option value="admin-user-std">admin-user-std</option>
              </select>
            </div>
          </div>
        </div>

        <!-- Step 2: Confirm Information -->
        <div v-else class="confirm-container">
          <div class="confirm-item">
            <span class="confirm-label">资源组织：</span>
            <span class="confirm-val">{{ formData.org }}</span>
          </div>
          <div class="confirm-item">
            <span class="confirm-label">所属区域：</span>
            <span class="confirm-val">{{ formData.region }}</span>
          </div>
          <div class="confirm-item">
            <span class="confirm-label">所属集群：</span>
            <span class="confirm-val">{{ formData.cluster }}</span>
          </div>
          <div class="confirm-item">
            <span class="confirm-label">实例名称：</span>
            <span class="confirm-val highlight">{{ computedBucketName }}</span>
          </div>
          <div class="confirm-item">
            <span class="confirm-label">容量配额：</span>
            <span class="confirm-val">{{ formData.capacity }} GB</span>
          </div>
          <div class="confirm-item">
            <span class="confirm-label">多版本状态：</span>
            <span class="confirm-val" :class="{ 'status-open': formData.versioning }">
              {{ formData.versioning ? '已开启' : '未开启' }}
            </span>
          </div>
          <div class="confirm-item">
            <span class="confirm-label">高权限用户：</span>
            <span class="confirm-val">{{ formData.adminUser }}</span>
          </div>
        </div>
      </div>

      <div class="modal-footer">
        <button v-if="currentStep === 1" class="btn btn-default" @click="close">取消</button>
        <button v-if="currentStep === 1" class="btn btn-primary" @click="currentStep = 2">下一步</button>

        <button v-if="currentStep === 2" class="btn btn-default" @click="currentStep = 1">上一步</button>
        <button v-if="currentStep === 2" class="btn btn-primary" @click="handleCreate">确定创建</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, watch } from 'vue'

const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:visible', 'create'])

const currentStep = ref(1)

const formData = reactive({
  org: '浦发银行租户',
  region: '上海',
  cluster: 'cluster-stdcsp',
  prefix1: 'scmp',
  prefix2: 'biz',
  suffix: 'zhangzj8',
  capacity: 100,
  versioning: true,
  adminUser: 'dsfgdsdg-kf-0324'
})

const computedBucketName = computed(() => {
  const p1 = formData.prefix1 ? formData.prefix1.trim() : 'scmp'
  const p2 = formData.prefix2 ? formData.prefix2.trim() : 'biz'
  const suf = formData.suffix ? formData.suffix.trim() : 'demo'
  return `${p1}-${p2}-bucket-${suf}`
})

watch(() => props.visible, (newVal) => {
  if (newVal) {
    currentStep.value = 1
  }
})

const close = () => {
  emit('update:visible', false)
}

const handleCreate = () => {
  const now = new Date()
  const dateStr = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')} ${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}:${String(now.getSeconds()).padStart(2, '0')}`

  const newBucket = {
    name: computedBucketName.value,
    status: '可用',
    org: formData.org,
    region: formData.region === '上海' ? 'SH' : formData.region,
    cluster: formData.cluster,
    capacity: formData.capacity,
    createTime: dateStr
  }

  emit('create', newBucket)
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
  width: 680px;
  background: #ffffff;
  border-radius: 4px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
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
  padding: 24px 36px 16px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* Steps Header */
.steps-header {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  padding-bottom: 12px;
  border-bottom: 1px dashed #e8e8e8;
}

.step-item {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #8c8c8c;
}

.step-item.active {
  color: #2468f2;
}

.step-num {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 600;
}

.step-item.active .step-num {
  background: #2468f2;
  color: #ffffff;
}

.step-item.completed .step-num {
  background: #52c41a;
  color: #ffffff;
}

.step-label {
  font-size: 14px;
  font-weight: 500;
}

.step-line {
  width: 80px;
  height: 1px;
  background: #d9d9d9;
}

/* Form Styles */
.form-container {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-item {
  display: flex;
  align-items: center;
}

.form-label {
  width: 120px;
  font-size: 13px;
  color: #555555;
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

.form-select, .form-input {
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

.form-select:focus, .form-input:focus {
  border-color: #2468f2;
}

.bucket-name-composite {
  display: flex;
  align-items: center;
  gap: 6px;
}

.composite-input {
  height: 34px;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  padding: 0 8px;
  font-size: 13px;
  outline: none;
}

.composite-input:focus {
  border-color: #2468f2;
}

.composite-input.short {
  width: 90px;
}

.composite-input.flex-1 {
  flex: 1;
}

.dash {
  color: #8c8c8c;
  font-size: 12px;
}

.form-hint {
  font-size: 12px;
  color: #2468f2;
  margin-top: 4px;
}

.input-with-unit {
  position: relative;
  display: flex;
  align-items: center;
}

.input-with-unit .unit {
  position: absolute;
  right: 10px;
  color: #8c8c8c;
  font-size: 12px;
}

.switch-row {
  display: flex;
  align-items: center;
  gap: 12px;
}

.switch {
  position: relative;
  display: inline-block;
  width: 44px;
  height: 22px;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0; left: 0; right: 0; bottom: 0;
  background-color: #bfbfbf;
  transition: .3s;
  border-radius: 22px;
}

.slider:before {
  position: absolute;
  content: "";
  height: 16px;
  width: 16px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: .3s;
  border-radius: 50%;
}

input:checked + .slider {
  background-color: #2468f2;
}

input:checked + .slider:before {
  transform: translateX(22px);
}

.switch-status {
  font-size: 13px;
  color: #333333;
}

/* Confirm Container */
.confirm-container {
  display: flex;
  flex-direction: column;
  gap: 14px;
  background-color: #f9fafb;
  padding: 16px 20px;
  border-radius: 4px;
  border: 1px solid #edf2f7;
}

.confirm-item {
  display: flex;
  font-size: 13px;
}

.confirm-label {
  width: 110px;
  color: #718096;
  flex-shrink: 0;
}

.confirm-val {
  color: #2d3748;
  font-weight: 500;
}

.confirm-val.highlight {
  color: #2468f2;
}

.status-open {
  color: #52c41a;
}

.modal-footer {
  padding: 16px 36px 24px;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.btn {
  height: 34px;
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
