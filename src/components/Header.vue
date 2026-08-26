<template>
  <header class="app-header">
    <div class="header-left">
      <div class="bank-logo">
        <div class="logo-icon">
          <!-- SPD Bank Logo Emblem -->
          <svg viewBox="0 0 100 100" class="bank-emblem">
            <path d="M50 8 C26.8 8 8 26.8 8 50 C8 73.2 26.8 92 50 92 C73.2 92 92 73.2 92 50 C92 26.8 73.2 8 50 8 Z" fill="#002A66" />
            <path d="M30 35 C30 30 40 28 50 28 C60 28 70 30 70 35 C70 42 55 45 45 47 C35 49 26 53 26 62 C26 73 38 76 50 76 C62 76 74 73 74 65 L66 65 C66 70 58 71 50 71 C42 71 34 69 34 62 C34 56 42 53 52 51 C64 49 78 45 78 35 C78 24 64 23 50 23 C36 23 22 26 22 35 Z" fill="#ffffff" />
            <path d="M38 48 Q50 42 62 48" stroke="#ffffff" stroke-width="4" fill="none" stroke-linecap="round" />
          </svg>
        </div>
        <div class="logo-text">
          <span class="cn-name">浦发银行</span>
          <span class="en-name">SPD BANK</span>
        </div>
      </div>

      <nav class="top-nav">
        <a 
          v-for="item in navList" 
          :key="item.id"
          :class="['nav-item', { active: currentNav === item.id }]"
          @click="currentNav = item.id"
        >
          {{ item.name }}
        </a>
      </nav>
    </div>

    <div class="header-right">
      <div class="action-link">
        <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" />
          <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" />
        </svg>
        <span>评价</span>
      </div>

      <div class="action-link">
        <div class="bell-wrapper">
          <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9" />
            <path d="M13.73 21a2 2 0 0 1-3.46 0" />
          </svg>
          <span class="badge">0</span>
        </div>
        <span>报障</span>
      </div>

      <div class="action-link">
        <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
        </svg>
        <span>意见箱</span>
      </div>

      <div class="divider"></div>

      <div class="icon-tools">
        <button class="tool-btn" title="消息">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z" />
          </svg>
        </button>
        <button class="tool-btn" title="帮助">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10" />
            <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3" />
            <line x1="12" y1="17" x2="12.01" y2="17" />
          </svg>
        </button>
        <button class="tool-btn" title="通知">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z" />
            <polyline points="22,6 12,13 2,6" />
          </svg>
        </button>
      </div>

      <div class="user-profile">
        <div class="user-badge">USER</div>
        <span class="user-arrow">▾</span>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref } from 'vue'

const currentNav = ref('tianji')

const navList = [
  { id: 'apaas', name: 'aPaaS' },
  { id: 'xuanwu', name: '玄武云产品' },
  { id: 'tianji', name: '天玑云产品' },
  { id: 'mscloud', name: '微软云产品' },
  { id: 'solution', name: '解决方案' },
  { id: 'resource', name: '资源管理' },
  { id: 'system', name: '系统管理' }
]
</script>

<style scoped>
.app-header {
  height: 50px;
  background-color: #ffffff;
  border-bottom: 1px solid #e5e9f2;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px 0 20px;
  user-select: none;
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.04);
  position: relative;
  z-index: 100;
}

.header-left {
  display: flex;
  align-items: center;
  height: 100%;
}

.bank-logo {
  display: flex;
  align-items: center;
  margin-right: 32px;
  cursor: pointer;
}

.bank-emblem {
  width: 28px;
  height: 28px;
  margin-right: 8px;
}

.logo-text {
  display: flex;
  flex-direction: column;
  line-height: 1.15;
}

.cn-name {
  font-size: 15px;
  font-weight: 700;
  color: #002a66;
  letter-spacing: 0.5px;
}

.en-name {
  font-size: 8px;
  font-weight: 600;
  color: #002a66;
  letter-spacing: 0.5px;
}

.top-nav {
  display: flex;
  align-items: center;
  height: 100%;
}

.nav-item {
  display: flex;
  align-items: center;
  height: 50px;
  padding: 0 16px;
  font-size: 14px;
  color: #333333;
  cursor: pointer;
  position: relative;
  transition: all 0.2s;
  font-weight: 400;
}

.nav-item:hover {
  color: #2468f2;
}

.nav-item.active {
  color: #2468f2;
  font-weight: 600;
}

.nav-item.active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 16px;
  right: 16px;
  height: 2.5px;
  background-color: #2468f2;
  border-radius: 2px 2px 0 0;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
  color: #555555;
  font-size: 13px;
}

.action-link {
  display: flex;
  align-items: center;
  gap: 4px;
  cursor: pointer;
  padding: 4px 6px;
  border-radius: 4px;
  transition: all 0.2s;
}

.action-link:hover {
  color: #2468f2;
  background-color: #f5f8ff;
}

.action-link .icon {
  width: 15px;
  height: 15px;
}

.bell-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.badge {
  position: absolute;
  top: -6px;
  right: -8px;
  background-color: #f5222d;
  color: #ffffff;
  font-size: 10px;
  height: 14px;
  min-width: 14px;
  line-height: 14px;
  text-align: center;
  border-radius: 7px;
  padding: 0 3px;
  font-weight: 500;
  transform: scale(0.85);
}

.divider {
  width: 1px;
  height: 16px;
  background-color: #e8e8e8;
  margin: 0 4px;
}

.icon-tools {
  display: flex;
  align-items: center;
  gap: 10px;
}

.tool-btn {
  background: none;
  border: none;
  cursor: pointer;
  color: #666666;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 4px;
  border-radius: 4px;
  transition: color 0.2s;
}

.tool-btn:hover {
  color: #2468f2;
}

.tool-btn svg {
  width: 16px;
  height: 16px;
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 4px;
  cursor: pointer;
  margin-left: 8px;
  padding: 3px 8px;
  border-radius: 12px;
  border: 1px solid #d9d9d9;
  background: #fbfbfb;
}

.user-badge {
  font-size: 12px;
  font-weight: 600;
  color: #2468f2;
}

.user-arrow {
  font-size: 10px;
  color: #999999;
}
</style>
