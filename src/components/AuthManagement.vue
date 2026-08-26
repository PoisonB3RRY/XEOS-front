<template>
  <div class="auth-container">
    <!-- Action Bar -->
    <div class="action-bar">
      <div class="left-actions">
        <button class="btn-create" @click="showAddAuth = true">
          <svg class="plus-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <line x1="12" y1="5" x2="12" y2="19"/>
            <line x1="5" y1="12" x2="19" y2="12"/>
          </svg>
          <span>创建</span>
        </button>
      </div>

      <div class="right-tools">
        <div class="search-filter-wrap">
          <select class="search-select">
            <option value="user">用户名称</option>
          </select>
          <input type="text" placeholder="请输入" class="search-input" />
          <button class="btn-search">
            <span>查询</span>
          </button>
          <button class="btn-reset">重置</button>
          <button class="btn-refresh" title="刷新">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="23 4 23 10 17 10"/>
              <polyline points="1 20 1 14 7 14"/>
              <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/>
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Table -->
    <div class="table-card">
      <table class="auth-table">
        <thead>
          <tr>
            <th>用户名称</th>
            <th>授权类型</th>
            <th>授权方式</th>
            <th>授权前缀</th>
            <th class="col-op">操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in authList" :key="index">
            <td>{{ item.username }}</td>
            <td>{{ item.authType }}</td>
            <td>{{ item.scope }}</td>
            <td>{{ item.prefix }}</td>
            <td class="col-op">
              <a class="op-link delete" @click="removeAuth(index)">移除授权</a>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const showAddAuth = ref(false)

const authList = ref([
  {
    username: 'xum-kf-20260702001',
    authType: '只读',
    scope: '全桶',
    prefix: '--'
  },
  {
    username: 'xum-kf-20260526001',
    authType: '高权限',
    scope: '全桶',
    prefix: '--'
  }
])

const removeAuth = (index) => {
  authList.value.splice(index, 1)
}
</script>

<style scoped>
.auth-container {
  padding: 16px 20px 24px;
}

.action-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.btn-create {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background-color: #2468f2;
  color: #ffffff;
  border: 1px solid #2468f2;
  height: 32px;
  padding: 0 16px;
  border-radius: 4px;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(36, 104, 242, 0.15);
}

.plus-icon {
  width: 14px;
  height: 14px;
}

.right-tools {
  display: flex;
  align-items: center;
  gap: 8px;
}

.search-filter-wrap {
  display: flex;
  align-items: center;
  gap: 8px;
}

.search-select {
  height: 32px;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  padding: 0 8px;
  font-size: 13px;
  color: #333333;
  outline: none;
  background: #ffffff;
}

.search-input {
  height: 32px;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  padding: 0 10px;
  font-size: 13px;
  color: #333333;
  width: 160px;
  outline: none;
}

.btn-search {
  height: 32px;
  padding: 0 16px;
  background-color: #2468f2;
  color: #ffffff;
  border: 1px solid #2468f2;
  border-radius: 4px;
  font-size: 13px;
  cursor: pointer;
}

.btn-reset {
  height: 32px;
  padding: 0 14px;
  background-color: #ffffff;
  color: #666666;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  font-size: 13px;
  cursor: pointer;
}

.btn-refresh {
  height: 32px;
  width: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #ffffff;
  color: #666666;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  cursor: pointer;
}

.btn-refresh svg {
  width: 15px;
  height: 15px;
}

.table-card {
  border: 1px solid #e8ecef;
  border-radius: 4px;
  background: #ffffff;
  overflow: hidden;
}

.auth-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
  font-size: 13px;
}

.auth-table th {
  background-color: #f7f9fb;
  color: #555555;
  font-weight: 500;
  padding: 12px 16px;
  border-bottom: 1px solid #e8ecef;
}

.auth-table td {
  padding: 12px 16px;
  color: #333333;
  border-bottom: 1px solid #f0f2f5;
}

.col-op {
  text-align: right;
  padding-right: 24px !important;
}

.op-link {
  color: #2468f2;
  cursor: pointer;
}

.op-link:hover {
  text-decoration: underline;
}
</style>
