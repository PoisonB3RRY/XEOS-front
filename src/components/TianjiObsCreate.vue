<template>
  <div class="obs-create-container">
    <!-- Top Step Bar -->
    <div class="step-bar">
      <div class="step-item active">
        <span class="step-num">1</span>
        <span class="step-text">服务配置</span>
      </div>
      <div :class="['step-line', { active: showConfirmStep }]"></div>
      <div :class="['step-item', { active: showConfirmStep }]">
        <span class="step-num">2</span>
        <span class="step-text">确认信息</span>
      </div>
    </div>

    <!-- Main Form Panel -->
    <div class="create-form-card">
      <!-- Step 1: Form Inputs -->
      <div v-if="!showConfirmStep" class="form-wrapper">
        <!-- Section 1: Infrastructure -->
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

        <div class="form-row">
          <label class="form-label">
            <span class="required">*</span>
            <span>区域</span>
          </label>
          <div class="form-field">
            <select v-model="form.region" class="form-select">
              <option value="上海">上海</option>
              <option value="北京">北京</option>
              <option value="合肥">合肥</option>
            </select>
          </div>
        </div>

        <div class="form-row">
          <label class="form-label">
            <span class="required">*</span>
            <span>OBS资源池</span>
          </label>
          <div class="form-field">
            <select v-model="form.pool" :class="['form-select', { 'has-error': errors.pool }]">
              <option value="" disabled>请选择OBS资源池</option>
              <option value="ZH_DEV">ZH_DEV (开发测试资源池)</option>
              <option value="ZH_BIZ02">ZH_BIZ02 (业务专用资源池)</option>
              <option value="ZH_PROD01">ZH_PROD01 (生产核心资源池)</option>
            </select>
            <div class="field-sub-tip">ⓘ 对象用户所属资源池需在OBS资源池内部署</div>
            <div v-if="errors.pool" class="field-error-tip">{{ errors.pool }}</div>
          </div>
        </div>

        <!-- Section Divider -->
        <div class="form-divider"></div>

        <!-- Section 2: Bucket Specification -->
        <div class="form-row">
          <label class="form-label">
            <span class="required">*</span>
            <span>实例名称</span>
            <span class="info-icon" title="桶名称命名规则：系统简称-业务标识-bucket-自定义后缀">ⓘ</span>
          </label>
          <div class="form-field">
            <div class="composite-name-input">
              <input 
                type="text" 
                v-model="form.nameSys" 
                placeholder="系统英文简称" 
                :class="['input-part sys-input', { 'has-error': errors.name }]"
              />
              <span class="name-dash">-</span>
              <input 
                type="text" 
                v-model="form.nameBiz" 
                placeholder="业务标识" 
                :class="['input-part biz-input', { 'has-error': errors.name }]"
              />
              <span class="name-tag">- bucket -</span>
              <input 
                type="text" 
                v-model="form.nameCustom" 
                placeholder="请输入" 
                :class="['input-part custom-input', { 'has-error': errors.name }]"
              />
            </div>
            <div class="name-preview-text">
              完整桶名称：<strong>{{ fullBucketName }}</strong>
            </div>
            <div v-if="errors.name" class="field-error-tip">{{ errors.name }}</div>
          </div>
        </div>

        <div class="form-row">
          <label class="form-label">
            <span class="required">*</span>
            <span>桶容量 (单个)</span>
          </label>
          <div class="form-field">
            <div class="capacity-input-wrap">
              <input 
                type="number" 
                v-model.number="form.capacity" 
                placeholder="请输入" 
                min="1"
                step="10"
                :class="['form-input', { 'has-error': errors.capacity }]"
              />
              <span class="input-unit">GB</span>
            </div>
            <div v-if="errors.capacity" class="field-error-tip">{{ errors.capacity }}</div>
          </div>
        </div>

        <div class="form-row">
          <label class="form-label">
            <span class="required">*</span>
            <span>多版本</span>
            <span class="info-icon" title="开启后将保留对象的历史版本，防止误删或覆盖数据">ⓘ</span>
          </label>
          <div class="form-field">
            <div 
              :class="['switch-toggle', { checked: form.versioning }]" 
              @click="form.versioning = !form.versioning"
            >
              <div class="switch-handle"></div>
            </div>
          </div>
        </div>

        <!-- 部署环境类型 -->
        <div class="form-row">
          <label class="form-label">
            <span class="required">*</span>
            <span>部署环境类型</span>
          </label>
          <div class="form-field">
            <div class="radio-group">
              <label class="radio-label">
                <input 
                  type="radio" 
                  value="常态环境" 
                  v-model="form.envType" 
                  @change="handleEnvTypeChange('常态环境')"
                />
                <span>常态环境</span>
              </label>
              <label class="radio-label">
                <input 
                  type="radio" 
                  value="性能测试环境" 
                  v-model="form.envType" 
                  @change="handleEnvTypeChange('性能测试环境')"
                />
                <span>性能测试环境</span>
              </label>
            </div>
          </div>
        </div>

        <!-- 部署环境 (下拉式单选框) -->
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

        <div class="form-row">
          <label class="form-label">
            <span class="required">*</span>
            <span>桶高可用策略</span>
          </label>
          <div class="form-field">
            <div class="strategy-badge">多AZ</div>
          </div>
        </div>

        <!-- Section Divider -->
        <div class="form-divider"></div>

        <!-- Section 3: Auth User -->
        <div class="form-row">
          <label class="form-label">
            <span class="required">*</span>
            <span>授权用户</span>
            <span class="info-icon" title="为新创建的对象存储桶绑定初始管理访问账号">ⓘ</span>
          </label>
          <div class="form-field">
            <select v-model="form.authUser" :class="['form-select', { 'has-error': errors.authUser }]">
              <option value="" disabled>请选择</option>
              <option value="admin_obs">admin_obs (系统管理员用户)</option>
              <option value="oaml_kf_user">oaml_kf_user (业务应用主账号)</option>
              <option value="spsd_user">spsd_user (只读审计账号)</option>
              <option value="icard_user">icard_user (信用卡中心服务账号)</option>
              <option value="app_service_user">app_service_user (基础服务账号)</option>
            </select>
            <div v-if="errors.authUser" class="field-error-tip">{{ errors.authUser }}</div>
          </div>
        </div>
      </div>

      <!-- Step 2: Confirm Information View -->
      <div v-else class="confirm-wrapper">
        <div class="confirm-alert">
          <span class="alert-icon">ℹ️</span>
          <span>请仔细核对以下信创对象存储-桶配置信息，确认无误后点击“立即创建”。</span>
        </div>

        <div class="confirm-grid">
          <div class="confirm-card">
            <div class="card-title">基础配置信息</div>
            <div class="confirm-item">
              <span class="c-label">资源组织：</span>
              <span class="c-val">{{ form.org }}</span>
            </div>
            <div class="confirm-item">
              <span class="c-label">所在区域：</span>
              <span class="c-val">{{ form.region }}</span>
            </div>
            <div class="confirm-item">
              <span class="c-label">OBS资源池：</span>
              <span class="c-val font-bold text-primary">{{ form.pool }}</span>
            </div>
            <div class="confirm-item">
              <span class="c-label">授权用户：</span>
              <span class="c-val">{{ form.authUser }}</span>
            </div>
          </div>

          <div class="confirm-card">
            <div class="card-title">存储规格与策略</div>
            <div class="confirm-item">
              <span class="c-label">实例名称：</span>
              <span class="c-val font-bold text-primary">{{ fullBucketName }}</span>
            </div>
            <div class="confirm-item">
              <span class="c-label">桶配额：</span>
              <span class="c-val font-bold">{{ form.capacity }} GB</span>
            </div>
            <div class="confirm-item">
              <span class="c-label">多版本状态：</span>
              <span class="c-val">{{ form.versioning ? '已开启' : '未开启' }}</span>
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
              <span class="c-label">高可用策略：</span>
              <span class="c-val">多AZ</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Bottom Action Bar (Centered) -->
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
  '境外分行反洗钱信息系统',
  '浦天开物研发工具体系服务平台',
  '智能问答组件系统',
  '商户类服务平台（信用卡中心）',
  '信用卡网络系统',
  '数智化贷后管理系统',
  '资本充足率管理及数据披露系统',
  '影像内容管理服务平台',
  '数字员工智能孵化管理平台',
  '金融云门户系统'
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
  pool: '',
  nameSys: '',
  nameBiz: 'kf',
  nameCustom: '',
  capacity: 200,
  versioning: false,
  envType: '常态环境',
  env: 'SIT',
  ha: '多AZ',
  authUser: ''
})

const currentEnvOptions = computed(() => {
  return form.envType === '性能测试环境' ? perfEnvOptions : normalEnvOptions
})

const handleEnvTypeChange = (type) => {
  form.envType = type
  form.env = type === '性能测试环境' ? '混沌' : 'SIT'
  errors.env = ''
}

const errors = reactive({
  org: '',
  pool: '',
  name: '',
  capacity: '',
  env: '',
  authUser: ''
})

const showConfirmStep = ref(false)

const fullBucketName = computed(() => {
  const sys = form.nameSys.trim() || 'sys'
  const biz = form.nameBiz.trim() || 'kf'
  const custom = form.nameCustom.trim() || 'bucket01'
  return `${sys}-${biz}-bucket-${custom}`
})

const validateForm = () => {
  let valid = true
  Object.keys(errors).forEach(key => errors[key] = '')

  if (!form.org) {
    errors.org = '请选择资源组织'
    valid = false
  }
  if (!form.pool) {
    errors.pool = '请选择OBS资源池'
    valid = false
  }
  if (!form.nameSys.trim() || !form.nameCustom.trim()) {
    errors.name = '请输入系统英文简称和自定义后缀'
    valid = false
  }
  if (!form.capacity || form.capacity <= 0) {
    errors.capacity = '请输入有效的桶配额'
    valid = false
  }
  if (!form.env) {
    errors.env = '请选择部署环境'
    valid = false
  }
  if (!form.authUser) {
    errors.authUser = '请选择授权用户'
    valid = false
  }

  return valid
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
    const now = new Date()
    const timeStr = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')} ${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}:${String(now.getSeconds()).padStart(2, '0')}`

    const newBucket = {
      name: fullBucketName.value,
      org: form.org,
      region: form.region,
      pool: form.pool,
      quota: `${form.capacity}G`,
      ha: '多AZ',
      createTime: timeStr,
      versioning: form.versioning,
      envType: form.envType,
      env: form.env,
      authUser: form.authUser
    }
    emit('success', newBucket)
  }
}
</script>

<style scoped>
.obs-create-container {
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
  color: #909399;
}

.step-item.active {
  color: #2468f2;
}

.step-num {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background-color: #dcdfe6;
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 600;
}

.step-item.active .step-num {
  background-color: #2468f2;
}

.step-text {
  font-size: 14px;
  font-weight: 500;
}

.step-line {
  flex: 1;
  max-width: 140px;
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

.field-sub-tip {
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
}

.field-error-tip {
  color: #f5222d;
  font-size: 12px;
  margin-top: 4px;
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

.input-part {
  height: 100%;
  border: 1px solid #dcdfe6;
  padding: 0 10px;
  font-size: 13px;
  color: #333333;
  outline: none;
  transition: border-color 0.2s;
  border-radius: 3px;
}

.input-part:focus {
  border-color: #2468f2;
  z-index: 2;
}

.sys-input {
  width: 140px;
}

.biz-input {
  width: 80px;
}

.name-dash {
  padding: 0 6px;
  color: #909399;
  user-select: none;
}

.name-tag {
  padding: 0 8px;
  color: #606266;
  font-size: 12.5px;
  user-select: none;
  white-space: nowrap;
}

.custom-input {
  flex: 1;
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
  gap: 8px;
}

.capacity-input-wrap .form-input {
  width: 180px;
}

.input-unit {
  font-size: 13px;
  color: #606266;
}

/* Switch Toggle */
.switch-toggle {
  width: 40px;
  height: 22px;
  background-color: #dcdfe6;
  border-radius: 11px;
  position: relative;
  cursor: pointer;
  transition: background-color 0.2s;
  margin-top: 5px;
}

.switch-toggle.checked {
  background-color: #2468f2;
}

.switch-handle {
  width: 18px;
  height: 18px;
  background-color: #ffffff;
  border-radius: 50%;
  position: absolute;
  top: 2px;
  left: 2px;
  transition: transform 0.2s;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
}

.switch-toggle.checked .switch-handle {
  transform: translateX(18px);
}

/* Radio Group */
.radio-group {
  display: flex;
  align-items: center;
  gap: 20px;
  padding-top: 6px;
}

.radio-label {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: #333333;
  cursor: pointer;
}

/* Strategy Badge */
.strategy-badge {
  display: inline-block;
  padding: 4px 14px;
  background-color: #e8f1ff;
  color: #2468f2;
  border: 1px solid #adc6ff;
  border-radius: 3px;
  font-size: 12.5px;
  font-weight: 500;
  width: fit-content;
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
  width: 90px;
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

/* Bottom Actions (Centered) */
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
