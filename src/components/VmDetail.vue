<template>
  <div class="vm-detail-card">
    <!-- Top Header Bar -->
    <div class="detail-top-bar">
      <div class="header-left">
        <span class="status-tag status-normal">正常</span>
        <span class="instance-name">{{ instanceInfo.name }}</span>
        <button class="btn-refresh-header" @click="handleRefresh">
          <svg class="refresh-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="23 4 23 10 17 10"/>
            <polyline points="1 20 1 14 7 14"/>
            <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/>
          </svg>
          <span>刷新</span>
        </button>
      </div>

      <div class="header-right">
        <button class="btn-back" @click="handleBack">返回</button>
      </div>
    </div>

    <!-- Secondary Tabs Bar -->
    <div class="detail-tabs-bar">
      <div 
        v-for="tab in subTabs" 
        :key="tab.id"
        :class="['tab-item', { active: currentTab === tab.id }]"
        @click="currentTab = tab.id"
      >
        {{ tab.name }}
      </div>
    </div>

    <!-- Tab Panels -->
    <div class="detail-panel-body">
      <!-- 基本信息 -->
      <VmBasicInfo 
        v-if="currentTab === 'info'" 
        :vm-info="instanceInfo" 
      />

      <!-- 硬盘管理 (磁盘列表页，带新增回收站按钮) -->
      <VmDiskManagement 
        v-else-if="currentTab === 'disk'" 
        :instance-name="instanceInfo.name" 
      />

      <!-- 快照管理 -->
      <VmSnapshotManagement 
        v-else-if="currentTab === 'snapshot'" 
        :instance-name="instanceInfo.name" 
      />
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import VmBasicInfo from './VmBasicInfo.vue'
import VmDiskManagement from './VmDiskManagement.vue'
import VmSnapshotManagement from './VmSnapshotManagement.vue'

const props = defineProps({
  instanceData: {
    type: Object,
    default: () => ({
      name: 'testlu01',
      id: '241c6956-2c3e-4461-b55d-afc6e4eafeb2',
      org: '金融云门户系统',
      owner: '12064927',
      region: '上海',
      zone: '上海裸金属一区（赵巷）',
      os: 'Kylin Linux Advanced Server V10 (64-bit)',
      arch: 'C86',
      cpuCores: '4',
      memory: '8GB',
      createTime: '2026-09-14 17:28:09',
      expireTime: '2026-12-13',
      ip: '190.23.55.19'
    })
  },
  defaultTab: {
    type: String,
    default: 'info'
  }
})

const emit = defineEmits(['back'])

const instanceInfo = ref({ ...props.instanceData })
const currentTab = ref(props.defaultTab || 'info')

watch(() => props.defaultTab, (val) => {
  if (val) currentTab.value = val
})

watch(() => props.instanceData, (val) => {
  if (val) instanceInfo.value = { ...val }
}, { deep: true })

const subTabs = [
  { id: 'info', name: '基本信息' },
  { id: 'disk', name: '硬盘管理' },
  { id: 'snapshot', name: '快照管理' }
]

const handleRefresh = () => {
  // Simple refresh feedback
  const original = instanceInfo.value.name
  instanceInfo.value.name = '刷新中...'
  setTimeout(() => {
    instanceInfo.value.name = original
  }, 300)
}

const handleBack = () => {
  emit('back')
}
</script>

<style scoped>
.vm-detail-card {
  background-color: #ffffff;
  border-radius: 4px;
  min-height: calc(100vh - 105px);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
}

/* Header */
.detail-top-bar {
  padding: 14px 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid #f0f2f5;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.status-tag {
  font-size: 12px;
  padding: 2px 8px;
  border-radius: 3px;
  font-weight: 500;
  display: inline-flex;
  align-items: center;
}

.status-normal {
  background-color: #f0f9eb;
  border: 1px solid #e1f3d8;
  color: #67c23a;
}

.instance-name {
  font-size: 15px;
  font-weight: 600;
  color: #1f2d3d;
}

.btn-refresh-header {
  height: 28px;
  padding: 0 10px;
  display: flex;
  align-items: center;
  gap: 5px;
  background-color: #ffffff;
  border: 1px solid #dcdfe6;
  border-radius: 3px;
  font-size: 12px;
  color: #606266;
  cursor: pointer;
  transition: all 0.15s;
}

.btn-refresh-header:hover {
  color: #2468f2;
  border-color: #2468f2;
}

.refresh-icon {
  width: 13px;
  height: 13px;
}

.header-right {
  display: flex;
  align-items: center;
}

.btn-back {
  height: 28px;
  padding: 0 16px;
  background-color: #ffffff;
  border: 1px solid #dcdfe6;
  border-radius: 3px;
  font-size: 13px;
  color: #606266;
  cursor: pointer;
  transition: all 0.15s;
}

.btn-back:hover {
  color: #2468f2;
  border-color: #2468f2;
}

/* Tabs */
.detail-tabs-bar {
  display: flex;
  align-items: center;
  padding: 0 20px;
  border-bottom: 1px solid #e8ecef;
  gap: 28px;
  background-color: #ffffff;
}

.tab-item {
  padding: 10px 2px;
  font-size: 13.5px;
  color: #5c6b77;
  cursor: pointer;
  position: relative;
  transition: all 0.15s;
  font-weight: 400;
}

.tab-item:hover {
  color: #2468f2;
}

.tab-item.active {
  color: #2468f2;
  font-weight: 500;
}

.tab-item.active::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 0;
  right: 0;
  height: 2.5px;
  background-color: #2468f2;
  border-radius: 2px 2px 0 0;
}

.detail-panel-body {
  flex: 1;
  background-color: #ffffff;
}
</style>
