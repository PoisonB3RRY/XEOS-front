<template>
  <div class="ops-layout">
    <!-- Top Header -->
    <OpsHeader 
      @select-nav="handleNavSelect"
      @go-home="handleGoHome"
    />

    <!-- Main Container -->
    <div class="main-body">
      <!-- Left Sidebar -->
      <OpsSidebar 
        :current-menu="currentMenu"
        @select-menu="handleMenuSelect"
      />

      <!-- Content Area -->
      <div class="content-wrapper">
        <!-- Tab Bar -->
        <OpsTabBar 
          :tabs="tabs"
          :active-tab-id="activeTabId"
          @select-tab="handleTabSelect"
          @close-tab="handleTabClose"
          @back="handleBack"
        />

        <!-- Page View Container -->
        <main class="page-viewport">
          <!-- Ops Home (Screenshot Replica) -->
          <OpsHome v-if="activeTabId === 'home'" />

          <!-- 信创对象存储 (Reuse TianjiObsList component) -->
          <div v-else-if="activeTabId === 'xc-obs'" class="sub-view-wrapper">
            <TianjiObsList 
              :buckets="tianjiBucketList"
              @create="handleNotice('功能在当前运维权限下已锁定或请切换对应功能')"
              @delete="handleNotice('运维管理员操作：删除请求已拦截')"
              @expand="handleNotice('运维管理员操作：扩容操作')"
              @select-bucket="handleNotice"
              @notify="handleNotice"
            />
          </div>

          <!-- 信创云硬盘 (Reuse EvsList component) -->
          <div v-else-if="activeTabId === 'xc-disk'" class="sub-view-wrapper">
            <EvsList 
              :instances="evsList"
              @create="handleNotice"
              @delete="handleNotice"
              @expand="handleNotice"
              @notify="handleNotice"
            />
          </div>

          <!-- OBS用户组管理 -->
          <div v-else-if="activeTabId === 'obs-user-group'" class="sub-view-wrapper">
            <ObsUserGroupManage />
          </div>

          <!-- 桶管理 (Reuse BucketList component) -->
          <div v-else-if="activeTabId === 'bucket-mgr'" class="sub-view-wrapper">
            <BucketList 
              @select-bucket="handleNotice"
              @open-auth="handleNotice"
            />
          </div>

          <!-- 虚拟机管理 (Reuse VmList component) -->
          <div v-else-if="activeTabId === 'vm'" class="sub-view-wrapper">
            <VmList 
              @select-vm="handleNotice"
              @open-snapshot="handleNotice"
            />
          </div>

          <!-- Placeholder for other ops menus -->
          <div v-else class="placeholder-view">
            <div class="placeholder-box">
              <div class="icon">🖥️</div>
              <h2>{{ currentMenuTitle }}</h2>
              <p>浦发银行云管理系统（运维门户）- 业务功能管理区</p>
              <button class="back-home-btn" @click="handleGoHome">返回运维门户首页</button>
            </div>
          </div>
        </main>
      </div>
    </div>

    <!-- Toast Notification -->
    <transition name="toast-fade">
      <div v-if="toastMessage" class="ops-toast">
        {{ toastMessage }}
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import OpsHeader from './components/OpsHeader.vue'
import OpsSidebar from './components/OpsSidebar.vue'
import OpsTabBar from './components/OpsTabBar.vue'
import OpsHome from './components/OpsHome.vue'
import ObsUserGroupManage from './components/ObsUserGroupManage.vue'

// Import existing modules for functional preview
import TianjiObsList from '../components/TianjiObsList.vue'
import EvsList from '../components/EvsList.vue'
import BucketList from '../components/BucketList.vue'
import VmList from '../components/VmList.vue'

const currentMenu = ref('home')
const currentMenuTitle = ref('首页')
const activeTabId = ref('home')
const toastMessage = ref('')
let toastTimer = null

const handleNotice = (msg) => {
  if (typeof msg === 'string') {
    toastMessage.value = msg
  } else {
    toastMessage.value = '运维管理指令已响应'
  }
  if (toastTimer) clearTimeout(toastTimer)
  toastTimer = setTimeout(() => {
    toastMessage.value = ''
  }, 2500)
}

// Tabs matching screenshot: defaults to '首页'
const tabs = ref([
  { id: 'home', name: '首页', closable: false }
])

// Mock data for integrated preview
const tianjiBucketList = ref([
  {
    name: 'oaml-kf-bucket-hk-dev',
    org: '境外分行反洗钱信息系统',
    region: '上海',
    pool: 'ZH_DEV',
    quota: '1000G',
    ha: '多AZ',
    envType: '常态环境',
    env: 'SIT',
    createTime: '2025-12-30 10:28:44'
  },
  {
    name: 'spsd-kf-bucket-ai02',
    org: '浦天开物研发工具体系服务平台',
    region: '上海',
    pool: 'ZH_BIZ02',
    quota: '20G',
    ha: '多AZ',
    envType: '常态环境',
    env: 'SIT',
    createTime: '2026-10-21 14:07:49'
  },
  {
    name: 'znwd-kf-bucket-uat',
    org: '智能问答组件系统',
    region: '上海',
    pool: 'ZH_DEV',
    quota: '1000G',
    ha: '多AZ',
    envType: '常态环境',
    env: 'SIT',
    createTime: '2025-11-10 14:01:00'
  }
])

const evsList = ref([
  {
    id: '52502c0b-126e-4a62-8178-9031efb78341',
    name: 'ogls-uatap-hkg02-volume-0000',
    status: '已挂载',
    org: '境外分行会计核算及总账系统',
    region: '上海',
    zone: '上海通用二区L1（赵巷）',
    mountPoint: '/dev/vda',
    capacity: '50',
    env: 'SIT'
  },
  {
    id: 'd67965f9-a849-432c-9821-66710b746812',
    name: 'ogls-uatap-hkg02-volume-0001',
    status: '已挂载',
    org: '境外分行会计核算及总账系统',
    region: '上海',
    zone: '上海通用二区L1（赵巷）',
    mountPoint: '/dev/vdb',
    capacity: '100',
    env: 'SIT'
  }
])

const handleNavSelect = (navId) => {
  handleNotice(`已切换运维导航：${navId}`)
}

const handleMenuSelect = (item) => {
  currentMenu.value = item.id
  currentMenuTitle.value = item.name
  activeTabId.value = item.id

  const exists = tabs.value.some(t => t.id === item.id)
  if (!exists) {
    tabs.value.push({
      id: item.id,
      name: item.name,
      closable: true
    })
  }
}

const handleTabSelect = (tabId) => {
  activeTabId.value = tabId
  const tab = tabs.value.find(t => t.id === tabId)
  if (tab) {
    currentMenu.value = tab.id
    currentMenuTitle.value = tab.name
  }
}

const handleTabClose = (tabId) => {
  const index = tabs.value.findIndex(t => t.id === tabId)
  if (index !== -1) {
    tabs.value.splice(index, 1)
    if (activeTabId.value === tabId) {
      const nextTab = tabs.value[index - 1] || tabs.value[0]
      activeTabId.value = nextTab.id
      currentMenu.value = nextTab.id
      currentMenuTitle.value = nextTab.name
    }
  }
}

const handleBack = () => {
  handleGoHome()
}

const handleGoHome = () => {
  activeTabId.value = 'home'
  currentMenu.value = 'home'
  currentMenuTitle.value = '首页'
}
</script>

<style scoped>
.ops-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f0f2f5;
}

.main-body {
  display: flex;
  flex: 1;
  height: calc(100vh - 50px);
  overflow: hidden;
}

.content-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  background-color: #f0f2f5;
}

.page-viewport {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
}

.sub-view-wrapper {
  padding: 12px;
}

.placeholder-view {
  padding: 40px;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
}

.placeholder-box {
  background: #ffffff;
  padding: 48px;
  border-radius: 4px;
  text-align: center;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05);
  border: 1px solid #e8eaec;
  max-width: 480px;
  width: 100%;
}

.placeholder-box .icon {
  font-size: 40px;
  margin-bottom: 16px;
}

.placeholder-box h2 {
  font-size: 18px;
  color: #1f2329;
  margin-bottom: 8px;
}

.placeholder-box p {
  color: #8c8c8c;
  font-size: 13px;
  margin-bottom: 24px;
}

.back-home-btn {
  background-color: #1890ff;
  color: #ffffff;
  border: none;
  padding: 8px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 13px;
  transition: background 0.2s;
}

.back-home-btn:hover {
  background-color: #40a9ff;
}

.ops-toast {
  position: fixed;
  top: 24px;
  left: 50%;
  transform: translateX(-50%);
  background-color: #1890ff;
  color: #ffffff;
  padding: 8px 20px;
  border-radius: 4px;
  box-shadow: 0 4px 12px rgba(24, 144, 255, 0.3);
  font-size: 13px;
  z-index: 3000;
}

.toast-fade-enter-active,
.toast-fade-leave-active {
  transition: opacity 0.2s, transform 0.2s;
}

.toast-fade-enter-from,
.toast-fade-leave-to {
  opacity: 0;
  transform: translate(-50%, -10px);
}
</style>
