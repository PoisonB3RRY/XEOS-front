<template>
  <div class="app-layout">
    <!-- Top Global Header -->
    <Header 
      v-model="currentProduct" 
      @change="handleProductChange"
    />

    <!-- Main Container (Sidebar + Content Area) -->
    <div class="main-body">
      <!-- Left Navigation Sidebar -->
      <Sidebar 
        :current-product="currentProduct"
        v-model="currentMenu"
        @select-menu="handleMenuSelect"
      />

      <!-- Right Content Layout -->
      <div class="content-wrapper">
        <!-- Tab Navigation Bar -->
        <TabBar 
          :tabs="tabs"
          v-model:active-tab="activeTabId"
          @tab-click="handleTabClick"
          @tab-close="handleTabClose"
          @back="handleGoBack"
        />

        <!-- Scrollable Page Container -->
        <main class="page-content">
          <!-- 玄武云虚拟机列表页 (复刻截图2) -->
          <VmList 
            v-if="currentView === 'vm-list'"
            @select-vm="handleSelectVm"
            @open-snapshot="(item) => handleSelectVm({ item, tab: 'snapshot' })"
          />

          <!-- 玄武云虚拟机详情页 (复刻截图1与3，含基本信息、硬盘管理[新增回收站按钮]、快照管理) -->
          <VmDetail 
            v-else-if="currentView === 'vm-detail'"
            :instance-data="selectedVm"
            :default-tab="vmDetailDefaultTab"
            @back="handleGoBack"
          />

          <!-- 玄武云 / 对象存储桶 列表页 -->
          <BucketList 
            v-else-if="currentView === 'bucket-list'"
            @select-bucket="handleSelectBucket"
            @open-auth="handleOpenAuth"
          />

          <!-- 桶详情页 (跨域复制 / 授权管理 / 基本信息) -->
          <BucketDetail 
            v-else-if="currentView === 'bucket-detail'"
            :bucket-name="selectedBucketName"
            :default-tab="detailDefaultTab"
            @back="handleGoBack"
          />

          <!-- 其它服务模块占位 -->
          <div v-else class="other-view-placeholder">
            <div class="placeholder-card">
              <div class="placeholder-icon">🚀</div>
              <h3>{{ getMenuTitle(currentMenu) }} 功能模块</h3>
              <p>该功能正在接入中，欢迎随时提出定制需求。</p>
            </div>
          </div>
        </main>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import Header from './components/Header.vue'
import Sidebar from './components/Sidebar.vue'
import TabBar from './components/TabBar.vue'
import BucketList from './components/BucketList.vue'
import BucketDetail from './components/BucketDetail.vue'
import VmList from './components/VmList.vue'
import VmDetail from './components/VmDetail.vue'

// Top Product selection: 'xuanwu' (default) | 'tianji'
const currentProduct = ref('xuanwu')

// Sidebar Menu selection: default to 'vm' matching user screenshots
const currentMenu = ref('vm')

// Main View: 'vm-list' | 'vm-detail' | 'bucket-list' | 'bucket-detail' | 'other'
const currentView = ref('vm-list')

// Selected VM instance data
const selectedVm = ref({
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
const vmDetailDefaultTab = ref('info')

// Selected bucket name for detail view
const selectedBucketName = ref('test-1')
const detailDefaultTab = ref('ccr')

// Dynamic Tabs for TabBar
const tabs = ref([
  { id: 'home', name: '首页', closable: false },
  { id: 'vm', name: '云虚拟机', closable: true }
])
const activeTabId = ref('vm')

const handleProductChange = (productId) => {
  if (productId === 'xuanwu') {
    currentMenu.value = 'vm'
    currentView.value = 'vm-list'
    activeTabId.value = 'vm'
    ensureTab({ id: 'vm', name: '云虚拟机', closable: true })
  } else if (productId === 'tianji') {
    currentMenu.value = 'tianji-obs-bucket'
    currentView.value = 'bucket-detail'
    activeTabId.value = 'tianji-obs-bucket'
    ensureTab({ id: 'tianji-obs-bucket', name: '信创对象存储-桶(OBS)', closable: true })
  }
}

const handleMenuSelect = (menuId) => {
  if (menuId === 'vm') {
    currentView.value = 'vm-list'
    activeTabId.value = 'vm'
    ensureTab({ id: 'vm', name: '云虚拟机', closable: true })
  } else if (menuId === 'obs-bucket') {
    currentView.value = 'bucket-list'
    activeTabId.value = 'obs-bucket'
    ensureTab({ id: 'obs-bucket', name: '对象存储桶', closable: true })
  } else if (menuId === 'tianji-obs-bucket') {
    currentView.value = 'bucket-detail'
    activeTabId.value = 'tianji-obs-bucket'
    ensureTab({ id: 'tianji-obs-bucket', name: '信创对象存储-桶(OBS)', closable: true })
  } else {
    currentView.value = 'other'
    activeTabId.value = menuId
    ensureTab({ id: menuId, name: getMenuTitle(menuId), closable: true })
  }
}

const handleSelectVm = ({ item, tab }) => {
  selectedVm.value = { ...item }
  vmDetailDefaultTab.value = tab || 'info'
  currentView.value = 'vm-detail'
  const detailTabId = `vm-${item.name}`
  ensureTab({ id: detailTabId, name: item.name, closable: true })
  activeTabId.value = detailTabId
}

const handleSelectBucket = (bucketName) => {
  selectedBucketName.value = bucketName
  detailDefaultTab.value = 'ccr'
  currentView.value = 'bucket-detail'
  const detailTabId = `bucket-${bucketName}`
  ensureTab({ id: detailTabId, name: bucketName, closable: true })
  activeTabId.value = detailTabId
}

const handleOpenAuth = (bucketName) => {
  selectedBucketName.value = bucketName
  detailDefaultTab.value = 'auth'
  currentView.value = 'bucket-detail'
  const detailTabId = `bucket-${bucketName}`
  ensureTab({ id: detailTabId, name: bucketName, closable: true })
  activeTabId.value = detailTabId
}

const handleGoBack = () => {
  if (currentView.value === 'vm-detail') {
    currentView.value = 'vm-list'
    activeTabId.value = 'vm'
  } else {
    currentView.value = 'bucket-list'
    activeTabId.value = 'obs-bucket'
  }
}

const handleTabClick = (tabId) => {
  if (tabId === 'home' || tabId === 'vm') {
    currentView.value = 'vm-list'
    currentMenu.value = 'vm'
    activeTabId.value = 'vm'
  } else if (tabId.startsWith('vm-')) {
    currentView.value = 'vm-detail'
    activeTabId.value = tabId
  } else if (tabId === 'obs-bucket') {
    currentView.value = 'bucket-list'
    currentMenu.value = 'obs-bucket'
    activeTabId.value = 'obs-bucket'
  } else if (tabId.startsWith('bucket-')) {
    currentView.value = 'bucket-detail'
    activeTabId.value = tabId
  } else if (tabId === 'tianji-obs-bucket') {
    currentView.value = 'bucket-detail'
    currentMenu.value = 'tianji-obs-bucket'
    activeTabId.value = 'tianji-obs-bucket'
  } else {
    currentView.value = 'other'
    currentMenu.value = tabId
    activeTabId.value = tabId
  }
}

const handleTabClose = (tabId) => {
  tabs.value = tabs.value.filter(t => t.id !== tabId)
  if (activeTabId.value === tabId) {
    const last = tabs.value[tabs.value.length - 1]
    if (last) {
      activeTabId.value = last.id
      handleTabClick(last.id)
    }
  }
}

const ensureTab = (tab) => {
  const exists = tabs.value.some(t => t.id === tab.id)
  if (!exists) {
    tabs.value.push(tab)
  }
}

const menuTitles = {
  'vm': '云虚拟机',
  'obs-bucket': '对象存储桶',
  'obs-user': '对象存储用户',
  'tianji-obs-bucket': '信创对象存储-桶(OBS)',
  'tianji-obs-user': '信创对象存储-用户',
  'evs': '信创云硬盘(EVS)',
  'sfs': '信创文件存储(SFS)',
  'snapshot': '信创快照',
  'mq': '消息队列服务',
  'cache': '缓存服务',
  'analytics': '数据计算与分析服务',
  'compute': '计算服务',
  'trash': '回收站',
  'network': '网络服务'
}

const getMenuTitle = (id) => menuTitles[id] || '业务服务'
</script>

<style scoped>
.app-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f0f2f5;
}

.main-body {
  flex: 1;
  display: flex;
  overflow: hidden;
}

.content-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  background-color: #f0f2f5;
}

.page-content {
  flex: 1;
  padding: 12px 16px 20px;
  overflow-y: auto;
}

.other-view-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  min-height: 380px;
}

.placeholder-card {
  background: #ffffff;
  border-radius: 4px;
  padding: 60px 80px;
  text-align: center;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.placeholder-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.placeholder-card h3 {
  font-size: 18px;
  color: #1f2d3d;
  margin-bottom: 8px;
  font-weight: 500;
}

.placeholder-card p {
  color: #909399;
  font-size: 13px;
}
</style>
