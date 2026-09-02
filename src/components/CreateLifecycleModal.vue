<template>
  <div v-if="visible" class="modal-overlay" @click.self="close">
    <div class="modal-card">
      <div class="modal-header">
        <div class="title-wrap">
          <h3 class="modal-title">创建生命周期规则</h3>
          <a class="help-link" href="javascript:void(0);">如何配置?</a>
        </div>
        <button class="modal-close-btn" @click="close">×</button>
      </div>

      <div class="modal-body">
        <!-- 1. 基本信息 -->
        <div class="section-group">
          <!-- 状态 -->
          <div class="form-item">
            <label class="form-label"><span class="required">*</span> 状态</label>
            <div class="form-content">
              <div class="radio-group">
                <label class="radio-label">
                  <input type="radio" value="启用" v-model="formData.status" />
                  <span>启用</span>
                </label>
                <label class="radio-label">
                  <input type="radio" value="禁用" v-model="formData.status" />
                  <span>禁用</span>
                </label>
              </div>
            </div>
          </div>

          <!-- 规则名称 -->
          <div class="form-item">
            <label class="form-label"><span class="required">*</span> 规则名称</label>
            <div class="form-content">
              <input 
                type="text" 
                v-model="formData.ruleName" 
                placeholder="请输入规则名称" 
                class="form-input" 
                maxlength="128"
              />
            </div>
          </div>

          <!-- 生效范围 -->
          <div class="form-item">
            <label class="form-label">
              <span class="required">*</span> 生效范围
              <span class="label-info-icon" title="配置规则是应用于整桶还是按前缀过滤">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="12" cy="12" r="10"/>
                  <line x1="12" y1="16" x2="12" y2="12"/>
                  <line x1="12" y1="8" x2="12.01" y2="8"/>
                </svg>
              </span>
            </label>
            <div class="form-content">
              <div class="segmented-control">
                <button 
                  type="button"
                  :class="['seg-btn', { active: formData.scope === '整桶' }]"
                  @click="formData.scope = '整桶'"
                >
                  整桶
                </button>
                <button 
                  type="button"
                  :class="['seg-btn', { active: formData.scope === '前缀' }]"
                  @click="formData.scope = '前缀'"
                >
                  前缀
                </button>
              </div>
            </div>
          </div>

          <!-- 前缀 (整桶时置灰而非隐藏) -->
          <div class="form-item">
            <label class="form-label">
              <span class="required" v-if="formData.scope === '前缀'">*</span> 前缀
              <span class="label-info-icon" title="匹配指定前缀的对象">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="12" cy="12" r="10"/>
                  <line x1="12" y1="16" x2="12" y2="12"/>
                  <line x1="12" y1="8" x2="12.01" y2="8"/>
                </svg>
              </span>
            </label>
            <div class="form-content">
              <input 
                type="text" 
                v-model="formData.prefix" 
                :disabled="formData.scope === '整桶'"
                :placeholder="formData.scope === '整桶' ? '' : '请输入对象名前缀'" 
                :class="['form-input', { 'input-disabled': formData.scope === '整桶' }]"
              />
            </div>
          </div>
        </div>

        <div class="section-divider"></div>

        <!-- 2. 当前版本 -->
        <div class="section-group">
          <div class="section-title-wrap">
            <span class="section-title">当前版本</span>
          </div>

          <!-- 当前版本：对象过期删除天数 -->
          <div class="form-item">
            <label class="form-label">对象过期删除天数</label>
            <div class="form-content">
              <div class="checkbox-input-row">
                <label class="checkbox-label">
                  <input type="checkbox" v-model="formData.enableCurrentExpire" />
                </label>
                <div class="input-wrap">
                  <input 
                    type="number" 
                    v-model.number="formData.currentExpireDays" 
                    :disabled="!formData.enableCurrentExpire"
                    placeholder="30" 
                    :class="['form-input', 'input-number', { 'input-disabled': !formData.enableCurrentExpire }]"
                    min="1"
                  />
                  <span class="label-info-icon inline-icon" title="指定当前版本对象在多少天后自动过期删除">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <circle cx="12" cy="12" r="10"/>
                      <line x1="12" y1="16" x2="12" y2="12"/>
                      <line x1="12" y1="8" x2="12.01" y2="8"/>
                    </svg>
                  </span>
                </div>
              </div>
              <div class="danger-tip-text">
                说明：当桶未启用多版本控制时，指定的对象在配置的过期时间后将被自动删除，无法找回。
              </div>
            </div>
          </div>

          <!-- 当前版本：碎片过期删除天数 -->
          <div class="form-item">
            <label class="form-label">碎片过期删除天数</label>
            <div class="form-content">
              <div class="checkbox-input-row">
                <label class="checkbox-label">
                  <input type="checkbox" v-model="formData.enableCurrentFragmentExpire" />
                </label>
                <div class="input-wrap">
                  <input 
                    type="number" 
                    v-model.number="formData.currentFragmentExpireDays" 
                    :disabled="!formData.enableCurrentFragmentExpire"
                    placeholder="30" 
                    :class="['form-input', 'input-number', { 'input-disabled': !formData.enableCurrentFragmentExpire }]"
                    min="1"
                  />
                  <span class="label-info-icon inline-icon" title="指定未完成的分段上传碎片在多少天后自动清理">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <circle cx="12" cy="12" r="10"/>
                      <line x1="12" y1="16" x2="12" y2="12"/>
                      <line x1="12" y1="8" x2="12.01" y2="8"/>
                    </svg>
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="section-divider"></div>

        <!-- 3. 历史版本 -->
        <div class="section-group">
          <div class="section-title-wrap">
            <span class="section-title">历史版本</span>
            <span class="label-info-icon" title="历史版本生命周期策略">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
                <line x1="12" y1="16" x2="12" y2="12"/>
                <line x1="12" y1="8" x2="12.01" y2="8"/>
              </svg>
            </span>
          </div>

          <!-- 历史版本：对象过期删除天数 -->
          <div class="form-item">
            <label class="form-label">对象过期删除天数</label>
            <div class="form-content">
              <div class="checkbox-input-row">
                <label class="checkbox-label">
                  <input type="checkbox" v-model="formData.enableHistoryExpire" />
                </label>
                <div class="input-wrap">
                  <input 
                    type="number" 
                    v-model.number="formData.historyExpireDays" 
                    :disabled="!formData.enableHistoryExpire"
                    placeholder="30" 
                    :class="['form-input', 'input-number', { 'input-disabled': !formData.enableHistoryExpire }]"
                    min="1"
                  />
                  <span class="label-info-icon inline-icon" title="指定历史版本对象在成为非当前版本后多少天自动永久删除">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <circle cx="12" cy="12" r="10"/>
                      <line x1="12" y1="16" x2="12" y2="12"/>
                      <line x1="12" y1="8" x2="12.01" y2="8"/>
                    </svg>
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="modal-footer">
        <button 
          class="btn btn-primary" 
          :disabled="!isFormValid" 
          @click="handleSubmit"
        >
          确定
        </button>
        <button class="btn btn-default" @click="close">取消</button>
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
  // 1. 基本信息
  status: '启用',
  ruleName: '',
  scope: '整桶',
  prefix: '',
  // 2. 当前版本
  enableCurrentExpire: false,
  currentExpireDays: 30,
  enableCurrentFragmentExpire: false,
  currentFragmentExpireDays: 30,
  // 3. 历史版本
  enableHistoryExpire: false,
  historyExpireDays: 30
})

watch(() => props.visible, (val) => {
  if (val) {
    formData.status = '启用'
    formData.ruleName = ''
    formData.scope = '整桶'
    formData.prefix = ''
    formData.enableCurrentExpire = false
    formData.currentExpireDays = 30
    formData.enableCurrentFragmentExpire = false
    formData.currentFragmentExpireDays = 30
    formData.enableHistoryExpire = false
    formData.historyExpireDays = 30
  }
})

const isFormValid = computed(() => {
  if (!formData.ruleName.trim()) return false
  if (formData.scope === '前缀' && !formData.prefix.trim()) return false
  
  // 至少勾选一项过期策略
  const hasAnyPolicy = formData.enableCurrentExpire || formData.enableCurrentFragmentExpire || formData.enableHistoryExpire
  if (!hasAnyPolicy) return false

  if (formData.enableCurrentExpire && (!formData.currentExpireDays || formData.currentExpireDays <= 0)) return false
  if (formData.enableCurrentFragmentExpire && (!formData.currentFragmentExpireDays || formData.currentFragmentExpireDays <= 0)) return false
  if (formData.enableHistoryExpire && (!formData.historyExpireDays || formData.historyExpireDays <= 0)) return false

  return true
})

const close = () => {
  emit('update:visible', false)
}

const handleSubmit = () => {
  if (!isFormValid.value) return

  // 计算版本汇总与过期天数展示
  const versions = []
  if (formData.enableCurrentExpire || formData.enableCurrentFragmentExpire) versions.push('当前版本')
  if (formData.enableHistoryExpire) versions.push('历史版本')

  const expireDays = formData.enableCurrentExpire 
    ? formData.currentExpireDays 
    : (formData.enableHistoryExpire ? formData.historyExpireDays : (formData.enableCurrentFragmentExpire ? formData.currentFragmentExpireDays : 30))

  emit('submit', {
    ruleName: formData.ruleName.trim(),
    status: formData.status,
    scope: formData.scope,
    prefix: formData.scope === '前缀' ? formData.prefix.trim() : '-',
    objectVersion: versions.join(', ') || '当前版本',
    expireDays: expireDays,
    enableCurrentExpire: formData.enableCurrentExpire,
    currentExpireDays: formData.enableCurrentExpire ? Number(formData.currentExpireDays) : null,
    enableCurrentFragmentExpire: formData.enableCurrentFragmentExpire,
    currentFragmentExpireDays: formData.enableCurrentFragmentExpire ? Number(formData.currentFragmentExpireDays) : null,
    enableHistoryExpire: formData.enableHistoryExpire,
    historyExpireDays: formData.enableHistoryExpire ? Number(formData.historyExpireDays) : null
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
  width: 640px;
  max-height: 92vh;
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

.title-wrap {
  display: flex;
  align-items: center;
  gap: 8px;
}

.modal-title {
  font-size: 15px;
  font-weight: 600;
  color: #333333;
}

.help-link {
  font-size: 12px;
  color: #2468f2;
  text-decoration: none;
}

.help-link:hover {
  text-decoration: underline;
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
  padding: 20px 24px 16px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.section-group {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.section-title-wrap {
  display: flex;
  align-items: center;
  gap: 4px;
  font-weight: 600;
  color: #333333;
  font-size: 13px;
  margin-bottom: 2px;
}

.section-title {
  font-size: 13px;
  font-weight: 600;
  color: #333333;
}

.section-divider {
  height: 1px;
  background-color: #f0f0f0;
  margin: 4px 0;
}

.form-item {
  display: flex;
  align-items: flex-start;
}

.form-label {
  width: 140px;
  font-size: 13px;
  color: #555555;
  padding-top: 6px;
  flex-shrink: 0;
  text-align: right;
  margin-right: 16px;
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

.inline-icon {
  margin-left: 8px;
}

.form-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.radio-group {
  display: flex;
  align-items: center;
  gap: 24px;
  height: 32px;
}

.radio-label {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: #333333;
  cursor: pointer;
}

.radio-label input[type="radio"] {
  cursor: pointer;
}

.form-input {
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

.form-input:focus:not(.input-disabled) {
  border-color: #2468f2;
  box-shadow: 0 0 0 2px rgba(36, 104, 242, 0.1);
}

.input-disabled {
  background-color: #f5f5f5 !important;
  color: #999999 !important;
  cursor: not-allowed;
  border-color: #e4e7ed !important;
}

.segmented-control {
  display: inline-flex;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  overflow: hidden;
  height: 32px;
  width: fit-content;
}

.seg-btn {
  padding: 0 20px;
  height: 100%;
  border: none;
  background: #ffffff;
  color: #555555;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
  border-right: 1px solid #d9d9d9;
}

.seg-btn:last-child {
  border-right: none;
}

.seg-btn.active {
  background: #e8f0fe;
  color: #2468f2;
  font-weight: 500;
}

.checkbox-input-row {
  display: flex;
  align-items: center;
  gap: 10px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.checkbox-label input[type="checkbox"] {
  width: 15px;
  height: 15px;
  cursor: pointer;
}

.input-wrap {
  display: flex;
  align-items: center;
  flex: 1;
}

.input-number {
  max-width: 260px;
}

.danger-tip-text {
  font-size: 12px;
  color: #e65252;
  line-height: 1.5;
  margin-top: 2px;
}

.modal-footer {
  height: 56px;
  padding: 0 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  border-top: 1px solid #f0f0f0;
  background: #fafafa;
  flex-shrink: 0;
}

.btn {
  height: 32px;
  padding: 0 20px;
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
