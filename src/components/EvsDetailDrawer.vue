<template>
  <div v-if="visible" class="drawer-overlay" @click.self="close">
    <div class="drawer-container">
      <div class="drawer-header">
        <div class="header-title">
          <span class="badge-type">EVS 云硬盘</span>
          <h3>{{ instance?.name }}</h3>
        </div>
        <button class="drawer-close-btn" @click="close">×</button>
      </div>

      <div class="drawer-body">
        <div class="detail-section">
          <h4 class="section-title">基本信息</h4>
          <div class="grid-props">
            <div class="prop-item">
              <span class="prop-label">硬盘名称</span>
              <span class="prop-val">{{ instance?.name }}</span>
            </div>
            <div class="prop-item">
              <span class="prop-label">状态</span>
              <span class="prop-val status-val">
                <span class="status-dot"></span>
                <span>{{ instance?.status || '已挂载' }}</span>
              </span>
            </div>
            <div class="prop-item">
              <span class="prop-label">硬盘 ID</span>
              <span class="prop-val font-mono">{{ instance?.id }}</span>
            </div>
            <div class="prop-item">
              <span class="prop-label">资源组织</span>
              <span class="prop-val">{{ instance?.org }}</span>
            </div>
            <div class="prop-item">
              <span class="prop-label">区域</span>
              <span class="prop-val">{{ instance?.region || '上海' }}</span>
            </div>
            <div class="prop-item">
              <span class="prop-label">可用区</span>
              <span class="prop-val">{{ instance?.zone || '上海通用二区L1（赵巷）' }}</span>
            </div>
            <div class="prop-item">
              <span class="prop-label">硬盘容量</span>
              <span class="prop-val font-bold">{{ instance?.capacity || '50' }} GB</span>
            </div>
            <div class="prop-item">
              <span class="prop-label">磁盘类型</span>
              <span class="prop-val">高IO (SAS)</span>
            </div>
            <div class="prop-item">
              <span class="prop-label">部署环境</span>
              <span class="prop-val font-bold text-primary">{{ instance?.env || 'SIT' }}</span>
            </div>
            <div class="prop-item">
              <span class="prop-label">共享盘</span>
              <span class="prop-val">否</span>
            </div>
            <div class="prop-item">
              <span class="prop-label">可启动</span>
              <span class="prop-val">是</span>
            </div>
          </div>
        </div>

        <div class="detail-section">
          <h4 class="section-title">挂载信息</h4>
          <div class="grid-props">
            <div class="prop-item">
              <span class="prop-label">设备挂载点</span>
              <span class="prop-val font-mono font-bold text-primary">{{ instance?.mountPoint || '/dev/vda' }}</span>
            </div>
            <div class="prop-item">
              <span class="prop-label">挂载虚拟机</span>
              <span class="prop-val font-mono">{{ instance?.name?.replace(/-volume-\d+$/, '') || 'vm-instance' }}</span>
            </div>
            <div class="prop-item">
              <span class="prop-label">挂载模式</span>
              <span class="prop-val">读写 (Read/Write)</span>
            </div>
            <div class="prop-item">
              <span class="prop-label">挂载时间</span>
              <span class="prop-val">2026-09-15 10:24:32</span>
            </div>
          </div>
        </div>

        <div class="detail-section">
          <h4 class="section-title">快照与备份策略</h4>
          <div class="mount-box">
            <div class="mount-tip">当前硬盘关联快照数：1 个</div>
            <div class="snapshot-row">
              <span class="font-mono">snap-auto-bak-01 (50 GB)</span>
              <span class="text-gray">2026-10-18 02:00:00</span>
            </div>
          </div>
        </div>
      </div>

      <div class="drawer-footer">
        <button class="btn btn-default" @click="close">关闭</button>
        <button class="btn btn-primary" @click="$emit('expand', instance)">扩容硬盘</button>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  },
  instance: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['update:visible', 'expand'])

const close = () => {
  emit('update:visible', false)
}
</script>

<style scoped>
.drawer-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.35);
  display: flex;
  justify-content: flex-end;
  z-index: 1000;
  animation: fadeIn 0.15s ease-out;
}

.drawer-container {
  width: 520px;
  max-width: 90vw;
  background: #ffffff;
  height: 100%;
  display: flex;
  flex-direction: column;
  box-shadow: -4px 0 16px rgba(0, 0, 0, 0.1);
  animation: slideIn 0.2s ease-out;
}

.drawer-header {
  height: 52px;
  padding: 0 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid #e8ecef;
}

.header-title {
  display: flex;
  align-items: center;
  gap: 10px;
}

.badge-type {
  font-size: 11px;
  color: #2468f2;
  background: #e8f1ff;
  padding: 2px 6px;
  border-radius: 3px;
  font-weight: 500;
}

.header-title h3 {
  font-size: 14.5px;
  font-weight: 600;
  color: #1f2d3d;
  margin: 0;
}

.drawer-close-btn {
  background: none;
  border: none;
  font-size: 20px;
  color: #909399;
  cursor: pointer;
  padding: 0;
  line-height: 1;
}

.drawer-close-btn:hover {
  color: #303133;
}

.drawer-body {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
}

.detail-section {
  margin-bottom: 24px;
}

.section-title {
  font-size: 13.5px;
  font-weight: 600;
  color: #1f2d3d;
  margin-bottom: 12px;
  padding-left: 8px;
  border-left: 3px solid #2468f2;
}

.grid-props {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px 16px;
}

.prop-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.prop-label {
  font-size: 12px;
  color: #8c8c8c;
}

.prop-val {
  font-size: 13px;
  color: #333333;
  word-break: break-all;
}

.prop-val.font-mono {
  font-family: monospace;
  font-size: 12px;
}

.prop-val.font-bold {
  font-weight: 600;
  color: #1f2d3d;
}

.text-primary {
  color: #2468f2;
}

.text-gray {
  color: #8c8c8c;
  font-size: 12px;
}

.status-val {
  display: flex;
  align-items: center;
  gap: 6px;
}

.status-dot {
  width: 6px;
  height: 6px;
  background: #52c41a;
  border-radius: 50%;
}

.mount-box {
  background: #f7f9fb;
  border: 1px solid #e8ecef;
  border-radius: 4px;
  padding: 12px 14px;
}

.mount-tip {
  font-size: 12.5px;
  color: #606266;
  margin-bottom: 8px;
}

.snapshot-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 12px;
}

.drawer-footer {
  height: 52px;
  padding: 0 20px;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 12px;
  border-top: 1px solid #e8ecef;
  background: #fafbfc;
}

.btn {
  height: 32px;
  padding: 0 16px;
  border-radius: 3px;
  font-size: 13px;
  cursor: pointer;
}

.btn-default {
  background: #ffffff;
  border: 1px solid #dcdfe6;
  color: #606266;
}

.btn-default:hover {
  border-color: #2468f2;
  color: #2468f2;
}

.btn-primary {
  background: #2468f2;
  border: 1px solid #2468f2;
  color: #ffffff;
}

.btn-primary:hover {
  background: #1855d1;
}

@keyframes slideIn {
  from { transform: translateX(100%); }
  to { transform: translateX(0); }
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
</style>
