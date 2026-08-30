<template>
  <div v-if="visible" class="modal-overlay" @click.self="close">
    <div class="modal-card">
      <div class="modal-header">
        <div class="title-wrap">
          <h3 class="modal-title">创建跨域复制</h3>
          <span class="info-circle" title="跨域复制功能说明">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"/>
              <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/>
              <line x1="12" y1="17" x2="12.01" y2="17"/>
            </svg>
          </span>
        </div>
        <button class="modal-close-btn" @click="close">×</button>
      </div>

      <div class="modal-body">
        <!-- 1. 全局状态 -->
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

        <!-- 2. 源桶参数组 -->
        <div class="section-title">源桶</div>

        <div class="form-item">
          <label class="form-label"><span class="required">*</span> 桶名称</label>
          <div class="form-content">
            <span class="text-value">{{ sourceBucketInfo.name }}</span>
          </div>
        </div>

        <div class="form-item">
          <label class="form-label"><span class="required">*</span> 区域</label>
          <div class="form-content">
            <span class="text-value">{{ sourceBucketInfo.region }}</span>
          </div>
        </div>

        <div class="form-item">
          <label class="form-label"><span class="required">*</span> 集群</label>
          <div class="form-content">
            <span class="text-value">{{ sourceBucketInfo.cluster }}</span>
          </div>
        </div>

        <div class="form-item">
          <label class="form-label"><span class="required">*</span> 复制对象</label>
          <div class="form-content">
            <button type="button" class="btn-tag active">所有对象</button>
          </div>
        </div>

        <!-- 3. 目标桶参数组 -->
        <div class="section-title">目标桶</div>

        <div class="form-item">
          <label class="form-label"><span class="required">*</span> 区域</label>
          <div class="form-content">
            <span class="text-value">{{ targetRegion }}</span>
          </div>
        </div>

        <div class="form-item">
          <label class="form-label"><span class="required">*</span> 集群</label>
          <div class="form-content">
            <select v-model="formData.targetCluster" class="form-select">
              <option value="" disabled>请选择集群</option>
              <option v-for="cluster in clusterOptions" :key="cluster" :value="cluster">
                {{ cluster }}
              </option>
            </select>
          </div>
        </div>

        <div class="form-item">
          <label class="form-label">
            <span class="required">*</span> 桶
            <span class="label-info-icon" title="选择目标桶">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
                <line x1="12" y1="16" x2="12" y2="12"/>
                <line x1="12" y1="8" x2="12.01" y2="8"/>
              </svg>
            </span>
          </label>
          <div class="form-content">
            <select v-model="formData.targetBucket" class="form-select">
              <option value="" disabled>请选择目标桶</option>
              <option v-for="bucket in filteredTargetBuckets" :key="bucket" :value="bucket">
                {{ bucket }}
              </option>
            </select>
          </div>
        </div>

        <!-- 4. 高级选项参数组 -->
        <div class="advanced-section">
          <div class="advanced-header" @click="isAdvancedOpen = !isAdvancedOpen">
            <span class="arrow-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline v-if="isAdvancedOpen" points="6 9 12 15 18 9"/>
                <polyline v-else points="9 18 15 12 9 6"/>
              </svg>
            </span>
            <span class="advanced-title">高级选项</span>
          </div>

          <div v-show="isAdvancedOpen" class="advanced-body">
            <!-- 是否开启双向复制 -->
            <div class="form-item">
              <label class="form-label"><span class="required">*</span> 是否开启双向复制</label>
              <div class="form-content">
                <div class="radio-group">
                  <label class="radio-label">
                    <input type="radio" value="是" v-model="formData.bidirectional" />
                    <span>是</span>
                  </label>
                  <label class="radio-label">
                    <input type="radio" value="否" v-model="formData.bidirectional" />
                    <span>否</span>
                  </label>
                </div>
                <div class="sub-tip-text">
                  <span class="tip-icon">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <circle cx="12" cy="12" r="10"/>
                      <line x1="12" y1="16" x2="12" y2="12"/>
                      <line x1="12" y1="8" x2="12.01" y2="8"/>
                    </svg>
                  </span>
                  <span>开启双向复制后会同步在目标桶创建一条和此条规则完全一样的规则（目标桶复制到源桶，即源桶目标桶互换）</span>
                </div>
              </div>
            </div>

            <!-- 同步历史对象 -->
            <div class="form-item">
              <label class="form-label">
                <span class="required">*</span> 同步历史对象
                <span class="label-info-icon" title="是否同步开启复制前已存在的历史数据">
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
                    :class="['seg-btn', { active: formData.historySync === '同步' }]"
                    @click="formData.historySync = '同步'"
                  >
                    同步
                  </button>
                  <button 
                    type="button"
                    :class="['seg-btn', { active: formData.historySync === '不同步' }]"
                    @click="formData.historySync = '不同步'"
                  >
                    不同步
                  </button>
                </div>
              </div>
            </div>

            <!-- 同步删除操作 -->
            <div class="form-item">
              <label class="form-label">
                <span class="required">*</span> 同步删除操作
                <span class="label-info-icon" title="源桶删除对象时是否同步删除目标桶对象">
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
                    :class="['seg-btn', { active: formData.deleteSync === '同步' }]"
                    @click="formData.deleteSync = '同步'"
                  >
                    同步
                  </button>
                  <button 
                    type="button"
                    :class="['seg-btn', { active: formData.deleteSync === '不同步' }]"
                    @click="formData.deleteSync = '不同步'"
                  >
                    不同步
                  </button>
                </div>
              </div>
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
import { reactive, computed, watch, ref } from 'vue'

const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  },
  sourceBucket: {
    type: String,
    default: 'zyy-kf-bucket-zyy3'
  }
})

const emit = defineEmits(['update:visible', 'submit'])

const isAdvancedOpen = ref(true)

// Bucket metadata map
const bucketMeta = {
  'zyy-kf-bucket-zyy3': { region: '上海', cluster: 'xhgs-stfk' },
  'jgh-kf-bucket-testpulsar2': { region: '上海', cluster: 'cluster-stdcsp' },
  'test-1': { region: '上海', cluster: 'cluster-stdcsp' },
  'testdcsp': { region: '合肥', cluster: 'cluster-stdcsp' },
  'xum3-test-20260603': { region: '合肥', cluster: 'cluster-stdcsp' },
  'yangxw-test-qu': { region: '合肥', cluster: 'cluster-stdcsp' },
  'yangxw-test': { region: '合肥', cluster: 'cluster-stdcsp' },
  'ystest-7-9': { region: '合肥', cluster: 'cluster-stdcsp' }
}

const allBuckets = [
  'testdcsp',
  'test-1',
  'xum3-test-20260603',
  'yangxw-test-qu',
  'yangxw-test',
  'ystest-7-9',
  'zyy-kf-bucket-zyy3'
]

const clusterOptions = ['cluster-stdcsp', 'xhgs-stfk']

// Current source bucket info
const sourceBucketInfo = computed(() => {
  const info = bucketMeta[props.sourceBucket] || { region: '上海', cluster: 'xhgs-stfk' }
  return {
    name: props.sourceBucket,
    region: info.region,
    cluster: info.cluster
  }
})

// Target Region: if Source is 上海 -> 合肥, if Source is 合肥 -> 上海
const targetRegion = computed(() => {
  return sourceBucketInfo.value.region === '上海' ? '合肥' : '上海'
})

// Filter target buckets based on target region and not equal to source bucket
const filteredTargetBuckets = computed(() => {
  return allBuckets.filter(b => b !== props.sourceBucket)
})

const formData = reactive({
  status: '启用',
  targetCluster: 'cluster-stdcsp',
  targetBucket: '',
  bidirectional: '是',
  historySync: '同步',
  deleteSync: '同步'
})

watch(() => props.visible, (newVal) => {
  if (newVal) {
    formData.status = '启用'
    formData.targetCluster = 'cluster-stdcsp'
    formData.targetBucket = ''
    formData.bidirectional = '是'
    formData.historySync = '同步'
    formData.deleteSync = '同步'
    isAdvancedOpen.value = true
  }
})

const close = () => {
  emit('update:visible', false)
}

const handleSubmit = () => {
  if (!formData.targetBucket) return

  emit('submit', {
    sourceBucket: props.sourceBucket,
    sourceRegion: sourceBucketInfo.value.region,
    sourceCluster: sourceBucketInfo.value.cluster,
    targetBucket: formData.targetBucket,
    targetRegion: targetRegion.value,
    targetCluster: formData.targetCluster,
    scope: '全部对象',
    status: formData.status,
    bidirectional: formData.bidirectional,
    historySync: formData.historySync,
    deleteSync: formData.deleteSync
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
  width: 620px;
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

.title-wrap {
  display: flex;
  align-items: center;
  gap: 6px;
}

.modal-title {
  font-size: 15px;
  font-weight: 600;
  color: #333333;
}

.info-circle {
  display: flex;
  align-items: center;
  color: #8c8c8c;
  cursor: pointer;
}

.info-circle svg {
  width: 14px;
  height: 14px;
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
  padding: 20px 28px 16px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.section-title {
  font-size: 14px;
  font-weight: 600;
  color: #333333;
  margin-top: 4px;
  margin-bottom: -4px;
}

.form-item {
  display: flex;
  align-items: flex-start;
}

.form-label {
  width: 135px;
  font-size: 13px;
  color: #555555;
  padding-top: 5px;
  flex-shrink: 0;
  text-align: right;
  margin-right: 20px;
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
  color: #8c8c8c;
  cursor: pointer;
}

.label-info-icon svg {
  width: 13px;
  height: 13px;
}

.form-content {
  flex: 1;
}

.text-value {
  display: inline-block;
  padding-top: 5px;
  font-size: 13px;
  color: #333333;
}

.form-select {
  width: 100%;
  height: 32px;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  padding: 0 10px;
  font-size: 13px;
  color: #333333;
  background-color: #ffffff;
  outline: none;
  transition: border-color 0.2s;
}

.form-select:focus {
  border-color: #2468f2;
}

.radio-group {
  display: flex;
  align-items: center;
  gap: 24px;
  min-height: 32px;
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

.btn-tag {
  height: 28px;
  padding: 0 16px;
  background-color: #2468f2;
  color: #ffffff;
  border: 1px solid #2468f2;
  border-radius: 3px;
  font-size: 13px;
  cursor: default;
}

/* Advanced section */
.advanced-section {
  margin-top: 4px;
}

.advanced-header {
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  user-select: none;
  padding: 6px 0;
  color: #333333;
  font-size: 14px;
  font-weight: 600;
}

.advanced-header .arrow-icon {
  display: flex;
  align-items: center;
  color: #666666;
}

.advanced-header .arrow-icon svg {
  width: 14px;
  height: 14px;
}

.advanced-body {
  margin-top: 14px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.sub-tip-text {
  margin-top: 6px;
  font-size: 12px;
  color: #8c8c8c;
  line-height: 1.5;
  display: flex;
  align-items: flex-start;
  gap: 4px;
}

.tip-icon {
  display: inline-flex;
  align-items: center;
  flex-shrink: 0;
  margin-top: 2px;
}

.tip-icon svg {
  width: 12px;
  height: 12px;
}

/* Segmented button group (同步 / 不同步) */
.segmented-control {
  display: inline-flex;
  border-radius: 3px;
  overflow: hidden;
  border: 1px solid #d9d9d9;
}

.seg-btn {
  height: 28px;
  padding: 0 16px;
  background: #ffffff;
  border: none;
  font-size: 13px;
  color: #555555;
  cursor: pointer;
  transition: all 0.15s;
}

.seg-btn:not(:last-child) {
  border-right: 1px solid #d9d9d9;
}

.seg-btn.active {
  background-color: #2468f2;
  color: #ffffff;
  font-weight: 500;
}

.modal-footer {
  padding: 12px 24px 18px;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  border-top: 1px solid #f0f0f0;
  flex-shrink: 0;
}

.btn {
  height: 32px;
  padding: 0 20px;
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
