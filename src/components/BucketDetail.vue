<template>
  <div class="bucket-detail-card">
    <!-- Card Header with Title and Back Button -->
    <div class="card-top-bar">
      <h2 class="bucket-title">{{ bucketName }}</h2>
      <button class="btn-back" @click="handleBack">返回</button>
    </div>

    <!-- Secondary Tab Bar -->
    <div class="sub-tabs-bar">
      <div 
        v-for="tab in subTabs" 
        :key="tab.id"
        :class="['sub-tab-item', { active: currentSubTab === tab.id }]"
        @click="currentSubTab = tab.id"
      >
        {{ tab.name }}
      </div>
    </div>

    <!-- Tab Content -->
    <div class="tab-panel-content">
      <!-- 跨域复制管理 (CCR) - 目标复刻页 -->
      <CrossRegionReplication v-if="currentSubTab === 'ccr'" />

      <!-- 授权管理 -->
      <AuthManagement v-else-if="currentSubTab === 'auth'" />

      <!-- 基本信息 -->
      <BasicInfo v-else-if="currentSubTab === 'info'" />

      <!-- Other Tabs Placeholder -->
      <div v-else class="placeholder-tab">
        <div class="placeholder-icon">📂</div>
        <p>{{ getTabName(currentSubTab) }} 模块已就绪</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import CrossRegionReplication from './CrossRegionReplication.vue'
import AuthManagement from './AuthManagement.vue'
import BasicInfo from './BasicInfo.vue'

const props = defineProps({
  bucketName: {
    type: String,
    default: 'jgh-kf-bucket-testpulsar2'
  },
  defaultTab: {
    type: String,
    default: 'ccr'
  }
})

const emit = defineEmits(['back'])

const currentSubTab = ref(props.defaultTab || 'ccr')

watch(() => props.defaultTab, (val) => {
  if (val) currentSubTab.value = val
})

const subTabs = [
  { id: 'info', name: '基本信息' },
  { id: 'auth', name: '授权管理' },
  { id: 'lifecycle', name: '生命周期管理' },
  { id: 'ccr', name: '跨域复制管理' },
  { id: 'migration', name: '迁移管理' },
  { id: 'cors', name: 'CORS管理' }
]

const getTabName = (tabId) => {
  const t = subTabs.find(item => item.id === tabId)
  return t ? t.name : ''
}

const handleBack = () => {
  emit('back')
}
</script>

<style scoped>
.bucket-detail-card {
  background-color: #ffffff;
  border-radius: 4px;
  min-height: calc(100vh - 110px);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
}

.card-top-bar {
  padding: 16px 20px 12px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.bucket-title {
  font-size: 16px;
  font-weight: 500;
  color: #1f2d3d;
  letter-spacing: 0.2px;
}

.btn-back {
  background-color: #ffffff;
  border: 1px solid #dcdfe6;
  color: #606266;
  padding: 4px 16px;
  font-size: 13px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-back:hover {
  border-color: #2468f2;
  color: #2468f2;
}

/* Secondary Tab Bar */
.sub-tabs-bar {
  display: flex;
  align-items: center;
  padding: 0 20px;
  border-bottom: 1px solid #e8ecef;
  gap: 28px;
}

.sub-tab-item {
  padding: 10px 2px;
  font-size: 14px;
  color: #4a5568;
  cursor: pointer;
  position: relative;
  transition: all 0.2s;
}

.sub-tab-item:hover {
  color: #2468f2;
}

.sub-tab-item.active {
  color: #2468f2;
  font-weight: 500;
}

.sub-tab-item.active::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 0;
  right: 0;
  height: 2.5px;
  background-color: #2468f2;
  border-radius: 2px 2px 0 0;
}

.tab-panel-content {
  flex: 1;
}

.placeholder-tab {
  padding: 80px 20px;
  text-align: center;
  color: #909399;
}

.placeholder-icon {
  font-size: 40px;
  margin-bottom: 12px;
}
</style>
