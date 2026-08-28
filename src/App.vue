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
          <!-- 玄武云 / 对象存储桶 列表页 -->
          <BucketList 
            v-if="currentView === 'bucket-list'"
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

// Top Product selection: 'xuanwu' (default) | 'tianji'
const currentProduct = ref('xuanwu')

// Sidebar Menu selection
const currentMenu = ref('obs-bucket')

// Main View: 'bucket-list' | 'bucket-detail' | 'other'
const currentView = ref('bucket-list')

// Selected bucket name for detail view
const selectedBucketName = ref('test-1')
const detailDefaultTab = ref('ccr')

// Dynamic Tabs for TabBar
const tabs = ref([
  { id: 'home', name: '首页', closable: false },
  { id: 'obs-bucket', name: '对象存储桶', closable: true }
])
const activeTabId = ref('obs-bucket')

const handleProductChange = (productId) => {
  if (productId === 'xuanwu') {
    currentMenu.value = 'obs-bucket'
    currentView.value = 'bucket-list'
    activeTabId.value = 'obs-bucket'
    ensureTab({ id: 'obs-bucket', name: '对象存储桶', closable: true })
  } else if (productId === 'tianji') {
    currentMenu.value = 'tianji-obs-bucket'
    currentView.value = 'bucket-detail'
    activeTabId.value = 'tianji-obs-bucket'
    ensureTab({ id: 'tianji-obs-bucket', name: '信创对象存储-桶(OBS)', closable: true })
  }
}

const handleMenuSelect = (menuId) => {
  if (menuId === 'obs-bucket') {
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
  currentView.value = 'bucket-list'
  activeTabId.value = 'obs-bucket'
}

const handleTabClick = (tabId) => {
  if (tabId === 'home') {
    currentView.value = 'bucket-list'
  } else if (tabId === 'obs-bucket') {
    currentView.value = 'bucket-list'
    currentMenu.value = 'obs-bucket'
  } else if (tabId.startsWith('bucket-')) {
    currentView.value = 'bucket-detail'
  } else if (tabId === 'tianji-obs-bucket') {
    currentView.value = 'bucket-detail'
    currentMenu.value = 'tianji-obs-bucket'
  } else {
    currentView.value = 'other'
    currentMenu.value = tabId
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
