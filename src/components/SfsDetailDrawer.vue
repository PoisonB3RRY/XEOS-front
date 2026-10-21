<template>
  <div v-if="visible" class="drawer-overlay" @click.self="close">
    <div class="drawer-container">
      <div class="drawer-header">
        <div class="header-title">
          <span class="badge-type">{{ instance?.type || 'SFS' }}</span>
          <h3>{{ instance?.name }}</h3>
        </div>
        <button class="drawer-close-btn" @click="close">×</button>
      </div>

      <div class="drawer-body">
        <div class="detail-section">
          <h4 class="section-title">基本信息</h4>
          <div class="grid-props">
            <div class="prop-item">
              <span class="prop-label">实例名称</span>
              <span class="prop-val">{{ instance?.name }}</span>
            </div>
            <div class="prop-item">
              <span class="prop-label">状态</span>
              <span class="prop-val status-val">
                <span class="status-dot"></span>
                <span>{{ instance?.status || '可用' }}</span>
              </span>
            </div>
            <div class="prop-item">
              <span class="prop-label">实例 ID</span>
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
              <span class="prop-label">存储类型</span>
              <span class="prop-val">{{ instance?.type }}</span>
            </div>
            <div class="prop-item">
              <span class="prop-label">总容量</span>
              <span class="prop-val font-bold">{{ instance?.capacity }} GB</span>
            </div>
            <div class="prop-item">
              <span class="prop-label">环境类型</span>
              <span class="prop-val">{{ instance?.envType || '常态环境' }}</span>
            </div>
            <div class="prop-item">
              <span class="prop-label">部署环境</span>
              <span class="prop-val font-bold">{{ instance?.env || 'DEV' }}</span>
            </div>
            <div class="prop-item">
              <span class="prop-label">协议类型</span>
              <span class="prop-val">NFS v4.1 / v3</span>
            </div>
          </div>
        </div>

        <div class="detail-section">
          <h4 class="section-title">网络与挂载配置</h4>
          <div class="grid-props">
            <div class="prop-item">
              <span class="prop-label">网络区域</span>
              <span class="prop-val">{{ instance?.netZone || '生产业务区' }}</span>
            </div>
            <div class="prop-item">
              <span class="prop-label">虚拟私有云</span>
              <span class="prop-val">{{ instance?.vpc || 'vpc-sh-prod01' }}</span>
            </div>
            <div class="prop-item">
              <span class="prop-label">关联子网</span>
              <span class="prop-val">{{ instance?.subnet || 'subnet-storage-01' }}</span>
            </div>
            <div class="prop-item">
              <span class="prop-label">安全组</span>
              <span class="prop-val">{{ instance?.securityGroup || 'sg-sfs-default' }}</span>
            </div>
            <div class="prop-item full-width">
              <span class="prop-label">挂载点地址</span>
              <span class="prop-val font-mono">190.23.55.{{ (Math.abs(hash(instance?.id || '')) % 150) + 10 }}:/{{ instance?.name }}</span>
            </div>
          </div>
        </div>

        <div class="detail-section">
          <h4 class="section-title">挂载指南 (Linux)</h4>
          <div class="mount-box">
            <div class="mount-tip">1. 安装 NFS 客户端工具：</div>
            <div class="code-block">yum install -y nfs-utils # CentOS/Kylin<br>apt-get install -y nfs-common # Ubuntu/Debian</div>
            <div class="mount-tip" style="margin-top: 10px;">2. 创建本地挂载目录并挂载：</div>
            <div class="code-block">mkdir -p /mnt/sfs<br>mount -t nfs -o vers=4.1,proto=tcp,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2 190.23.55.{{ (Math.abs(hash(instance?.id || '')) % 150) + 10 }}:/{{ instance?.name }} /mnt/sfs</div>
          </div>
        </div>
      </div>

      <div class="drawer-footer">
        <button class="btn btn-default" @click="close">关闭</button>
        <button class="btn btn-primary" @click="$emit('expand', instance)">扩容实例</button>
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

const hash = (str) => {
  let h = 0
  for (let i = 0; i < str.length; i++) {
    h = Math.imul(31, h) + str.charCodeAt(i) | 0
  }
  return h
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
  width: 540px;
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
  font-size: 15px;
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

.prop-item.full-width {
  grid-column: 1 / -1;
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
  font-size: 12px;
  color: #606266;
  margin-bottom: 4px;
}

.code-block {
  background: #282c34;
  color: #abb2bf;
  padding: 10px 12px;
  border-radius: 4px;
  font-family: monospace;
  font-size: 12px;
  line-height: 1.6;
  overflow-x: auto;
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
