<template>
  <div class="sfs-create-container">
    <!-- Top Step Bar -->
    <div class="step-bar">
      <div class="step-item active">
        <span class="step-num">1</span>
        <span class="step-text">服务配置</span>
      </div>
      <div v-if="showConfirmStep" class="step-line active"></div>
      <div v-if="showConfirmStep" class="step-item active">
        <span class="step-num">2</span>
        <span class="step-text">确认信息</span>
      </div>
    </div>

    <!-- Main Form Panel -->
    <div class="create-form-card">
      <!-- Step 1: Form Inputs -->
      <div v-if="!showConfirmStep" class="form-wrapper">
        <!-- 1. 资源组织 -->
        <div class="form-row">
          <label class="form-label">
            <span class="required">*</span>
            <span>资源组织</span>
          </label>
          <div class="form-field">
            <select v-model="form.org" :class="['form-select', { 'has-error': errors.org }]">
              <option value="" disabled>请选择资源组织</option>
              <option v-for="org in orgOptions" :key="org" :value="org">{{ org }}</option>
            </select>
            <div v-if="errors.org" class="field-error-tip">{{ errors.org }}</div>
          </div>
        </div>

        <!-- 2. 区域 -->
        <div class="form-row">
          <label class="form-label">
            <span class="required">*</span>
            <span>区域</span>
            <span class="info-icon" title="选择SFS实例所在的物理地域">ⓘ</span>
          </label>
          <div class="form-field">
            <select v-model="form.region" class="form-select">
              <option value="上海">上海</option>
              <option value="北京">北京</option>
              <option value="合肥">合肥</option>
              <option value="深圳">深圳</option>
            </select>
          </div>
        </div>

        <!-- 3. 可用区 -->
        <div class="form-row">
          <label class="form-label">
            <span class="required">*</span>
            <span>可用区</span>
            <span class="info-icon" title="同一区域内电力和网络相互独立的可用分区">ⓘ</span>
          </label>
          <div class="form-field">
            <select v-model="form.zone" class="form-select">
              <option value="上海通用二区L1（赵巷）">上海通用二区L1（赵巷）</option>
              <option value="上海通用一区（赵巷）">上海通用一区（赵巷）</option>
              <option value="上海通用三区（赵巷）">上海通用三区（赵巷）</option>
            </select>
          </div>
        </div>

        <!-- 4. 网络区域 -->
        <div class="form-row">
          <label class="form-label">
            <span class="required">*</span>
            <span>网络区域</span>
          </label>
          <div class="form-field">
            <select v-model="form.netZone" :class="['form-select', { 'has-error': errors.netZone }]">
              <option value="" disabled>请选择</option>
              <option value="生产业务区">生产业务区</option>
              <option value="DMZ区">DMZ区</option>
              <option value="内网办公区">内网办公区</option>
              <option value="测试区">测试区</option>
            </select>
            <div v-if="errors.netZone" class="field-error-tip">{{ errors.netZone }}</div>
          </div>
        </div>

        <!-- 5. 虚拟网络 -->
        <div class="form-row">
          <label class="form-label">
            <span class="required">*</span>
            <span>虚拟网络</span>
          </label>
          <div class="form-field">
            <div class="dual-select-wrap">
              <select v-model="form.vpc" :class="['form-select', { 'has-error': errors.vpc }]">
                <option value="" disabled>请选择</option>
                <option value="vpc-sh-prod01">vpc-sh-prod01 (10.120.0.0/16)</option>
                <option value="vpc-sh-dev01">vpc-sh-dev01 (10.121.0.0/16)</option>
                <option value="vpc-sh-test01">vpc-sh-test01 (10.122.0.0/16)</option>
              </select>
              <select v-model="form.subnet" :class="['form-select', { 'has-error': errors.subnet }]">
                <option value="" disabled>请选择</option>
                <option value="subnet-storage-01">subnet-storage-01 (10.120.10.0/24)</option>
                <option value="subnet-compute-01">subnet-compute-01 (10.120.20.0/24)</option>
                <option value="subnet-mgmt-01">subnet-mgmt-01 (10.120.30.0/24)</option>
              </select>
            </div>
            <div v-if="errors.vpc || errors.subnet" class="field-error-tip">请选择虚拟私有云及对应子网</div>
          </div>
        </div>

        <!-- 6. 安全组 -->
        <div class="form-row">
          <label class="form-label">
            <span class="required">*</span>
            <span>安全组</span>
          </label>
          <div class="form-field">
            <select v-model="form.securityGroup" :class="['form-select', { 'has-error': errors.securityGroup }]">
              <option value="" disabled>请选择</option>
              <option value="sg-sfs-default">sg-sfs-default (SFS默认安全组)</option>
              <option value="sg-all-internal">sg-all-internal (内网全通安全组)</option>
              <option value="sg-custom-sec">sg-custom-sec (自定义业务安全组)</option>
            </select>
            <div v-if="errors.securityGroup" class="field-error-tip">{{ errors.securityGroup }}</div>
          </div>
        </div>

        <!-- Subtle Section Divider -->
        <div class="form-divider"></div>

        <!-- 7. 实例名称 -->
        <div class="form-row">
          <label class="form-label">
            <span class="required">*</span>
            <span>实例名称</span>
            <span class="info-icon" title="实例名称规范：sfs-系统英文简称-自定义名称，支持小写字母、数字及中划线">ⓘ</span>
          </label>
          <div class="form-field">
            <div class="composite-name-input">
              <span class="name-prefix-tag">sfs-</span>
              <input 
                type="text" 
                v-model="form.nameSys" 
                placeholder="系统英文简称" 
                :class="['input-part sys-input', { 'has-error': errors.name }]"
              />
              <span class="name-dash">-</span>
              <input 
                type="text" 
                v-model="form.nameCustom" 
                placeholder="请输入" 
                :class="['input-part custom-input', { 'has-error': errors.name }]"
              />
            </div>
            <div class="name-preview-text">
              完整实例名：<strong>{{ fullInstanceName }}</strong>
            </div>
            <div v-if="errors.name" class="field-error-tip">{{ errors.name }}</div>
          </div>
        </div>

        <!-- 8. 类型 -->
        <div class="form-row">
          <label class="form-label">
            <span class="required">*</span>
            <span>类型</span>
          </label>
          <div class="form-field">
            <select v-model="form.type" :class="['form-select', { 'has-error': errors.type }]">
              <option value="" disabled>请选择</option>
              <option value="SFS_High_M02">SFS_High_M02 (高性能型)</option>
              <option value="SFS_SHigh_M03">SFS_SHigh_M03 (超高性能型)</option>
              <option value="SFS_Capacity_M01">SFS_Capacity_M01 (容量型)</option>
            </select>
            <div v-if="errors.type" class="field-error-tip">{{ errors.type }}</div>
          </div>
        </div>

        <!-- 9. 容量 (TB) -->
        <div class="form-row">
          <label class="form-label">
            <span class="required">*</span>
            <span>容量 (TB)</span>
          </label>
          <div class="form-field">
            <div class="capacity-input-wrap">
              <input 
                type="number" 
                v-model.number="form.capacityTb" 
                placeholder="请输入" 
                min="0.5"
                step="0.5"
                :class="['form-input', { 'has-error': errors.capacity }]"
              />
              <span class="input-unit">TB (约 {{ (form.capacityTb * 1024).toFixed(0) || 0 }} GB)</span>
            </div>
            <div v-if="errors.capacity" class="field-error-tip">{{ errors.capacity }}</div>
          </div>
        </div>

        <!-- 10. 部署环境类型 -->
        <div class="form-row">
          <label class="form-label">
            <span class="required">*</span>
            <span>部署环境类型</span>
          </label>
          <div class="form-field">
            <div class="btn-group-toggle">
              <button 
                type="button" 
                :class="['toggle-btn', { active: form.envType === '常态环境' }]"
                @click="setEnvType('常态环境')"
              >
                常态环境
              </button>
              <button 
                type="button" 
                :class="['toggle-btn', { active: form.envType === '性能测试环境' }]"
                @click="setEnvType('性能测试环境')"
              >
                性能测试环境
              </button>
            </div>
          </div>
        </div>

        <!-- 11. 部署环境 (下拉式单选框) -->
        <div class="form-row">
          <label class="form-label">
            <span class="required">*</span>
            <span>部署环境</span>
          </label>
          <div class="form-field">
            <select v-model="form.env" :class="['form-select', { 'has-error': errors.env }]">
              <option value="" disabled>请选择部署环境</option>
              <option v-for="opt in currentEnvOptions" :key="opt" :value="opt">
                {{ opt }}
              </option>
            </select>
            <div v-if="errors.env" class="field-error-tip">{{ errors.env }}</div>
          </div>
        </div>
      </div>

      <!-- Step 2: Confirm Information View -->
      <div v-else class="confirm-wrapper">
        <div class="confirm-alert">
          <span class="alert-icon">ℹ️</span>
          <span>请仔细核对以下信创文件存储配置信息，确认无误后点击“立即创建”。</span>
        </div>

        <div class="confirm-grid">
          <div class="confirm-card">
            <div class="card-title">基础与网络配置</div>
            <div class="confirm-item">
              <span class="c-label">资源组织：</span>
              <span class="c-val">{{ form.org }}</span>
            </div>
            <div class="confirm-item">
              <span class="c-label">区　　域：</span>
              <span class="c-val">{{ form.region }}</span>
            </div>
            <div class="confirm-item">
              <span class="c-label">可 用 区：</span>
              <span class="c-val">{{ form.zone }}</span>
            </div>
            <div class="confirm-item">
              <span class="c-label">网络区域：</span>
              <span class="c-val">{{ form.netZone }}</span>
            </div>
            <div class="confirm-item">
              <span class="c-label">虚拟网络：</span>
              <span class="c-val">{{ form.vpc }} / {{ form.subnet }}</span>
            </div>
            <div class="confirm-item">
              <span class="c-label">安 全 组：</span>
              <span class="c-val">{{ form.securityGroup }}</span>
            </div>
          </div>

          <div class="confirm-card">
            <div class="card-title">存储规格与性能</div>
            <div class="confirm-item">
              <span class="c-label">实例名称：</span>
              <span class="c-val font-bold text-primary">{{ fullInstanceName }}</span>
            </div>
            <div class="confirm-item">
              <span class="c-label">存储类型：</span>
              <span class="c-val">{{ form.type }}</span>
            </div>
            <div class="confirm-item">
              <span class="c-label">存储容量：</span>
              <span class="c-val font-bold">{{ form.capacityTb }} TB ({{ (form.capacityTb * 1024).toFixed(2) }} GB)</span>
            </div>
            <div class="confirm-item">
              <span class="c-label">环境类型：</span>
              <span class="c-val">{{ form.envType }}</span>
            </div>
            <div class="confirm-item">
              <span class="c-label">部署环境：</span>
              <span class="c-val font-bold text-primary">{{ form.env }}</span>
            </div>
            <div class="confirm-item">
              <span class="c-label">文件协议：</span>
              <span class="c-val">NFS v4.1 / NFS v3</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Bottom Action Bar -->
      <div class="form-bottom-actions">
        <button class="btn btn-cancel" @click="handleCancel">
          {{ showConfirmStep ? '返回修改' : '取消' }}
        </button>
        <button class="btn btn-next" @click="handleNext">
          {{ showConfirmStep ? '立即创建' : '下一步' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'

const emit = defineEmits(['cancel', 'success'])

const orgOptions = [
  '智能投研系统',
  '信用卡数据处理系统',
  '报表与信息服务平台系统',
  '数据科学家研发平台',
  '区块链应用平台',
  '智能体创设平台',
  '金融云门户系统',
  '个人网银核心系统'
]

const normalEnvOptions = [
  'DEV',
  'SIT',
  'UAT',
  'REL',
  '自动化测试',
  '自动化部署',
  '投产验证'
]

const perfEnvOptions = [
  '混沌',
  '性能全链路',
  '性能比对',
  '性能回归',
  '性能专项'
]

const form = reactive({
  org: '',
  region: '上海',
  zone: '上海通用二区L1（赵巷）',
  netZone: '',
  vpc: '',
  subnet: '',
  securityGroup: '',
  nameSys: '',
  nameCustom: '',
  type: '',
  capacityTb: 1.2,
  envType: '常态环境',
  env: 'SIT'
})

const currentEnvOptions = computed(() => {
  return form.envType === '性能测试环境' ? perfEnvOptions : normalEnvOptions
})

const setEnvType = (type) => {
  if (form.envType !== type) {
    form.envType = type
    form.env = type === '性能测试环境' ? '混沌' : 'SIT'
    errors.env = ''
  }
}

const errors = reactive({
  org: '',
  netZone: '',
  vpc: '',
  subnet: '',
  securityGroup: '',
  name: '',
  type: '',
  capacity: '',
  env: ''
})

const showConfirmStep = ref(false)

const fullInstanceName = computed(() => {
  const sys = form.nameSys.trim() || 'xxxx'
  const custom = form.nameCustom.trim() || 'yyyy'
  return `sfs-${sys}-${custom}`
})

const validateForm = () => {
  let valid = true
  // Reset errors
  Object.keys(errors).forEach(key => errors[key] = '')

  if (!form.org) {
    errors.org = '请选择资源组织'
    valid = false
  }
  if (!form.netZone) {
    errors.netZone = '请选择网络区域'
    valid = false
  }
  if (!form.vpc) {
    errors.vpc = '请选择虚拟私有云'
    valid = false
  }
  if (!form.subnet) {
    errors.subnet = '请选择对应子网'
    valid = false
  }
  if (!form.securityGroup) {
    errors.securityGroup = '请选择安全组'
    valid = false
  }
  if (!form.nameSys.trim() || !form.nameCustom.trim()) {
    errors.name = '请输入系统英文简称和自定义名称'
    valid = false
  }
  if (!form.type) {
    errors.type = '请选择文件存储类型'
    valid = false
  }
  if (!form.capacityTb || form.capacityTb <= 0) {
    errors.capacity = '请输入有效的容量'
    valid = false
  }
  if (!form.env) {
    errors.env = '请选择部署环境'
    valid = false
  }

  return valid
}

const generateUUID = () => {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    const r = Math.random() * 16 | 0
    const v = c === 'x' ? r : (r & 0x3 | 0x8)
    return v.toString(16)
  })
}

const handleCancel = () => {
  if (showConfirmStep.value) {
    showConfirmStep.value = false
  } else {
    emit('cancel')
  }
}

const handleNext = () => {
  if (!showConfirmStep.value) {
    if (validateForm()) {
      showConfirmStep.value = true
    }
  } else {
    // Confirm and submit
    const gbCapacity = (parseFloat(form.capacityTb) * 1024).toFixed(2)
    const newInstance = {
      id: generateUUID(),
      name: fullInstanceName.value,
      status: '可用',
      org: form.org,
      region: form.region,
      zone: form.zone,
      type: form.type,
      capacity: gbCapacity,
      netZone: form.netZone,
      vpc: form.vpc,
      subnet: form.subnet,
      securityGroup: form.securityGroup,
      envType: form.envType,
      env: form.env
    }
    emit('success', newInstance)
  }
}
</script>

<style scoped>
.sfs-create-container {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

/* Step Bar */
.step-bar {
  background: #ffffff;
  padding: 14px 24px;
  display: flex;
  align-items: center;
  border-radius: 2px;
  box-shadow: 0 1px 3px rgba(0, 21, 41, 0.04);
}

.step-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.step-num {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background-color: #2468f2;
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 600;
}

.step-text {
  font-size: 14px;
  font-weight: 500;
  color: #2468f2;
}

.step-line {
  flex: 1;
  max-width: 120px;
  height: 1px;
  background-color: #e4e7ed;
  margin: 0 16px;
}

.step-line.active {
  background-color: #2468f2;
}

/* Form Panel */
.create-form-card {
  background: #ffffff;
  border-radius: 2px;
  box-shadow: 0 1px 3px rgba(0, 21, 41, 0.04);
  padding: 24px 32px 30px;
  min-height: calc(100vh - 170px);
  display: flex;
  flex-direction: column;
}

.form-wrapper {
  flex: 1;
  max-width: 800px;
}

.form-row {
  display: flex;
  align-items: flex-start;
  margin-bottom: 18px;
}

.form-label {
  width: 120px;
  padding-top: 6px;
  font-size: 13px;
  color: #555555;
  display: flex;
  align-items: center;
  gap: 4px;
  flex-shrink: 0;
}

.required {
  color: #f5222d;
}

.info-icon {
  color: #8c8c8c;
  font-size: 13px;
  cursor: help;
}

.form-field {
  flex: 1;
  display: flex;
  flex-direction: column;
  max-width: 580px;
}

.form-select, .form-input {
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

.form-select:focus, .form-input:focus {
  border-color: #2468f2;
}

.form-select.has-error, .form-input.has-error, .input-part.has-error {
  border-color: #f5222d !important;
}

.field-error-tip {
  color: #f5222d;
  font-size: 12px;
  margin-top: 4px;
}

.dual-select-wrap {
  display: flex;
  align-items: center;
  gap: 12px;
}

.dual-select-wrap .form-select {
  flex: 1;
}

.form-divider {
  height: 1px;
  background-color: #f0f2f5;
  margin: 22px 0;
  max-width: 700px;
}

/* Composite Input */
.composite-name-input {
  display: flex;
  align-items: center;
  height: 32px;
  width: 100%;
}

.name-prefix-tag {
  height: 100%;
  background-color: #f5f7fa;
  border: 1px solid #dcdfe6;
  border-right: none;
  border-radius: 3px 0 0 3px;
  padding: 0 10px;
  display: flex;
  align-items: center;
  color: #606266;
  font-size: 13px;
  user-select: none;
}

.input-part {
  height: 100%;
  border: 1px solid #dcdfe6;
  padding: 0 10px;
  font-size: 13px;
  color: #333333;
  outline: none;
  transition: border-color 0.2s;
}

.input-part:focus {
  border-color: #2468f2;
  z-index: 2;
}

.sys-input {
  width: 140px;
}

.name-dash {
  padding: 0 8px;
  color: #909399;
  font-size: 14px;
  user-select: none;
}

.custom-input {
  flex: 1;
  border-radius: 0 3px 3px 0;
}

.name-preview-text {
  font-size: 12px;
  color: #8c8c8c;
  margin-top: 5px;
}

.name-preview-text strong {
  color: #2468f2;
}

/* Capacity Input */
.capacity-input-wrap {
  display: flex;
  align-items: center;
  gap: 10px;
}

.capacity-input-wrap .form-input {
  width: 160px;
}

.input-unit {
  font-size: 12.5px;
  color: #8c8c8c;
}

/* Button Group Toggle */
.btn-group-toggle {
  display: flex;
  align-items: center;
}

.toggle-btn {
  height: 32px;
  padding: 0 16px;
  font-size: 13px;
  border: 1px solid #dcdfe6;
  background-color: #ffffff;
  color: #606266;
  cursor: pointer;
  transition: all 0.2s;
}

.toggle-btn:first-child {
  border-radius: 3px 0 0 3px;
  border-right: none;
}

.toggle-btn:last-child {
  border-radius: 0 3px 3px 0;
}

.toggle-btn.active {
  background-color: #2468f2;
  border-color: #2468f2;
  color: #ffffff;
}

/* Confirm View */
.confirm-wrapper {
  flex: 1;
  max-width: 800px;
}

.confirm-alert {
  background-color: #e6f7ff;
  border: 1px solid #91d5ff;
  border-radius: 3px;
  padding: 10px 14px;
  font-size: 13px;
  color: #1890ff;
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 20px;
}

.confirm-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.confirm-card {
  background: #f7f9fb;
  border: 1px solid #e8ecef;
  border-radius: 4px;
  padding: 16px 20px;
}

.card-title {
  font-size: 14px;
  font-weight: 600;
  color: #1f2d3d;
  margin-bottom: 14px;
  padding-bottom: 8px;
  border-bottom: 1px solid #e8ecef;
}

.confirm-item {
  display: flex;
  align-items: center;
  font-size: 13px;
  margin-bottom: 10px;
}

.c-label {
  width: 80px;
  color: #8c8c8c;
  flex-shrink: 0;
}

.c-val {
  color: #333333;
}

.text-primary {
  color: #2468f2;
}

.font-bold {
  font-weight: 600;
}

/* Bottom Actions */
.form-bottom-actions {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  padding-top: 24px;
  border-top: 1px solid #f0f2f5;
  margin-top: 20px;
}

.btn {
  height: 32px;
  padding: 0 20px;
  font-size: 13px;
  border-radius: 3px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-cancel {
  background: #ffffff;
  border: 1px solid #dcdfe6;
  color: #606266;
}

.btn-cancel:hover {
  border-color: #2468f2;
  color: #2468f2;
}

.btn-next {
  background-color: #2468f2;
  border: 1px solid #2468f2;
  color: #ffffff;
}

.btn-next:hover {
  background-color: #1855d1;
  border-color: #1855d1;
}
</style>
