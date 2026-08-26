<template>
  <div class="basic-info-container">
    <div class="info-grid">
      <div class="info-item">
        <span class="info-label">实例名称：</span>
        <span class="info-value">jgh-kf-bucket-testpulsar2</span>
      </div>
      <div class="info-item">
        <span class="info-label">资源组织：</span>
        <span class="info-value">浦发银行租户</span>
      </div>
      <div class="info-item">
        <span class="info-label">所属区域：</span>
        <span class="info-value">上海 (SH)</span>
      </div>
      <div class="info-item">
        <span class="info-label">所属集群：</span>
        <span class="info-value">cluster-stdcsp</span>
      </div>
      <div class="info-item">
        <span class="info-label">容量配额：</span>
        <span class="info-value">100 GB</span>
      </div>
      <div class="info-item">
        <span class="info-label">多版本状态：</span>
        <span class="info-value status-open">已开启</span>
      </div>
      <div class="info-item">
        <span class="info-label">创建时间：</span>
        <span class="info-value">2026-06-18 13:50:40</span>
      </div>
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
.basic-info-container {
  padding: 24px 20px;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px 40px;
  max-width: 800px;
}

.info-item {
  display: flex;
  font-size: 13px;
}

.info-label {
  color: #718096;
  width: 100px;
  flex-shrink: 0;
}

.info-value {
  color: #2d3748;
  font-weight: 500;
}

.status-open {
  color: #52c41a;
}
</style>
