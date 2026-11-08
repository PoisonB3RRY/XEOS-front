<template>
  <div class="ops-tab-bar">
    <!-- Back arrow -->
    <button class="nav-arrow-btn" @click="handleBack" title="返回上一级">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
        <polyline points="15 18 9 12 15 6" />
      </svg>
    </button>

    <!-- Tab items -->
    <div class="tabs-list">
      <div 
        v-for="tab in tabs" 
        :key="tab.id"
        :class="['tab-pill', { active: activeTabId === tab.id }]"
        @click="selectTab(tab.id)"
      >
        <span class="tab-label">{{ tab.name }}</span>
        <span 
          v-if="tab.closable" 
          class="close-icon" 
          @click.stop="closeTab(tab.id)"
        >×</span >
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  tabs: {
    type: Array,
    default: () => [{ id: 'home', name: '首页', closable: false }]
  },
  activeTabId: {
    type: String,
    default: 'home'
  }
})

const emit = defineEmits(['select-tab', 'close-tab', 'back'])

const selectTab = (id) => {
  emit('select-tab', id)
}

const closeTab = (id) => {
  emit('close-tab', id)
}

const handleBack = () => {
  emit('back')
}
</script>

<style scoped>
.ops-tab-bar {
  height: 38px;
  background-color: #ffffff;
  border-bottom: 1px solid #e8eaec;
  display: flex;
  align-items: center;
  padding: 0 14px;
  user-select: none;
}

.nav-arrow-btn {
  background: none;
  border: none;
  width: 22px;
  height: 22px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #8c8c8c;
  border-radius: 3px;
  margin-right: 10px;
  transition: all 0.15s;
}

.nav-arrow-btn:hover {
  background-color: #f0f2f5;
  color: #1890ff;
}

.nav-arrow-btn svg {
  width: 14px;
  height: 14px;
}

.tabs-list {
  display: flex;
  align-items: center;
  gap: 8px;
}

.tab-pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  height: 26px;
  padding: 0 10px;
  font-size: 12px;
  color: #595959;
  background-color: #fafafa;
  border: 1px solid #d9d9d9;
  border-radius: 3px;
  cursor: pointer;
  transition: all 0.2s;
}

.tab-pill:hover {
  color: #1890ff;
  border-color: #91d5ff;
}

.tab-pill.active {
  color: #1890ff;
  background-color: #e6f7ff;
  border-color: #91d5ff;
}

.tab-label {
  line-height: 1;
}

.close-icon {
  font-size: 14px;
  line-height: 1;
  color: #8c8c8c;
  cursor: pointer;
  border-radius: 50%;
  width: 12px;
  height: 12px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.close-icon:hover {
  color: #f5222d;
  background: rgba(0, 0, 0, 0.06);
}
</style>
