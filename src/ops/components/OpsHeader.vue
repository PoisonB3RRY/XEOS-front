<template>
  <header class="ops-header">
    <div class="header-left">
      <!-- Bank Logo -->
      <div class="bank-logo" @click="handleLogoClick">
        <div class="logo-icon">
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

      <!-- Top Navigation Tabs -->
      <nav class="top-nav">
        <a 
          v-for="item in navList" 
          :key="item.id"
          :class="['nav-item', { active: currentNav === item.id }]"
          @click="selectNav(item.id)"
        >
          {{ item.name }}
        </a>
      </nav>
    </div>

    <div class="header-right">
      <!-- Portal Switch Pill -->
      <a href="http://localhost:3000/" target="_blank" class="portal-badge" title="前往租户运营门户 (3000端口)">
        <span class="dot"></span>
        前往租户运营门户 (3000)
      </a>

      <!-- User Profile -->
      <div class="user-profile" @click="showMenu = !showMenu">
        <span class="user-avatar-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
            <circle cx="12" cy="7" r="4" />
          </svg>
        </span>
        <span class="user-id">12014844</span>
        <span class="user-arrow">▾</span>

        <!-- Dropdown Menu -->
        <div v-if="showMenu" class="user-dropdown" @click.stop>
          <div class="dropdown-header">
            <span class="dropdown-name">系统管理员</span>
            <span class="dropdown-role">运维管理专员</span>
          </div>
          <div class="dropdown-divider"></div>
          <a href="http://localhost:3000/" target="_blank" class="dropdown-item">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" />
              <polyline points="15 3 21 3 21 9" />
              <line x1="10" y1="14" x2="21" y2="3" />
            </svg>
            切换到运营门户 (3000)
          </a>
          <div class="dropdown-item" @click="showMenu = false">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="3" />
              <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z" />
            </svg>
            个人设置
          </div>
          <div class="dropdown-divider"></div>
          <div class="dropdown-item logout" @click="showMenu = false">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
              <polyline points="16 17 21 12 16 7" />
              <line x1="21" y1="12" x2="9" y2="12" />
            </svg>
            退出登录
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref } from 'vue'

const emit = defineEmits(['select-nav', 'go-home'])

const currentNav = ref('cloud-ops')
const showMenu = ref(false)

const navList = [
  { id: 'xuanwu-ops', name: '玄武云运维' },
  { id: 'xinchuang-ops', name: '信创云运维' },
  { id: 'cloud-ops', name: '云运维' }
]

const selectNav = (id) => {
  currentNav.value = id
  emit('select-nav', id)
}

const handleLogoClick = () => {
  emit('go-home')
}
</script>

<style scoped>
.ops-header {
  height: 50px;
  background-color: #ffffff;
  border-bottom: 1px solid #e5e9f2;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px 0 20px;
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
  margin-right: 36px;
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
  padding: 0 20px;
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
  left: 20px;
  right: 20px;
  height: 2.5px;
  background-color: #2468f2;
  border-radius: 2px 2px 0 0;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.portal-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 10px;
  border-radius: 12px;
  background-color: #f0f5ff;
  border: 1px solid #adc6ff;
  color: #2f54eb;
  font-size: 12px;
  text-decoration: none;
  transition: all 0.2s;
}

.portal-badge:hover {
  background-color: #2f54eb;
  color: #ffffff;
}

.portal-badge .dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background-color: #52c41a;
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 4px;
  position: relative;
  transition: background-color 0.2s;
}

.user-profile:hover {
  background-color: #f5f7fa;
}

.user-avatar-icon {
  display: flex;
  align-items: center;
  color: #8c8c8c;
}

.user-avatar-icon svg {
  width: 16px;
  height: 16px;
}

.user-id {
  font-size: 13px;
  color: #333333;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

.user-arrow {
  font-size: 10px;
  color: #8c8c8c;
}

.user-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 8px;
  width: 180px;
  background: #ffffff;
  border-radius: 6px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
  border: 1px solid #ebeef5;
  padding: 6px 0;
  z-index: 1000;
}

.dropdown-header {
  padding: 8px 16px;
  display: flex;
  flex-direction: column;
}

.dropdown-name {
  font-weight: 600;
  color: #1f2329;
  font-size: 13px;
}

.dropdown-role {
  color: #8f959e;
  font-size: 11px;
}

.dropdown-divider {
  height: 1px;
  background: #f0f2f5;
  margin: 4px 0;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  font-size: 12px;
  color: #333333;
  text-decoration: none;
  cursor: pointer;
  transition: background 0.15s;
}

.dropdown-item svg {
  width: 14px;
  height: 14px;
  color: #8f959e;
}

.dropdown-item:hover {
  background: #f5f7fa;
  color: #2468f2;
}

.dropdown-item:hover svg {
  color: #2468f2;
}

.dropdown-item.logout:hover {
  color: #f5222d;
}

.dropdown-item.logout:hover svg {
  color: #f5222d;
}
</style>
