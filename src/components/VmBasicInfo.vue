<template>
  <div class="vm-basic-info-container">
    <div class="info-layout">
      <!-- Left Column: VM Information -->
      <div class="info-card left-card">
        <div class="card-header">
          <h3 class="card-title">云虚拟机信息</h3>
        </div>
        <div class="info-grid">
          <div class="info-row">
            <div class="info-item">
              <span class="label">实例名称</span>
              <span class="value">{{ vmData.name }}</span>
            </div>
            <div class="info-item">
              <span class="label">实例ID</span>
              <span class="value value-with-copy">
                {{ vmData.id }}
                <button class="btn-copy" title="复制" @click="copyText(vmData.id)">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                    <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
                  </svg>
                </button>
              </span>
            </div>
          </div>

          <div class="info-row">
            <div class="info-item">
              <span class="label">资源组织</span>
              <span class="value">{{ vmData.org }}</span>
            </div>
            <div class="info-item">
              <span class="label">属主</span>
              <span class="value">{{ vmData.owner }}</span>
            </div>
          </div>

          <div class="info-row">
            <div class="info-item">
              <span class="label">区域</span>
              <span class="value">{{ vmData.region }}</span>
            </div>
            <div class="info-item">
              <span class="label">可用区</span>
              <span class="value">{{ vmData.zone }}</span>
            </div>
          </div>

          <div class="info-row">
            <div class="info-item">
              <span class="label">操作系统</span>
              <span class="value">{{ vmData.os }}</span>
            </div>
            <div class="info-item">
              <span class="label">CPU架构</span>
              <span class="value">{{ vmData.arch }}</span>
            </div>
          </div>

          <div class="info-row">
            <div class="info-item">
              <span class="label">CPU核心数</span>
              <span class="value">{{ vmData.cpuCores }}</span>
            </div>
            <div class="info-item">
              <span class="label">内存</span>
              <span class="value">{{ vmData.memory }}</span>
            </div>
          </div>

          <div class="info-row">
            <div class="info-item">
              <span class="label">创建时间</span>
              <span class="value">{{ vmData.createTime }}</span>
            </div>
            <div class="info-item">
              <span class="label">过期时间</span>
              <span class="value">{{ vmData.expireTime }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Right Column: Disk & Network Cards -->
      <div class="right-column">
        <!-- Disk Card -->
        <div class="info-card disk-card">
          <div class="card-header">
            <h3 class="card-title">硬盘</h3>
          </div>
          <div class="simple-list">
            <div class="list-item">
              <span class="list-label">系统盘</span>
              <span class="list-device">{{ vmData.disk.system.mount }}</span>
              <span class="list-capacity">{{ vmData.disk.system.size }}</span>
            </div>
            <div class="list-item">
              <span class="list-label">数据盘</span>
              <span class="list-device">{{ vmData.disk.data.mount }}</span>
              <span class="list-capacity">{{ vmData.disk.data.size }}</span>
            </div>
          </div>
        </div>

        <!-- Network Card -->
        <div class="info-card network-card">
          <div class="card-header">
            <h3 class="card-title">网络</h3>
          </div>
          <div class="simple-list">
            <div class="list-item">
              <span class="list-label">主网卡</span>
              <span class="list-ip">{{ vmData.network.ip }}</span>
              <span class="list-mac">{{ vmData.network.mac }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive } from 'vue'

const props = defineProps({
  vmInfo: {
    type: Object,
    default: () => ({})
  }
})

const vmData = reactive({
  name: props.vmInfo?.name || 'testlu01',
  id: props.vmInfo?.id || '241c6956-2c3e-4461-b55d-afc6e4eafeb2',
  org: props.vmInfo?.org || '金融云门户系统',
  owner: props.vmInfo?.owner || '12064927',
  region: props.vmInfo?.region || '上海',
  zone: props.vmInfo?.zone || '上海裸金属一区（赵巷）',
  os: props.vmInfo?.os || 'Kylin Linux Advanced Server V10 (64-bit)',
  arch: props.vmInfo?.arch || 'C86',
  cpuCores: props.vmInfo?.cpuCores || '4',
  memory: props.vmInfo?.memory || '8GB',
  createTime: props.vmInfo?.createTime || '2026-09-14 17:28:09',
  expireTime: props.vmInfo?.expireTime || '2026-12-13',
  disk: {
    system: {
      mount: 'sda',
      size: '130G'
    },
    data: {
      mount: '--',
      size: '--'
    }
  },
  network: {
    ip: props.vmInfo?.ip || '190.23.55.19',
    mac: '52:54:00:91:c1:3d'
  }
})

const copyText = (text) => {
  if (navigator.clipboard) {
    navigator.clipboard.writeText(text)
  }
}
</script>

<style scoped>
.vm-basic-info-container {
  padding: 16px 20px 24px;
}

.info-layout {
  display: flex;
  gap: 16px;
  align-items: stretch;
}

.left-card {
  flex: 1.8;
  min-width: 0;
}

.right-column {
  flex: 1.2;
  display: flex;
  flex-direction: column;
  gap: 16px;
  min-width: 0;
}

.info-card {
  background-color: #ffffff;
  border: 1px solid #ebedf0;
  border-radius: 4px;
  padding: 20px 24px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02);
}

.card-header {
  margin-bottom: 22px;
}

.card-title {
  font-size: 14px;
  font-weight: 600;
  color: #1f2d3d;
  margin: 0;
}

.info-grid {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.info-row {
  display: flex;
  align-items: flex-start;
}

.info-item {
  flex: 1;
  display: flex;
  align-items: baseline;
  font-size: 13px;
  line-height: 1.5;
  padding-right: 16px;
}

.info-item .label {
  color: #5c6b77;
  width: 90px;
  flex-shrink: 0;
  user-select: none;
}

.info-item .value {
  color: #1f2d3d;
  font-weight: 400;
  word-break: break-all;
}

.value-with-copy {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.btn-copy {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
  color: #2468f2;
  display: inline-flex;
  align-items: center;
}

.btn-copy svg {
  width: 13px;
  height: 13px;
}

.simple-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
  font-size: 13px;
}

.list-item {
  display: flex;
  align-items: center;
  gap: 32px;
}

.list-label {
  color: #5c6b77;
  width: 60px;
  flex-shrink: 0;
}

.list-device {
  color: #1f2d3d;
  width: 50px;
}

.list-capacity {
  color: #1f2d3d;
}

.list-ip {
  color: #1f2d3d;
  min-width: 110px;
}

.list-mac {
  color: #1f2d3d;
}
</style>
