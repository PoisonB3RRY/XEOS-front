<template>
  <div class="tab-bar">
    <button class="nav-arrow-btn" title="返回上一层">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
        <polyline points="15 18 9 12 15 6" />
      </svg>
    </button>

    <div class="tabs-list">
      <div 
        :class="['tab-item', { active: activeTab === 'home' }]"
        @click="activeTab = 'home'"
      >
        <span class="tab-text">首页</span>
      </div>

      <div 
        :class="['tab-item', { active: activeTab === 'obs' }]"
        @click="activeTab = 'obs'"
      >
        <span class="tab-text">信创对象存储-桶(OBS)</span>
        <button class="close-btn" title="关闭标签">×</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const activeTab = ref('obs')
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
