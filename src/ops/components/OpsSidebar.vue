<template>
  <aside :class="['ops-sidebar', { collapsed: isCollapsed }]">
    <div class="menu-container">
      <div 
        v-for="item in menuList" 
        :key="item.id" 
        class="menu-block"
      >
        <!-- Single item or Group Header -->
        <div 
          :class="[
            'menu-row', 
            { 
              active: activeMenuId === item.id && !item.children,
              expanded: item.children && expandedGroups[item.id],
              hasChildren: !!item.children
            }
          ]"
          @click="handleMenuClick(item)"
        >
          <div class="row-left">
            <span class="menu-icon">
              <!-- 网关管理 -->
              <svg v-if="item.icon === 'gateway'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>
                <polyline points="9 22 9 12 15 12 15 22"/>
              </svg>
              <!-- 虚拟机管理 -->
              <svg v-else-if="item.icon === 'vm'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="2" y="3" width="20" height="14" rx="2" ry="2"/>
                <line x1="8" y1="21" x2="16" y2="21"/>
                <line x1="12" y1="17" x2="12" y2="21"/>
              </svg>
              <!-- 裸金属服务器管理 -->
              <svg v-else-if="item.icon === 'bare-metal'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="2" y="2" width="20" height="8" rx="2" ry="2"/>
                <rect x="2" y="14" width="20" height="8" rx="2" ry="2"/>
                <line x1="6" y1="6" x2="6.01" y2="6"/>
                <line x1="6" y1="18" x2="6.01" y2="18"/>
              </svg>
              <!-- 工具平台 -->
              <svg v-else-if="item.icon === 'tools'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>
              </svg>
              <!-- 存储服务 -->
              <svg v-else-if="item.icon === 'storage'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <ellipse cx="12" cy="5" rx="9" ry="3"/>
                <path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/>
                <path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/>
              </svg>
              <!-- 快照管理 -->
              <svg v-else-if="item.icon === 'snapshot'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="18" cy="5" r="3"/>
                <circle cx="6" cy="12" r="3"/>
                <circle cx="18" cy="19" r="3"/>
                <line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/>
                <line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/>
              </svg>
              <!-- 评价管理 -->
              <svg v-else-if="item.icon === 'evaluate'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                <polyline points="14 2 14 8 20 8"/>
                <line x1="16" y1="13" x2="8" y2="13"/>
                <line x1="16" y1="17" x2="8" y2="17"/>
                <polyline points="10 9 9 9 8 9"/>
              </svg>
              <!-- 回收站 -->
              <svg v-else-if="item.icon === 'recycle'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="3 6 5 6 21 6"/>
                <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
              </svg>
              <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
              </svg>
            </span>
            <span class="item-text" v-show="!isCollapsed">{{ item.name }}</span>
          </div>

          <!-- Chevron Right / Down -->
          <span class="chevron-icon" v-show="!isCollapsed">
            <svg v-if="item.children" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline v-if="expandedGroups[item.id]" points="6 9 12 15 18 9"/>
              <polyline v-else points="9 18 15 12 9 6"/>
            </svg>
            <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="9 18 15 12 9 6"/>
            </svg>
          </span>
        </div>

        <!-- Submenu Children (Under 存储服务) -->
        <div 
          v-if="item.children && expandedGroups[item.id] && !isCollapsed" 
          class="sub-container"
        >
          <div 
            v-for="sub in item.children" 
            :key="sub.id"
            :class="['sub-row', { active: activeMenuId === sub.id }]"
            @click="handleSubClick(sub)"
          >
            <span class="sub-icon">
              <!-- 信创快照 -->
              <svg v-if="sub.icon === 'lightbulb'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M9 18h6"/>
                <path d="M10 22h4"/>
                <path d="M15.09 14c.18-.98.65-1.74 1.41-2.5A4.65 4.65 0 0 0 18 8 6 6 0 0 0 6 8c0 1 .23 2.23 1.5 3.5A4.61 4.61 0 0 1 8.91 14"/>
              </svg>
              <!-- 桶管理 -->
              <svg v-else-if="sub.icon === 'bucket'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>
              </svg>
              <!-- 信创云硬盘 -->
              <svg v-else-if="sub.icon === 'disk'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
                <polyline points="12 6 12 12 16 14"/>
              </svg>
              <!-- 信创对象存储 (active in screenshot) -->
              <svg v-else-if="sub.icon === 'diamond'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M6 3h12l4 6-10 13L2 9z"/>
                <path d="M2 9h20"/>
                <path d="M10 22l-4-13 6-6 6 6-4 13"/>
              </svg>
              <!-- OBS用户组管理 -->
              <svg v-else-if="sub.icon === 'users'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
                <circle cx="9" cy="7" r="4"/>
                <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
                <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
              </svg>
              <!-- default bullet -->
              <span v-else class="bullet-dot"></span>
            </span>
            <span class="sub-text">{{ sub.name }}</span>
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
import { ref, reactive } from 'vue'

const props = defineProps({
  currentMenu: {
    type: String,
    default: 'home'
  }
})

const emit = defineEmits(['select-menu'])

const isCollapsed = ref(false)
const activeMenuId = ref(props.currentMenu || 'home')

const expandedGroups = reactive({
  storage: true
})

const menuList = [
  { id: 'gateway', name: '网关管理', icon: 'gateway' },
  { id: 'vm', name: '虚拟机管理', icon: 'vm' },
  { id: 'bare-metal', name: '裸金属服务器管理', icon: 'bare-metal' },
  { id: 'tools', name: '工具平台', icon: 'tools' },
  { 
    id: 'storage', 
    name: '存储服务', 
    icon: 'storage',
    children: [
      { id: 'xc-snapshot', name: '信创快照', icon: 'lightbulb' },
      { id: 'bucket-mgr', name: '桶管理', icon: 'bucket' },
      { id: 'obs-account', name: '对象存储账户', icon: 'dot' },
      { id: 'obs-tenant', name: 'OBS租户', icon: 'dot' },
      { id: 'obs-user-group', name: 'OBS用户组管理', icon: 'users' },
      { id: 'xc-disk', name: '信创云硬盘', icon: 'disk' },
      { id: 'xc-obs', name: '信创对象存储', icon: 'diamond' },
      { id: 'obs-user', name: '对象存储用户', icon: 'dot' }
    ]
  },
  { id: 'snapshot-mgr', name: '快照管理', icon: 'snapshot' },
  { id: 'evaluation', name: '评价管理', icon: 'evaluate' },
  { id: 'recycle', name: '回收站', icon: 'recycle' }
]

const handleMenuClick = (item) => {
  if (item.children) {
    expandedGroups[item.id] = !expandedGroups[item.id]
  } else {
    activeMenuId.value = item.id
    emit('select-menu', item)
  }
}

const handleSubClick = (sub) => {
  activeMenuId.value = sub.id
  emit('select-menu', sub)
}
</script>

<style scoped>
.ops-sidebar {
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

.ops-sidebar.collapsed {
  width: 52px;
}

.menu-container {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  padding-top: 6px;
}

.menu-block {
  margin-bottom: 1px;
}

.menu-row {
  height: 38px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 14px 0 16px;
  color: #595959;
  font-size: 13px;
  cursor: pointer;
  transition: background-color 0.15s, color 0.15s;
}

.menu-row:hover {
  background-color: #f0f3f6;
  color: #1890ff;
}

.menu-row.active {
  background-color: #e6f7ff;
  color: #1890ff;
  font-weight: 500;
}

.row-left {
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
  color: #8c8c8c;
  flex-shrink: 0;
}

.menu-icon svg {
  width: 15px;
  height: 15px;
}

.menu-row:hover .menu-icon,
.menu-row.active .menu-icon {
  color: #1890ff;
}

.item-text {
  overflow: hidden;
  text-overflow: ellipsis;
}

.chevron-icon {
  display: flex;
  align-items: center;
  color: #bfbfbf;
}

.chevron-icon svg {
  width: 12px;
  height: 12px;
}

.sub-container {
  background-color: #f2f5f8;
  padding: 2px 0;
}

.sub-row {
  height: 36px;
  display: flex;
  align-items: center;
  padding-left: 36px;
  font-size: 12.5px;
  color: #595959;
  cursor: pointer;
  white-space: nowrap;
  position: relative;
  transition: all 0.15s;
  gap: 8px;
}

.sub-row:hover {
  color: #1890ff;
  background-color: #e6f1fc;
}

.sub-row.active {
  color: #1890ff;
  background-color: #e6f1fc;
  font-weight: 500;
}

.sub-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 16px;
  color: #8c8c8c;
}

.sub-icon svg {
  width: 14px;
  height: 14px;
}

.sub-row.active .sub-icon {
  color: #1890ff;
}

.bullet-dot {
  width: 4px;
  height: 4px;
  border-radius: 50%;
  background-color: #bfbfbf;
  margin-left: 4px;
}

.sub-row.active .bullet-dot {
  background-color: #1890ff;
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
  color: #8c8c8c;
  display: flex;
  align-items: center;
}

.collapse-btn:hover {
  color: #1890ff;
}

.collapse-btn svg {
  width: 16px;
  height: 16px;
}
</style>
