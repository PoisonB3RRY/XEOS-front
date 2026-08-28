<template>
  <div class="tab-bar">
    <button class="nav-arrow-btn" @click="handleBack" title="返回上一层">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
        <polyline points="15 18 9 12 15 6" />
      </svg>
    </button>

    <div class="tabs-list">
      <div 
        v-for="tab in tabs" 
        :key="tab.id"
        :class="['tab-item', { active: currentActive === tab.id }]"
        @click="selectTab(tab.id)"
      >
        <span class="tab-text">{{ tab.name }}</span>
        <button 
          v-if="tab.closable" 
          class="close-btn" 
          @click.stop="closeTab(tab.id)"
          title="关闭标签"
        >×</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  tabs: {
    type: Array,
    default: () => [
      { id: 'home', name: '首页', closable: false },
      { id: 'obs-bucket', name: '对象存储桶', closable: true }
    ]
  },
  activeTab: {
    type: String,
    default: 'obs-bucket'
  }
})

const emit = defineEmits(['update:activeTab', 'tab-click', 'tab-close', 'back'])

const currentActive = ref(props.activeTab)

watch(() => props.activeTab, (val) => {
  if (val) currentActive.value = val
})

const selectTab = (tabId) => {
  currentActive.value = tabId
  emit('update:activeTab', tabId)
  emit('tab-click', tabId)
}

const closeTab = (tabId) => {
  emit('tab-close', tabId)
}

const handleBack = () => {
  emit('back')
}
</script>

<style scoped>
.tab-bar {
  height: 36px;
  background-color: #ffffff;
  border-bottom: 1px solid #e5e9f2;
  display: flex;
  align-items: center;
  padding: 0 12px;
  user-select: none;
}

.nav-arrow-btn {
  background: none;
  border: none;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #666666;
  border-radius: 3px;
  margin-right: 8px;
}

.nav-arrow-btn:hover {
  background-color: #f0f2f5;
  color: #2468f2;
}

.nav-arrow-btn svg {
  width: 14px;
  height: 14px;
}

.tabs-list {
  display: flex;
  align-items: center;
  gap: 4px;
  height: 100%;
}

.tab-item {
  display: flex;
  align-items: center;
  gap: 6px;
  height: 36px;
  padding: 0 14px;
  font-size: 13px;
  color: #606266;
  cursor: pointer;
  position: relative;
  transition: all 0.2s;
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
  bottom: 0;
  left: 0;
  right: 0;
  height: 2px;
  background-color: #2468f2;
}

.close-btn {
  background: none;
  border: none;
  cursor: pointer;
  color: #909399;
  font-size: 14px;
  line-height: 1;
  padding: 2px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 14px;
  height: 14px;
}

.close-btn:hover {
  color: #f56c6c;
  background-color: #f2f3f5;
}
</style>
