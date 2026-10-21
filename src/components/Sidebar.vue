<template>
  <aside :class="['sidebar', { collapsed: isCollapsed }]">
    <div class="menu-container">
      <div 
        v-for="group in activeMenuGroups" 
        :key="group.id" 
        class="menu-group"
      >
        <!-- Group Header (Parent Item) -->
        <div 
          :class="['group-title', { 
            active: isGroupActive(group),
            expanded: expandedGroups[group.id]
          }]"
          @click="toggleGroup(group.id)"
        >
          <div class="title-left">
            <span class="menu-icon">
              <!-- Render specific icon based on group.icon -->
              <svg v-if="group.icon === 'mq'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
                <line x1="8" y1="10" x2="16" y2="10"/>
                <line x1="8" y1="6" x2="14" y2="6"/>
              </svg>
              <svg v-else-if="group.icon === 'cache'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>
              </svg>
              <svg v-else-if="group.icon === 'container'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="2" y="7" width="20" height="14" rx="2" ry="2"/>
                <path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>
              </svg>
              <svg v-else-if="group.icon === 'network'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="2" y="2" width="6" height="6" rx="1"/>
                <rect x="16" y="2" width="6" height="6" rx="1"/>
                <rect x="9" y="16" width="6" height="6" rx="1"/>
                <path d="M5 8v3a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8"/>
                <path d="M12 13v3"/>
              </svg>
              <svg v-else-if="group.icon === 'compute'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="4" y="4" width="16" height="16" rx="2"/>
                <rect x="9" y="9" width="6" height="6"/>
                <line x1="9" y1="1" x2="9" y2="4"/>
                <line x1="15" y1="1" x2="15" y2="4"/>
                <line x1="9" y1="20" x2="9" y2="23"/>
                <line x1="15" y1="20" x2="15" y2="23"/>
                <line x1="20" y1="9" x2="23" y2="9"/>
                <line x1="20" y1="14" x2="23" y2="14"/>
                <line x1="1" y1="9" x2="4" y2="9"/>
                <line x1="1" y1="14" x2="4" y2="14"/>
              </svg>
              <svg v-else-if="group.icon === 'storage'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <ellipse cx="12" cy="5" rx="9" ry="3"/>
                <path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/>
                <path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/>
              </svg>
              <svg v-else-if="group.icon === 'analytics'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="20" x2="18" y2="10"/>
                <line x1="12" y1="20" x2="12" y2="4"/>
                <line x1="6" y1="20" x2="6" y2="14"/>
              </svg>
              <svg v-else-if="group.icon === 'trash'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="3 6 5 6 21 6"/>
                <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
                <line x1="10" y1="11" x2="10" y2="17"/>
                <line x1="14" y1="11" x2="14" y2="17"/>
              </svg>
              <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
              </svg>
            </span>
            <span class="group-name" v-show="!isCollapsed">{{ group.name }}</span>
          </div>

          <span class="arrow-icon" v-show="!isCollapsed">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline v-if="expandedGroups[group.id]" points="6 9 12 15 18 9"/>
              <polyline v-else points="9 18 15 12 9 6"/>
            </svg>
          </span>
        </div>

        <!-- Submenu Children -->
        <div 
          v-if="group.children && expandedGroups[group.id] && !isCollapsed" 
          class="submenu"
        >
          <div 
            v-for="sub in group.children" 
            :key="sub.id"
            :class="['sub-item', { active: activeSubItem === sub.id }]"
            @click="selectSubItem(sub.id)"
          >
            {{ sub.name }}
          </div>
        </div>
      </div>
    </div>

    <!-- Bottom Collapse Toggle Button -->
    <div class="sidebar-footer" @click="isCollapsed = !isCollapsed">
      <div class="collapse-btn" title="折叠/展开侧边栏">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="3" y1="12" x2="21" y2="12"/>
          <line x1="3" y1="6" x2="21" y2="6"/>
          <line x1="3" y1="18" x2="21" y2="18"/>
        </svg>
      </div>
    </div>
  </aside>
</template>

<script setup>
import { ref, reactive, computed, watch } from 'vue'

const props = defineProps({
  currentProduct: {
    type: String,
    default: 'xuanwu'
  },
  modelValue: {
    type: String,
    default: 'obs-bucket'
  }
})

const emit = defineEmits(['update:modelValue', 'select-menu'])

const isCollapsed = ref(false)
const activeSubItem = ref(props.modelValue || 'obs-bucket')

watch(() => props.modelValue, (newVal) => {
  if (newVal) {
    activeSubItem.value = newVal
  }
})

const expandedGroups = reactive({
  storage: true,
  compute: true,
  mq: false,
  cache: false,
  analytics: false,
  trash: false,
  network: false,
  container1: false,
  container2: false,
  database: false,
  middleware: false,
  bigdata: false,
  security: false
})

// Menu for Xuanwu Cloud (玄武云产品) matching photo/玄武云-对象存储桶 列表页.jpg
const xuanwuMenuGroups = [
  { id: 'mq', name: '消息队列服务', icon: 'mq' },
  { id: 'cache', name: '缓存服务', icon: 'cache' },
  { id: 'analytics', name: '数据计算与分析服务', icon: 'analytics' },
  { 
    id: 'compute', 
    name: '计算服务', 
    icon: 'compute',
    children: [
      { id: 'vm', name: '云虚拟机' }
    ]
  },
  { 
    id: 'storage', 
    name: '存储服务', 
    icon: 'storage',
    children: [
      { id: 'obs-bucket', name: '对象存储桶' },
      { id: 'obs-user', name: '对象存储用户' }
    ]
  },
  { id: 'trash', name: '回收站', icon: 'trash' },
  { id: 'network', name: '网络服务', icon: 'network' }
]

// Menu for Tianji Cloud (天玑云产品)
const tianjiMenuGroups = [
  { id: 'container1', name: '容器服务', icon: 'container' },
  { 
    id: 'compute', 
    name: '计算服务', 
    icon: 'compute',
    children: [
      { id: 'vm', name: '云虚拟机' }
    ]
  },
  { 
    id: 'storage', 
    name: '存储服务', 
    icon: 'storage',
    children: [
      { id: 'evs', name: '信创云硬盘(EVS)' },
      { id: 'sfs', name: '信创文件存储(SFS)' },
      { id: 'snapshot', name: '信创快照' },
      { id: 'tianji-obs-bucket', name: '信创对象存储-桶(OBS)' },
      { id: 'tianji-obs-user', name: '信创对象存储-用户' }
    ]
  },
  { id: 'network', name: '网络服务', icon: 'network' },
  { id: 'database', name: '数据库服务', icon: 'database' },
  { id: 'cache', name: '缓存服务', icon: 'cache' },
  { id: 'mq', name: '消息队列服务', icon: 'mq' },
  { id: 'analytics', name: '数据计算与分析服务', icon: 'analytics' },
  { id: 'security', name: '安全服务', icon: 'security' },
  { id: 'trash', name: '回收站', icon: 'trash' }
]

const activeMenuGroups = computed(() => {
  return props.currentProduct === 'tianji' ? tianjiMenuGroups : xuanwuMenuGroups
})

const isGroupActive = (group) => {
  if (group.children && group.children.some(c => c.id === activeSubItem.value)) {
    return true
  }
  return false
}

const toggleGroup = (groupId) => {
  expandedGroups[groupId] = !expandedGroups[groupId]
}

const selectSubItem = (subId) => {
  activeSubItem.value = subId
  emit('update:modelValue', subId)
  emit('select-menu', subId)
}
</script>

<style scoped>
.sidebar {
  width: 200px;
  background-color: #f7f9fb;
  border-right: 1px solid #e8ecef;
  display: flex;
  flex-direction: column;
  height: calc(100vh - 50px);
  transition: width 0.25s ease;
  user-select: none;
  flex-shrink: 0;
}

.sidebar.collapsed {
  width: 52px;
}

.menu-container {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  padding-top: 6px;
}

.menu-group {
  margin-bottom: 2px;
}

.group-title {
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 14px 0 16px;
  color: #4a5568;
  font-size: 13px;
  cursor: pointer;
  transition: background-color 0.15s, color 0.15s;
}

.group-title:hover {
  background-color: #edf2f7;
  color: #1a202c;
}

.title-left {
  display: flex;
  align-items: center;
  gap: 10px;
  overflow: hidden;
  white-space: nowrap;
}

.menu-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  color: #718096;
  flex-shrink: 0;
}

.menu-icon svg {
  width: 16px;
  height: 16px;
}

.group-name {
  font-weight: 500;
  overflow: hidden;
  text-overflow: ellipsis;
}

.arrow-icon {
  display: flex;
  align-items: center;
  color: #a0aec0;
}

.arrow-icon svg {
  width: 13px;
  height: 13px;
}

.submenu {
  background-color: #f0f4f8;
  padding: 2px 0;
}

.sub-item {
  height: 36px;
  display: flex;
  align-items: center;
  padding-left: 42px;
  font-size: 12.5px;
  color: #4a5568;
  cursor: pointer;
  white-space: nowrap;
  position: relative;
  transition: all 0.15s;
}

.sub-item:hover {
  color: #2468f2;
  background-color: #e2e8f0;
}

.sub-item.active {
  color: #2468f2;
  background-color: #e8f1ff;
  font-weight: 600;
}

.sub-item.active::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 3px;
  background-color: #2468f2;
}

.sidebar-footer {
  height: 40px;
  border-top: 1px solid #e8ecef;
  display: flex;
  align-items: center;
  padding: 0 16px;
  background-color: #f7f9fb;
}

.collapse-btn {
  cursor: pointer;
  color: #718096;
  display: flex;
  align-items: center;
}

.collapse-btn:hover {
  color: #2468f2;
}

.collapse-btn svg {
  width: 16px;
  height: 16px;
}
</style>
