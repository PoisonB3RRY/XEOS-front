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
          <!-- 信创文件存储(SFS) 列表页 (复刻附件照片1) -->
          <SfsList 
            v-if="currentView === 'sfs-list'"
            :instances="sfsList"
            @create="handleOpenSfsCreate"
            @delete="handleDeleteSfs"
            @expand="handleExpandSfs"
          />

          <!-- 信创文件存储(SFS) 创建页 (复刻附件照片2) -->
          <SfsCreate 
            v-else-if="currentView === 'sfs-create'"
            @cancel="handleCloseSfsCreate"
            @success="handleSfsCreated"
          />

          <!-- 信创云硬盘(EVS) 列表页 (复刻附件照片) -->
          <EvsList 
            v-else-if="currentView === 'evs-list'"
            :instances="evsList"
            @create="handleCreateEvs"
            @delete="handleDeleteEvs"
            @expand="handleExpandEvs"
            @notify="showToast"
          />

          <!-- 信创对象存储-桶(OBS) 列表页 (复刻附件照片1) -->
          <TianjiObsList 
            v-else-if="currentView === 'tianji-obs-list'"
            :buckets="tianjiBucketList"
            @create="handleOpenTianjiBucketCreate"
            @delete="handleDeleteTianjiBucket"
            @expand="handleExpandTianjiBucket"
            @select-bucket="handleSelectTianjiBucket"
            @notify="showToast"
          />

          <!-- 信创对象存储-桶(OBS) 创建页 (复刻附件照片2) -->
          <TianjiObsCreate 
            v-else-if="currentView === 'tianji-obs-create'"
            @cancel="handleCloseTianjiBucketCreate"
            @success="handleCreateTianjiBucket"
          />

          <!-- 玄武云虚拟机列表页 -->
          <VmList 
            v-else-if="currentView === 'vm-list'"
            @select-vm="handleSelectVm"
            @open-snapshot="(item) => handleSelectVm({ item, tab: 'snapshot' })"
          />

          <!-- 玄武云虚拟机详情页 -->
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

    <!-- Global Toast Alert Message -->
    <transition name="toast-fade">
      <div v-if="toastMessage" :class="['global-toast', `toast-${toastType}`]">
        <span class="toast-icon">
          <svg v-if="toastType === 'success'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <polyline points="20 6 9 17 4 12" />
          </svg>
          <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <circle cx="12" cy="12" r="10" />
            <line x1="12" y1="8" x2="12" y2="12" />
            <line x1="12" y1="16" x2="12.01" y2="16" />
          </svg>
        </span>
        <span class="toast-text">{{ toastMessage }}</span>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Header from './components/Header.vue'
import Sidebar from './components/Sidebar.vue'
import TabBar from './components/TabBar.vue'
import BucketList from './components/BucketList.vue'
import BucketDetail from './components/BucketDetail.vue'
import VmList from './components/VmList.vue'
import VmDetail from './components/VmDetail.vue'
import SfsList from './components/SfsList.vue'
import SfsCreate from './components/SfsCreate.vue'
import EvsList from './components/EvsList.vue'
import TianjiObsList from './components/TianjiObsList.vue'
import TianjiObsCreate from './components/TianjiObsCreate.vue'

// Top Product selection: default to 'tianji' to directly match user request
const currentProduct = ref('tianji')

// Sidebar Menu selection: default to 'sfs'
const currentMenu = ref('sfs')

// Main View: 'sfs-list' | 'sfs-create' | 'vm-list' | 'vm-detail' | 'bucket-list' | 'bucket-detail' | 'other'
const currentView = ref('sfs-list')

// Toast notification state
const toastMessage = ref('')
const toastType = ref('success')
let toastTimer = null

const showToast = (msg, type = 'success') => {
  toastMessage.value = msg
  toastType.value = type
  if (toastTimer) clearTimeout(toastTimer)
  toastTimer = setTimeout(() => {
    toastMessage.value = ''
  }, 3000)
}

// Initial 10 SFS Records exactly matching photo 1
const initialSfsList = [
  {
    id: '9a1d880f-48a8-4d67-a473-3b1ab3act37b',
    name: 'sfs-iirs-test1',
    status: '可用',
    org: '智能投研系统',
    region: '上海',
    zone: '上海通用二区L1（赵巷）',
    type: 'SFS_High_M02',
    capacity: '2457.00',
    netZone: '生产业务区',
    vpc: 'vpc-sh-prod01',
    subnet: 'subnet-storage-01',
    securityGroup: 'sg-sfs-default',
    envType: '常态环境',
    env: 'SIT'
  },
  {
    id: '36707d08-14ec-40dc-8e9e-66d5966f6985',
    name: 'sfs-dps-kf-unload02',
    status: '可用',
    org: '信用卡数据处理系统',
    region: '上海',
    zone: '上海通用二区L1（赵巷）',
    type: 'SFS_High_M02',
    capacity: '4915.00',
    netZone: '生产业务区',
    vpc: 'vpc-sh-prod01',
    subnet: 'subnet-storage-01',
    securityGroup: 'sg-sfs-default',
    envType: '常态环境',
    env: 'SIT'
  },
  {
    id: '67fff945-7334-4988-8edc-14413d3a5ba6',
    name: 'sfs-iirs-spms-rel',
    status: '可用',
    org: '智能投研系统',
    region: '上海',
    zone: '上海通用二区L1（赵巷）',
    type: 'SFS_High_M02',
    capacity: '1228.00',
    netZone: '生产业务区',
    vpc: 'vpc-sh-prod01',
    subnet: 'subnet-storage-01',
    securityGroup: 'sg-sfs-default',
    envType: '常态环境',
    env: 'SIT'
  },
  {
    id: 'c6bfb102-3b22-438e-b91f-d01e7eecf2e0',
    name: 'sfs-nrpt-xc-uat',
    status: '可用',
    org: '报表与信息服务平台系统',
    region: '上海',
    zone: '上海通用二区L1（赵巷）',
    type: 'SFS_High_M02',
    capacity: '1228.00',
    netZone: '测试区',
    vpc: 'vpc-sh-test01',
    subnet: 'subnet-storage-01',
    securityGroup: 'sg-sfs-default',
    envType: '常态环境',
    env: 'SIT'
  },
  {
    id: 'c40da847-b563-44e2-bb0a-319f2349b563',
    name: 'sfs-nrpt-xc-dev',
    status: '可用',
    org: '报表与信息服务平台系统',
    region: '上海',
    zone: '上海通用二区L1（赵巷）',
    type: 'SFS_High_M02',
    capacity: '1228.00',
    netZone: '测试区',
    vpc: 'vpc-sh-dev01',
    subnet: 'subnet-storage-01',
    securityGroup: 'sg-sfs-default',
    envType: '常态环境',
    env: 'SIT'
  },
  {
    id: '756d62515-7148-46de-ab32-032a89d0a568',
    name: 'sfs-dataworks-dev-new',
    status: '可用',
    org: '数据科学家研发平台',
    region: '上海',
    zone: '上海通用二区L1（赵巷）',
    type: 'SFS_SHigh_M03',
    capacity: '1228.00',
    netZone: '测试区',
    vpc: 'vpc-sh-dev01',
    subnet: 'subnet-storage-01',
    securityGroup: 'sg-sfs-default',
    envType: '常态环境',
    env: 'SIT'
  },
  {
    id: '6d4f5dbf-f583-4d9b-8591-ecad1a9e19b7',
    name: 'sfs-turbo-dataworks-new',
    status: '可用',
    org: '数据科学家研发平台',
    region: '上海',
    zone: '上海通用二区L1（赵巷）',
    type: 'SFS_SHigh_M03',
    capacity: '1228.00',
    netZone: '生产业务区',
    vpc: 'vpc-sh-prod01',
    subnet: 'subnet-storage-01',
    securityGroup: 'sg-sfs-default',
    envType: '常态环境',
    env: 'SIT'
  },
  {
    id: 'fac4c867-e462-4236-9ad9-e05f4dbe02d6',
    name: 'sfs-bcap-rel',
    status: '可用',
    org: '区块链应用平台',
    region: '上海',
    zone: '上海通用二区L1（赵巷）',
    type: 'SFS_High_M02',
    capacity: '1228.00',
    netZone: '生产业务区',
    vpc: 'vpc-sh-prod01',
    subnet: 'subnet-storage-01',
    securityGroup: 'sg-sfs-default',
    envType: '常态环境',
    env: 'SIT'
  },
  {
    id: '670e4bfb-b6b9-4611-9476-ccdebaf979b',
    name: 'sfs-bcap-uat',
    status: '可用',
    org: '区块链应用平台',
    region: '上海',
    zone: '上海通用二区L1（赵巷）',
    type: 'SFS_High_M02',
    capacity: '1228.00',
    netZone: '测试区',
    vpc: 'vpc-sh-test01',
    subnet: 'subnet-storage-01',
    securityGroup: 'sg-sfs-default',
    envType: '常态环境',
    env: 'SIT'
  },
  {
    id: '94662a41-710e-452b-ba0e-ab07735da3bb',
    name: 'sfs-zncs-test-vm',
    status: '可用',
    org: '智能体创设平台',
    region: '上海',
    zone: '上海通用二区L1（赵巷）',
    type: 'SFS_High_M02',
    capacity: '1228.00',
    netZone: '测试区',
    vpc: 'vpc-sh-test01',
    subnet: 'subnet-storage-01',
    securityGroup: 'sg-sfs-default',
    envType: '常态环境',
    env: 'SIT'
  }
]

// Generate 85 mock items matching photo's "共 85 条"
const generateMockSfs = () => {
  const list = [...initialSfsList]
  const orgs = [
    '个人网银系统',
    '企业金融服务平台',
    '智能风控平台',
    '移动支付清算平台',
    '资产托管系统',
    '统一身份认证系统',
    '实时反欺诈平台',
    '智慧柜面协同系统'
  ]
  const prefixes = ['gateway', 'ecif', 'pay', 'risk', 'core', 'auth', 'loan', 'credit', 'settle']
  const envs = ['dev', 'test', 'uat', 'prod', 'rel']
  const types = ['SFS_High_M02', 'SFS_SHigh_M03', 'SFS_Capacity_M01']
  const caps = ['1228.00', '2048.00', '2457.00', '3072.00', '4096.00', '4915.00']

  for (let i = 11; i <= 85; i++) {
    const pref = prefixes[(i * 3) % prefixes.length]
    const env = envs[(i * 2) % envs.length]
    const num = String(i).padStart(2, '0')
    const hex = Math.random().toString(16).substring(2, 10)
    list.push({
      id: `${hex}-4f2a-48d9-8591-ecad1a9e${i}`,
      name: `sfs-${pref}-${env}${num}`,
      status: '可用',
      org: orgs[i % orgs.length],
      region: '上海',
      zone: '上海通用二区L1（赵巷）',
      type: types[i % types.length],
      capacity: caps[i % caps.length],
      netZone: i % 2 === 0 ? '生产业务区' : '测试区',
      vpc: 'vpc-sh-prod01',
      subnet: 'subnet-storage-01',
      securityGroup: 'sg-sfs-default',
      envType: '常态环境',
      env: 'SIT'
    })
  }
  return list
}

const sfsList = ref(generateMockSfs())

// Initial 10 EVS Records exactly matching user screenshot
const initialEvsList = [
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
  },
  {
    id: 'ed074854-6c9e-4361-9f7a-8b17326df501',
    name: 'ucrm-pt1-volume-0001',
    status: '已挂载',
    org: '统一客户关系管理系统',
    region: '上海',
    zone: '上海通用二区L1（赵巷）',
    mountPoint: '/dev/vdb',
    capacity: '200',
    env: 'SIT'
  },
  {
    id: '26161912-e83e-47aa-9d51-93107b36f781',
    name: 'ucrm-pt1-volume-0002',
    status: '已挂载',
    org: '统一客户关系管理系统',
    region: '上海',
    zone: '上海通用二区L1（赵巷）',
    mountPoint: '/dev/vdc',
    capacity: '150',
    env: 'SIT'
  },
  {
    id: '50f50d02-8473-4581-b209-66381ab9024f',
    name: 'ucrm-pt1-volume-0000',
    status: '已挂载',
    org: '统一客户关系管理系统',
    region: '上海',
    zone: '上海通用二区L1（赵巷）',
    mountPoint: '/dev/vda',
    capacity: '50',
    env: 'SIT'
  },
  {
    id: 'b50be562-aff4-47b8-8093-cc491ea738b5',
    name: 'plan-zookeeper-test02-volume-0000',
    status: '已挂载',
    org: '客户财富分析及规划系统',
    region: '上海',
    zone: '上海通用二区L2（赵巷）',
    mountPoint: '/dev/vda',
    capacity: '50',
    env: 'SIT'
  },
  {
    id: '5e28aaaf-2582-4211-9a99-0751283cbe9a',
    name: 'plan-zookeeper-test02-volume-0001',
    status: '已挂载',
    org: '客户财富分析及规划系统',
    region: '上海',
    zone: '上海通用二区L2（赵巷）',
    mountPoint: '/dev/vdb',
    capacity: '80',
    env: 'SIT'
  },
  {
    id: '0060ef37-4728-4e89-9e81-b40b15c92881',
    name: 'ecs-arm-linxos-test-volume-0000',
    status: '已挂载',
    org: 'Cloud-Transfer-IaaS',
    region: '上海',
    zone: '上海通用二区L2（赵巷）',
    mountPoint: '/dev/vda',
    capacity: '50',
    env: 'SIT'
  },
  {
    id: '711ab122-41e3-4c57-bf98-0cfa0b34918e',
    name: 'ecs-arm-kylinsp3-test-volume-0000',
    status: '已挂载',
    org: 'Cloud-Transfer-IaaS',
    region: '上海',
    zone: '上海通用二区L2（赵巷）',
    mountPoint: '/dev/vda',
    capacity: '50',
    env: 'SIT'
  },
  {
    id: '38aecf01-40f2-491c-8aa9-47e21a37881b',
    name: 'ecs-arm-kylinsp2-test-volume-0000',
    status: '已挂载',
    org: 'Cloud-Transfer-IaaS',
    region: '上海',
    zone: '上海通用二区L2（赵巷）',
    mountPoint: '/dev/vda',
    capacity: '50',
    env: 'SIT'
  }
]

const generateMockEvs = () => {
  const list = [...initialEvsList]
  const orgs = [
    '个人网银系统',
    '企业金融服务平台',
    '智能风控平台',
    '统一身份认证系统',
    '资产托管系统'
  ]
  const prefixes = ['pay', 'gateway', 'auth', 'loan', 'credit', 'ecif']
  const mounts = ['/dev/vda', '/dev/vdb', '/dev/vdc', '/dev/vdd']
  const caps = ['50', '100', '200', '500', '1024']

  for (let i = 11; i <= 60; i++) {
    const pref = prefixes[i % prefixes.length]
    const hex = Math.random().toString(16).substring(2, 10)
    list.push({
      id: `${hex}-14ec-40dc-8e9e-${i}6d5966f`,
      name: `${pref}-prod-volume-000${i % 10}`,
      status: '已挂载',
      org: orgs[i % orgs.length],
      region: '上海',
      zone: i % 2 === 0 ? '上海通用二区L1（赵巷）' : '上海通用二区L2（赵巷）',
      mountPoint: mounts[i % mounts.length],
      capacity: caps[i % caps.length],
      env: 'SIT'
    })
  }
  return list
}

const evsList = ref(generateMockEvs())

// Initial 10 Tianji OBS Bucket Records exactly matching user photo 1
const initialTianjiBucketList = [
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
  },
  {
    name: 'shfw-kf-bucket-shfw-uat',
    org: '商户类服务平台（信用卡中心）',
    region: '上海',
    pool: 'ZH_DEV',
    quota: '200G',
    ha: '多AZ',
    envType: '常态环境',
    env: 'SIT',
    createTime: '2025-04-14 22:45:21'
  },
  {
    name: 'icard-kf-bucket-uat',
    org: '信用卡网络系统',
    region: '上海',
    pool: 'ZH_DEV',
    quota: '130G',
    ha: '多AZ',
    envType: '常态环境',
    env: 'SIT',
    createTime: '2025-08-05 00:34:06'
  },
  {
    name: 'plms-kf-bucket-sit',
    org: '数智化贷后管理系统',
    region: '上海',
    pool: 'ZH_BIZ02',
    quota: '500G',
    ha: '多AZ',
    envType: '常态环境',
    env: 'SIT',
    createTime: '2026-10-21 11:24:50'
  },
  {
    name: 'zbjc-kf-bucket-rel',
    org: '资本充足率管理及数据披露系统',
    region: '上海',
    pool: 'ZH_DEV',
    quota: '300G',
    ha: '多AZ',
    envType: '常态环境',
    env: 'SIT',
    createTime: '2025-04-09 23:12:02'
  },
  {
    name: 'yxnr-kf-bucket-hftemp-bigfile-hf-rel',
    org: '影像内容管理服务平台',
    region: '上海',
    pool: 'ZH_DEV',
    quota: '1G',
    ha: '多AZ',
    envType: '常态环境',
    env: 'SIT',
    createTime: '2025-06-23 10:31:59'
  },
  {
    name: 'yxnr-kf-bucket-shtemp-bigfile-sh-rel',
    org: '影像内容管理服务平台',
    region: '上海',
    pool: 'ZH_DEV',
    quota: '1G',
    ha: '多AZ',
    envType: '常态环境',
    env: 'SIT',
    createTime: '2025-06-23 10:34:38'
  },
  {
    name: 'znfh-kf-bucket-cs-sit',
    org: '数字员工智能孵化管理平台',
    region: '上海',
    pool: 'ZH_DEV',
    quota: '100G',
    ha: '多AZ',
    envType: '常态环境',
    env: 'SIT',
    createTime: '2025-10-27 18:01:03'
  }
]

// Generate mock items for Tianji OBS Bucket List (total displays 5300)
const generateMockTianjiBuckets = () => {
  const list = [...initialTianjiBucketList]
  const orgs = [
    '境外分行反洗钱信息系统',
    '浦天开物研发工具体系服务平台',
    '智能问答组件系统',
    '商户类服务平台（信用卡中心）',
    '信用卡网络系统',
    '数智化贷后管理系统',
    '资本充足率管理及数据披露系统',
    '影像内容管理服务平台',
    '数字员工智能孵化管理平台',
    '金融云门户系统'
  ]
  const prefixes = ['gateway', 'ecif', 'pay', 'risk', 'core', 'auth', 'loan', 'credit', 'settle', 'media']
  const envs = ['dev', 'sit', 'uat', 'rel', 'prod']
  const pools = ['ZH_DEV', 'ZH_BIZ02', 'ZH_PROD01']
  const quotas = ['1G', '20G', '100G', '200G', '300G', '500G', '1000G']

  for (let i = 11; i <= 60; i++) {
    const pref = prefixes[(i * 3) % prefixes.length]
    const env = envs[(i * 2) % envs.length]
    const num = String(i).padStart(2, '0')
    list.push({
      name: `${pref}-kf-bucket-${env}${num}`,
      org: orgs[i % orgs.length],
      region: '上海',
      pool: pools[i % pools.length],
      quota: quotas[i % quotas.length],
      ha: '多AZ',
      envType: '常态环境',
      env: 'SIT',
      createTime: `2025-${String((i % 12) + 1).padStart(2, '0')}-${String((i % 28) + 1).padStart(2, '0')} 10:${String((i * 7) % 60).padStart(2, '0')}:${String((i * 11) % 60).padStart(2, '0')}`
    })
  }
  return list
}

const tianjiBucketList = ref(generateMockTianjiBuckets())

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

// Dynamic Tabs for TabBar: default to Tianji SFS
const tabs = ref([
  { id: 'home', name: '首页', closable: false },
  { id: 'sfs', name: '信创文件存储(SFS)', closable: true }
])
const activeTabId = ref('sfs')

const handleProductChange = (productId) => {
  if (productId === 'xuanwu') {
    currentMenu.value = 'vm'
    currentView.value = 'vm-list'
    activeTabId.value = 'vm'
    ensureTab({ id: 'vm', name: '云虚拟机', closable: true })
  } else if (productId === 'tianji') {
    currentMenu.value = 'sfs'
    currentView.value = 'sfs-list'
    activeTabId.value = 'sfs'
    ensureTab({ id: 'sfs', name: '信创文件存储(SFS)', closable: true })
  }
}

const handleMenuSelect = (menuId) => {
  if (menuId === 'evs') {
    currentView.value = 'evs-list'
    activeTabId.value = 'evs'
    ensureTab({ id: 'evs', name: '信创云硬盘(EVS)', closable: true })
  } else if (menuId === 'sfs') {
    currentView.value = 'sfs-list'
    activeTabId.value = 'sfs'
    ensureTab({ id: 'sfs', name: '信创文件存储(SFS)', closable: true })
  } else if (menuId === 'vm') {
    currentView.value = 'vm-list'
    activeTabId.value = 'vm'
    ensureTab({ id: 'vm', name: '云虚拟机', closable: true })
  } else if (menuId === 'obs-bucket') {
    currentView.value = 'bucket-list'
    activeTabId.value = 'obs-bucket'
    ensureTab({ id: 'obs-bucket', name: '对象存储桶', closable: true })
  } else if (menuId === 'tianji-obs-bucket') {
    currentView.value = 'tianji-obs-list'
    activeTabId.value = 'tianji-obs-bucket'
    ensureTab({ id: 'tianji-obs-bucket', name: '信创对象存储-桶(OBS)', closable: true })
  } else {
    currentView.value = 'other'
    activeTabId.value = menuId
    ensureTab({ id: menuId, name: getMenuTitle(menuId), closable: true })
  }
}

// EVS Handlers
const handleCreateEvs = (newInstance) => {
  evsList.value.unshift(newInstance)
  showToast(`信创云硬盘【${newInstance.name}】创建成功！`)
}

const handleDeleteEvs = (id) => {
  const item = evsList.value.find(e => e.id === id)
  const name = item ? item.name : ''
  evsList.value = evsList.value.filter(e => e.id !== id)
  showToast(`云硬盘【${name}】已成功删除并移入回收站`, 'success')
}

const handleExpandEvs = ({ id, capacity, name }) => {
  const item = evsList.value.find(e => e.id === id)
  if (item) {
    item.capacity = capacity
    showToast(`云硬盘【${name || item.name}】已成功扩容至 ${capacity} GB`, 'success')
  }
}

// SFS Handlers
const handleOpenSfsCreate = () => {
  currentView.value = 'sfs-create'
}

const handleCloseSfsCreate = () => {
  currentView.value = 'sfs-list'
}

const handleSfsCreated = (newItem) => {
  sfsList.value.unshift(newItem)
  currentView.value = 'sfs-list'
  showToast(`信创文件存储实例【${newItem.name}】创建成功！`)
}

const handleDeleteSfs = (id) => {
  const item = sfsList.value.find(s => s.id === id)
  const name = item ? item.name : ''
  sfsList.value = sfsList.value.filter(s => s.id !== id)
  showToast(`实例【${name}】已成功删除`, 'success')
}

const handleExpandSfs = ({ id, capacity, name }) => {
  const item = sfsList.value.find(s => s.id === id)
  if (item) {
    item.capacity = capacity
    showToast(`实例【${name || item.name}】已成功扩容至 ${capacity} GB`, 'success')
  }
}

// Tianji OBS Handlers
const handleOpenTianjiBucketCreate = () => {
  currentView.value = 'tianji-obs-create'
}

const handleCloseTianjiBucketCreate = () => {
  currentView.value = 'tianji-obs-list'
}

const handleCreateTianjiBucket = (newBucket) => {
  tianjiBucketList.value.unshift(newBucket)
  currentView.value = 'tianji-obs-list'
  showToast(`信创对象存储桶【${newBucket.name}】创建成功！`)
}

const handleDeleteTianjiBucket = (bucketName) => {
  tianjiBucketList.value = tianjiBucketList.value.filter(b => b.name !== bucketName)
  showToast(`信创对象存储桶【${bucketName}】已成功删除`, 'success')
}

const handleExpandTianjiBucket = ({ name, quota }) => {
  const item = tianjiBucketList.value.find(b => b.name === name)
  if (item) {
    item.quota = quota
    showToast(`存储桶【${name}】已成功扩容至 ${quota}`, 'success')
  }
}

const handleSelectTianjiBucket = (bucketName) => {
  selectedBucketName.value = bucketName
  detailDefaultTab.value = 'ccr'
  currentView.value = 'bucket-detail'
  const detailTabId = `bucket-${bucketName}`
  ensureTab({ id: detailTabId, name: bucketName, closable: true })
  activeTabId.value = detailTabId
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
  if (currentView.value === 'sfs-create') {
    currentView.value = 'sfs-list'
  } else if (currentView.value === 'tianji-obs-create') {
    currentView.value = 'tianji-obs-list'
  } else if (currentView.value === 'vm-detail') {
    currentView.value = 'vm-list'
    activeTabId.value = 'vm'
  } else if (currentView.value === 'bucket-detail') {
    if (currentProduct.value === 'tianji') {
      currentView.value = 'tianji-obs-list'
      activeTabId.value = 'tianji-obs-bucket'
    } else {
      currentView.value = 'bucket-list'
      activeTabId.value = 'obs-bucket'
    }
  }
}

const handleTabClick = (tabId) => {
  if (tabId === 'home') {
    if (currentProduct.value === 'tianji') {
      currentView.value = 'sfs-list'
      currentMenu.value = 'sfs'
      activeTabId.value = 'sfs'
    } else {
      currentView.value = 'vm-list'
      currentMenu.value = 'vm'
      activeTabId.value = 'vm'
    }
  } else if (tabId === 'evs') {
    currentView.value = 'evs-list'
    currentMenu.value = 'evs'
    activeTabId.value = 'evs'
  } else if (tabId === 'sfs') {
    currentView.value = 'sfs-list'
    currentMenu.value = 'sfs'
    activeTabId.value = 'sfs'
  } else if (tabId === 'vm') {
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
    currentView.value = 'tianji-obs-list'
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
  position: relative;
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

/* Toast Message */
.global-toast {
  position: fixed;
  top: 60px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 9999;
  background: #ffffff;
  padding: 10px 18px;
  border-radius: 4px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13.5px;
}

.toast-success {
  border-left: 4px solid #52c41a;
  color: #333333;
}

.toast-success .toast-icon {
  color: #52c41a;
  display: flex;
  align-items: center;
}

.toast-icon svg {
  width: 18px;
  height: 18px;
}

.toast-fade-enter-active,
.toast-fade-leave-active {
  transition: all 0.25s ease;
}

.toast-fade-enter-from,
.toast-fade-leave-to {
  opacity: 0;
  transform: translate(-50%, -10px);
}
</style>
