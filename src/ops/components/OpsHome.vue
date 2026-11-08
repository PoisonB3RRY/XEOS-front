<template>
  <div class="ops-home">
    <div class="card-box">
      <!-- SPDB Gradient Banner -->
      <div class="spdb-banner">
        <span class="banner-title">SPDB</span>
      </div>

      <!-- Sub Navigation Tabs -->
      <div class="notice-tabs">
        <div class="tabs-left">
          <div 
            v-for="t in tabs" 
            :key="t.key"
            :class="['notice-tab-item', { active: currentTab === t.key }]"
            @click="switchTab(t.key)"
          >
            {{ t.label }}
          </div>
        </div>

        <div class="tabs-right">
          <!-- Toggle sample data for demo -->
          <button class="mock-toggle-btn" @click="toggleMockData">
            {{ showSampleData ? '还原截图空状态 (共0条)' : '加载样例数据演示' }}
          </button>
        </div>
      </div>

      <!-- Data Table -->
      <div class="table-container">
        <table class="ops-table">
          <thead>
            <tr>
              <th class="col-content">通知内容</th>
              <th class="col-author">更新人</th>
              <th class="col-time">更新时间</th>
              <th class="col-file">通知附件</th>
              <th class="col-action">操作</th>
            </tr>
          </thead>
          <tbody>
            <!-- Empty State (Screenshot Replica) -->
            <tr v-if="!showSampleData || currentList.length === 0">
              <td colspan="5" class="empty-cell">
                <div class="empty-wrap">
                  <span class="empty-text">暂无数据</span>
                </div>
              </td>
            </tr>

            <!-- Mock Data Rows (if toggled) -->
            <tr v-else v-for="item in currentList" :key="item.id">
              <td class="col-content">
                <span class="notice-badge" :class="item.level">{{ item.type }}</span>
                <span class="notice-title-text">{{ item.title }}</span>
              </td>
              <td class="col-author">{{ item.author }}</td>
              <td class="col-time">{{ item.updateTime }}</td>
              <td class="col-file">
                <span v-if="item.attachment" class="file-link" @click="handleDownload(item)">
                  📎 {{ item.attachment }}
                </span>
                <span v-else class="text-muted">-</span>
              </td>
              <td class="col-action">
                <a class="action-btn" @click="handleView(item)">查看详情</a>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination Footer -->
      <div class="pagination-footer">
        <div class="pagination-left">
          <button class="page-arrow" :disabled="currentPage <= 1" @click="currentPage--">&lt;</button>
          <span class="page-num active">1</span>
          <button class="page-arrow" :disabled="currentPage >= totalPages" @click="currentPage++">&gt;</button>
          <span class="page-jump">
            前往 
            <input 
              type="text" 
              class="page-input" 
              v-model="inputPage" 
              @keydown.enter="handleJump"
            /> 
            页
          </span>
        </div>

        <div class="pagination-right">
          <span class="total-text">共 {{ showSampleData ? currentList.length : 0 }} 条</span>
        </div>
      </div>
    </div>

    <!-- Notice Detail Modal -->
    <div v-if="selectedNotice" class="modal-overlay" @click.self="selectedNotice = null">
      <div class="modal-box">
        <div class="modal-header">
          <h3>{{ selectedNotice.title }}</h3>
          <button class="close-btn" @click="selectedNotice = null">×</button>
        </div>
        <div class="modal-body">
          <div class="info-meta">
            <span>发布类型: <b>{{ selectedNotice.type }}</b></span>
            <span>更新人: <b>{{ selectedNotice.author }}</b></span>
            <span>更新时间: <b>{{ selectedNotice.updateTime }}</b></span>
          </div>
          <div class="info-content">
            <p>{{ selectedNotice.detail }}</p>
          </div>
          <div v-if="selectedNotice.attachment" class="info-attachment">
            <span>附件：</span>
            <span class="file-tag">📎 {{ selectedNotice.attachment }}</span>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn-primary" @click="selectedNotice = null">关闭</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const currentTab = ref('security')
const showSampleData = ref(false)
const currentPage = ref(1)
const inputPage = ref('1')
const selectedNotice = ref(null)

const tabs = [
  { key: 'security', label: '安全通知' },
  { key: 'announcement', label: '平台公告' },
  { key: 'manual', label: '使用手册' }
]

const sampleNotices = {
  security: [
    {
      id: 1,
      type: '高危',
      level: 'danger',
      title: '关于开展2026年第4季度全行信创云平台安全漏洞补丁加固的通知',
      author: '安全运维组 (12014844)',
      updateTime: '2026-11-06 14:32:10',
      attachment: '信创平台安全加固操作指引_v3.1.pdf',
      detail: '各运维团队请注意：定于本周五晚22:00对信创通用二区底座及信创对象存储服务进行Kernel内核热补丁更新与SSL协议套件升级，请提前做好巡检与监控保障。'
    },
    {
      id: 2,
      type: '提示',
      level: 'warning',
      title: '信创对象存储XEOS访问密钥与权限策略定期轮换提醒',
      author: '平台运营组 (12003891)',
      updateTime: '2026-11-01 09:15:00',
      attachment: 'XEOS密钥轮换操作手册.docx',
      detail: '根据总行信息安全规范要求，已到期的AK/SK密钥需在15个工作日内完成更新，请各租户管理员与运维专员协同排查。'
    }
  ],
  announcement: [
    {
      id: 3,
      type: '通知',
      level: 'info',
      title: '浦发银行云管理平台PCMP信创双AZ高可用能力正式上线公告',
      author: '云架构规划组',
      updateTime: '2026-10-28 17:00:22',
      attachment: 'PCMP_双AZ架构白皮书.pdf',
      detail: '上海通用二区L1/L2已全面完成双活跨可用区存储复制部署，支持信创云硬盘EVS与信创对象存储XEOS同城容灾自动切换。'
    },
    {
      id: 4,
      type: '维护',
      level: 'info',
      title: '关于2026年11月网络骨干交换机例行割接维护通知',
      author: '网络运维组',
      updateTime: '2026-10-25 11:20:05',
      attachment: null,
      detail: '割接期间管理面API存在瞬断重试机制，业务数据面不受影响。'
    }
  ],
  manual: [
    {
      id: 5,
      type: '文档',
      level: 'primary',
      title: '浦发银行云管理平台运维人员操作手册 (PCMP-V4.5)',
      author: '知识库管理员',
      updateTime: '2026-10-15 16:40:00',
      attachment: '浦发银行云管理平台_运维手册_v4.5.pdf',
      detail: '涵盖网关配置、虚拟机运维生命周期管理、裸金属管理、存储服务快照配置、桶配额管理等详细规程。'
    },
    {
      id: 6,
      type: '指南',
      level: 'primary',
      title: '信创云存储 (XEOS/EVS/SFS) 紧急故障应急处置预案',
      author: '存储保障专家组',
      updateTime: '2026-09-30 10:05:12',
      attachment: '存储故障应急预案_2026.pdf',
      detail: '包含快照应急恢复流程、跨区域复制中断排查、存储桶只读锁定与排错指导。'
    }
  ]
}

const currentList = computed(() => {
  if (!showSampleData.value) return []
  return sampleNotices[currentTab.value] || []
})

const totalPages = computed(() => {
  return 1
})

const switchTab = (tabKey) => {
  currentTab.value = tabKey
}

const toggleMockData = () => {
  showSampleData.value = !showSampleData.value
}

const handleJump = () => {
  const p = parseInt(inputPage.value, 10)
  if (!isNaN(p) && p >= 1) {
    currentPage.value = p
  }
}

const handleView = (item) => {
  selectedNotice.value = item
}

const handleDownload = (item) => {
  alert(`模拟下载附件: ${item.attachment}`)
}
</script>

<style scoped>
.ops-home {
  padding: 14px 16px;
  background-color: #f0f2f5;
  min-height: calc(100vh - 88px);
}

.card-box {
  background-color: #ffffff;
  border: 1px solid #e8eaec;
  border-radius: 2px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
  min-height: 520px;
  display: flex;
  flex-direction: column;
}

/* SPDB Red to Blue Gradient Banner */
.spdb-banner {
  height: 38px;
  /* Matches screenshot: Burgundy/Red -> Violet -> Deep Blue */
  background: linear-gradient(90deg, #9f1c24 0%, #aa1e29 18%, #66276b 55%, #184c9c 85%, #0b51b7 100%);
  display: flex;
  align-items: center;
  padding: 0 16px;
  border-top-left-radius: 2px;
  border-top-right-radius: 2px;
}

.banner-title {
  color: #ffffff;
  font-size: 15px;
  font-weight: 700;
  letter-spacing: 0.5px;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  user-select: none;
}

/* Sub Navigation Tabs */
.notice-tabs {
  height: 44px;
  border-bottom: 1px solid #e8eaec;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px;
  user-select: none;
}

.tabs-left {
  display: flex;
  align-items: center;
  gap: 24px;
  height: 100%;
}

.notice-tab-item {
  display: flex;
  align-items: center;
  height: 100%;
  font-size: 13px;
  color: #595959;
  cursor: pointer;
  position: relative;
  transition: all 0.2s;
  padding: 0 4px;
}

.notice-tab-item:hover {
  color: #1890ff;
}

.notice-tab-item.active {
  color: #1890ff;
  font-weight: 500;
}

.notice-tab-item.active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 2px;
  background-color: #1890ff;
}

.tabs-right {
  display: flex;
  align-items: center;
}

.mock-toggle-btn {
  background: #f5f5f5;
  border: 1px solid #d9d9d9;
  font-size: 11px;
  color: #666;
  padding: 3px 10px;
  border-radius: 3px;
  cursor: pointer;
  transition: all 0.2s;
}

.mock-toggle-btn:hover {
  color: #1890ff;
  border-color: #91d5ff;
  background: #e6f7ff;
}

/* Data Table */
.table-container {
  flex: 1;
  padding: 0;
  overflow-x: auto;
}

.ops-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}

.ops-table th {
  background-color: #fafafa;
  color: #595959;
  font-weight: 500;
  font-size: 13px;
  padding: 12px 16px;
  border-bottom: 1px solid #e8eaec;
  white-space: nowrap;
}

.ops-table td {
  padding: 14px 16px;
  font-size: 13px;
  color: #262626;
  border-bottom: 1px solid #f0f0f0;
}

.col-content {
  width: 45%;
}

.col-author {
  width: 15%;
}

.col-time {
  width: 15%;
}

.col-file {
  width: 15%;
}

.col-action {
  width: 10%;
  text-align: center;
}

.ops-table th.col-action {
  text-align: center;
}

/* Empty State */
.empty-cell {
  height: 280px;
  text-align: center;
  vertical-align: middle;
}

.empty-wrap {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.empty-text {
  font-size: 13px;
  color: #8c8c8c;
}

/* Table Row Details */
.notice-badge {
  display: inline-block;
  font-size: 11px;
  padding: 1px 6px;
  border-radius: 2px;
  margin-right: 8px;
  line-height: 1.4;
}

.notice-badge.danger {
  background-color: #fff1f0;
  border: 1px solid #ffa39e;
  color: #f5222d;
}

.notice-badge.warning {
  background-color: #fffbe6;
  border: 1px solid #ffe58f;
  color: #faad14;
}

.notice-badge.info {
  background-color: #e6f7ff;
  border: 1px solid #91d5ff;
  color: #1890ff;
}

.notice-badge.primary {
  background-color: #f6ffed;
  border: 1px solid #b7eb8f;
  color: #52c41a;
}

.notice-title-text {
  font-weight: 500;
  color: #262626;
}

.file-link {
  color: #1890ff;
  cursor: pointer;
  text-decoration: none;
  font-size: 12px;
}

.file-link:hover {
  text-decoration: underline;
}

.text-muted {
  color: #bfbfbf;
}

.action-btn {
  color: #1890ff;
  cursor: pointer;
  font-size: 12px;
  text-decoration: none;
}

.action-btn:hover {
  text-decoration: underline;
}

/* Pagination Footer */
.pagination-footer {
  height: 48px;
  border-top: 1px solid #e8eaec;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px;
  font-size: 12px;
  color: #595959;
  user-select: none;
}

.pagination-left {
  display: flex;
  align-items: center;
  gap: 8px;
}

.page-arrow {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #d9d9d9;
  background: #ffffff;
  border-radius: 3px;
  cursor: pointer;
  color: #595959;
  font-size: 12px;
  transition: all 0.15s;
}

.page-arrow:disabled {
  color: #bfbfbf;
  border-color: #e8eaec;
  cursor: not-allowed;
  background: #fafafa;
}

.page-arrow:not(:disabled):hover {
  border-color: #1890ff;
  color: #1890ff;
}

.page-num {
  min-width: 24px;
  height: 24px;
  padding: 0 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 3px;
  cursor: pointer;
  border: 1px solid transparent;
}

.page-num.active {
  background-color: #1890ff;
  color: #ffffff;
  border-color: #1890ff;
  font-weight: 500;
}

.page-jump {
  margin-left: 10px;
  display: flex;
  align-items: center;
  gap: 4px;
}

.page-input {
  width: 32px;
  height: 24px;
  text-align: center;
  border: 1px solid #d9d9d9;
  border-radius: 3px;
  padding: 0 2px;
  font-size: 12px;
  outline: none;
}

.page-input:focus {
  border-color: #1890ff;
  box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.2);
}

.pagination-right {
  color: #595959;
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}

.modal-box {
  background-color: #ffffff;
  border-radius: 4px;
  width: 580px;
  max-width: 90vw;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  overflow: hidden;
}

.modal-header {
  padding: 14px 20px;
  border-bottom: 1px solid #e8eaec;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.modal-header h3 {
  font-size: 15px;
  font-weight: 600;
  color: #1f2329;
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  font-size: 20px;
  color: #8c8c8c;
  cursor: pointer;
}

.modal-body {
  padding: 20px;
}

.info-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  font-size: 12px;
  color: #595959;
  padding-bottom: 12px;
  border-bottom: 1px solid #f0f0f0;
  margin-bottom: 14px;
}

.info-content {
  font-size: 13px;
  color: #262626;
  line-height: 1.7;
  margin-bottom: 16px;
}

.info-attachment {
  font-size: 12px;
  color: #595959;
  display: flex;
  align-items: center;
}

.file-tag {
  background-color: #f0f5ff;
  border: 1px solid #adc6ff;
  color: #2f54eb;
  padding: 2px 8px;
  border-radius: 2px;
}

.modal-footer {
  padding: 12px 20px;
  border-top: 1px solid #e8eaec;
  text-align: right;
  background: #fafafa;
}

.btn-primary {
  background-color: #1890ff;
  color: #ffffff;
  border: none;
  padding: 5px 16px;
  border-radius: 3px;
  cursor: pointer;
  font-size: 13px;
}

.btn-primary:hover {
  background-color: #40a9ff;
}
</style>
