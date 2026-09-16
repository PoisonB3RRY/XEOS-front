<template>
  <div class="vm-list-card">
    <!-- Top Action Bar -->
    <div class="action-bar">
      <!-- Left Action Buttons -->
      <div class="left-actions">
        <button class="btn-create" @click="showCreateModal = true">
          <svg class="plus-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <line x1="12" y1="5" x2="12" y2="19"/>
            <line x1="5" y1="12" x2="19" y2="12"/>
          </svg>
          <span>创建</span>
        </button>

        <button class="btn-outline" @click="showTrashModal = true">
          <span>回收站</span>
        </button>

        <button class="btn-outline" @click="handleExport">
          <span>导出清单</span>
        </button>

        <div class="dropdown-wrapper">
          <button class="btn-outline btn-dropdown" @click="showBatchDropdown = !showBatchDropdown">
            <span>批量操作</span>
            <span class="arrow-down">▾</span>
          </button>
          <div v-if="showBatchDropdown" class="dropdown-menu">
            <div class="dropdown-item" @click="handleBatchAction('开机')">批量开机</div>
            <div class="dropdown-item" @click="handleBatchAction('关机')">批量关机</div>
            <div class="dropdown-item" @click="handleBatchAction('重启')">批量重启</div>
          </div>
        </div>

        <button 
          :class="['btn-outline', { 'btn-disabled': selectedRows.length === 0 }]"
          :disabled="selectedRows.length === 0"
          @click="handleBatchDelete"
        >
          <span>批量删除</span>
        </button>
      </div>

      <!-- Right Search & Filter Bar -->
      <div class="right-tools">
        <div class="search-filter-wrap">
          <select v-model="searchField" class="search-select">
            <option value="name">实例名称</option>
            <option value="ip">IP地址</option>
            <option value="owner">属主</option>
            <option value="org">资源组织</option>
          </select>

          <input 
            type="text" 
            v-model="searchKeyword" 
            placeholder="请输入" 
            class="search-input"
            @keyup.enter="handleSearch"
          />

          <button class="btn-search" @click="handleSearch">
            <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="11" cy="11" r="8"/>
              <line x1="21" y1="21" x2="16.65" y2="16.65"/>
            </svg>
            <span>查询</span>
          </button>

          <button class="btn-reset" @click="handleReset">
            <svg class="reset-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/>
              <path d="M3 3v5h5"/>
            </svg>
            <span>重置</span>
          </button>

          <!-- Column Setting Icon -->
          <button class="tool-icon-btn" title="列表设置">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="3"></circle>
              <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
            </svg>
          </button>

          <!-- Refresh Icon -->
          <button class="tool-icon-btn" @click="handleRefresh" title="刷新列表">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="23 4 23 10 17 10"/>
              <polyline points="1 20 1 14 7 14"/>
              <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/>
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Virtual Machine Table -->
    <div class="table-card">
      <table class="vm-table">
        <thead>
          <tr>
            <th class="col-checkbox">
              <input 
                type="checkbox" 
                :checked="isAllSelected" 
                @change="toggleSelectAll" 
              />
            </th>
            <th class="col-name">实例名称</th>
            <th class="col-status">状态</th>
            <th class="col-org">资源组织</th>
            <th class="col-region">区域</th>
            <th class="col-zone">可用区</th>
            <th class="col-os">操作系统</th>
            <th class="col-ip">IP地址</th>
            <th class="col-owner">属主</th>
            <th class="col-time">创建时间</th>
            <th class="col-expire">过期时间</th>
            <th class="col-op">操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in pagedVmList" :key="item.id">
            <td class="col-checkbox">
              <input 
                type="checkbox" 
                :value="item.id" 
                v-model="selectedRows" 
              />
            </td>
            <td class="col-name">
              <a class="vm-link" @click="handleOpenDetail(item, 'info')">{{ item.name }}</a>
            </td>
            <td class="col-status">
              <span :class="['status-dot-badge', item.status === '正常' ? 'status-normal' : 'status-creating']">
                <span class="dot"></span>
                <span>{{ item.status }}</span>
              </span>
            </td>
            <td class="col-org">{{ item.org }}</td>
            <td class="col-region">{{ item.region }}</td>
            <td class="col-zone">{{ item.zone }}</td>
            <td class="col-os" :title="item.os">{{ item.os }}</td>
            <td class="col-ip">{{ item.ip || '-' }}</td>
            <td class="col-owner">{{ item.owner }}</td>
            <td class="col-time">{{ item.createTime }}</td>
            <td class="col-expire">{{ item.expireTime }}</td>
            <td class="col-op">
              <div class="op-links">
                <a class="op-link" @click="handleCreateSnapshot(item)">创建快照</a>
                <a class="op-link btn-del" @click="handleDelete(item)">删除</a>
                <div class="more-wrapper">
                  <a class="op-link op-more" @click.stop="toggleRowMore(item.id)">
                    <span>更多</span>
                    <span class="arrow-down">▾</span>
                  </a>
                  <div v-if="activeRowMore === item.id" class="dropdown-menu more-dropdown">
                    <div class="dropdown-item" @click="handleOpenDetail(item, 'disk')">磁盘管理</div>
                    <div class="dropdown-item" @click="handleOpenDetail(item, 'snapshot')">快照管理</div>
                    <div class="dropdown-item" @click="alertAction('开机')">开机</div>
                    <div class="dropdown-item" @click="alertAction('重启')">重启</div>
                    <div class="dropdown-item" @click="alertAction('重置密码')">重置密码</div>
                  </div>
                </div>
              </div>
            </td>
          </tr>

          <tr v-if="filteredVmList.length === 0">
            <td colspan="12" class="empty-cell">
              <div class="empty-wrap">
                <div class="empty-text">暂无符合条件的云虚拟机实例</div>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Table Footer / Pagination -->
    <div class="table-footer">
      <div class="total-info">共 {{ filteredVmList.length }} 条</div>
      <div class="pagination">
        <button 
          :class="['page-nav-btn', { disabled: currentPage === 1 }]"
          :disabled="currentPage === 1"
          @click="currentPage--"
        >&lt;</button>

        <button 
          v-for="p in totalPages" 
          :key="p"
          :class="['page-number', { active: currentPage === p }]"
          @click="currentPage = p"
        >{{ p }}</button>

        <button 
          :class="['page-nav-btn', { disabled: currentPage >= totalPages }]"
          :disabled="currentPage >= totalPages"
          @click="currentPage++"
        >&gt;</button>

        <div class="page-size-select">10 条/页 ▾</div>
      </div>
    </div>

    <!-- Create VM Modal -->
    <div v-if="showCreateModal" class="modal-overlay" @click.self="showCreateModal = false">
      <div class="modal-card modal-lg">
        <div class="modal-header">
          <h3>创建云虚拟机</h3>
          <button class="btn-close" @click="showCreateModal = false">×</button>
        </div>
        <div class="modal-body">
          <div class="form-grid">
            <div class="form-item">
              <label>实例名称</label>
              <input v-model="newVm.name" class="form-input" placeholder="请输入实例名称" />
            </div>
            <div class="form-item">
              <label>资源组织</label>
              <input v-model="newVm.org" class="form-input" placeholder="金融云门户系统" />
            </div>
            <div class="form-item">
              <label>区域</label>
              <select v-model="newVm.region" class="form-input">
                <option value="上海">上海</option>
                <option value="北京">北京</option>
              </select>
            </div>
            <div class="form-item">
              <label>可用区</label>
              <select v-model="newVm.zone" class="form-input">
                <option value="上海裸金属一区（赵巷）">上海裸金属一区（赵巷）</option>
                <option value="上海裸金属二区（张江）">上海裸金属二区（张江）</option>
              </select>
            </div>
            <div class="form-item">
              <label>操作系统</label>
              <select v-model="newVm.os" class="form-input">
                <option value="Kylin Linux Advanced Server V10 (64-bit)">Kylin Linux Advanced Server V10 (64-bit)</option>
                <option value="CentOS 7.9 64bit">CentOS 7.9 64bit</option>
              </select>
            </div>
            <div class="form-item">
              <label>IP地址</label>
              <input v-model="newVm.ip" class="form-input" placeholder="如 190.23.55.88" />
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn-cancel" @click="showCreateModal = false">取消</button>
          <button class="btn-confirm" @click="confirmCreateVm">确认创建</button>
        </div>
      </div>
    </div>

    <!-- Trash Bin Modal -->
    <div v-if="showTrashModal" class="modal-overlay" @click.self="showTrashModal = false">
      <div class="modal-card modal-lg">
        <div class="modal-header">
          <h3>虚拟机回收站</h3>
          <button class="btn-close" @click="showTrashModal = false">×</button>
        </div>
        <div class="modal-body">
          <p class="recycle-tip">回收站中保存已删除的云虚拟机实例，可随时进行恢复或彻底删除。</p>
          <table class="vm-table inner-table">
            <thead>
              <tr>
                <th>实例名称</th>
                <th>原IP地址</th>
                <th>删除时间</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(vm, idx) in trashVms" :key="idx">
                <td>{{ vm.name }}</td>
                <td>{{ vm.ip }}</td>
                <td>{{ vm.deleteTime }}</td>
                <td>
                  <a class="op-link" @click="restoreVm(vm, idx)">恢复</a>
                  <a class="op-link btn-del" @click="purgeVm(idx)">销毁</a>
                </td>
              </tr>
              <tr v-if="trashVms.length === 0">
                <td colspan="4" class="empty-cell">回收站中暂无数据</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="modal-footer">
          <button class="btn-cancel" @click="showTrashModal = false">关闭</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const emit = defineEmits(['select-vm', 'open-disk', 'open-snapshot'])

// 10 real data items from screenshot 2 (media_1789529395308.jpg)
const vmList = ref([
  {
    id: '241c6956-2c3e-4461-b55d-afc6e4eafeb2',
    name: 'testlu01',
    status: '正常',
    org: '金融云门户系统',
    region: '上海',
    zone: '上海裸金属一区（赵巷）',
    os: 'Kylin Linux Advanced Server V10 (64-bit)',
    ip: '190.23.55.19',
    owner: '12064927',
    createTime: '2026-09-14 17:28:09',
    expireTime: '2026-12-13',
    arch: 'C86',
    cpuCores: '4',
    memory: '8GB'
  },
  {
    id: 'vm-testlu02-002',
    name: 'testlu02',
    status: '正常',
    org: '金融云门户系统',
    region: '上海',
    zone: '上海裸金属一区（赵巷）',
    os: 'Kylin Linux Advanced Server V10 (64-bit)',
    ip: '190.23.55.20',
    owner: '12064927',
    createTime: '2026-09-14 17:28:09',
    expireTime: '2026-12-13',
    arch: 'C86',
    cpuCores: '4',
    memory: '8GB'
  },
  {
    id: 'vm-test0909yml01-003',
    name: 'test0909yml01',
    status: '创建中',
    org: '金融云门户系统',
    region: '上海',
    zone: '上海裸金属一区（赵巷）',
    os: 'Kylin Linux Advanced Server V10 (64-bit)',
    ip: '11.12.34.18',
    owner: '12064927',
    createTime: '2026-09-11 15:10:09',
    expireTime: '2026-12-08',
    arch: 'C86',
    cpuCores: '4',
    memory: '8GB'
  },
  {
    id: 'vm-test0909yml02-004',
    name: 'test0909yml02',
    status: '创建中',
    org: '金融云门户系统',
    region: '上海',
    zone: '上海裸金属一区（赵巷）',
    os: 'Kylin Linux Advanced Server V10 (64-bit)',
    ip: '11.12.34.17',
    owner: '12064927',
    createTime: '2026-09-11 15:10:09',
    expireTime: '2026-12-08',
    arch: 'C86',
    cpuCores: '4',
    memory: '8GB'
  },
  {
    id: 'vm-test-iac-0911-005',
    name: 'test-iac-0911',
    status: '正常',
    org: '金融云门户系统',
    region: '上海',
    zone: '上海裸金属一区（赵巷）',
    os: 'Kylin Linux Advanced Server V10 (64-bit)',
    ip: '21.22.10.16',
    owner: '12064843',
    createTime: '2026-09-10 17:02:11',
    expireTime: '2026-09-30',
    arch: 'C86',
    cpuCores: '8',
    memory: '16GB'
  },
  {
    id: 'vm-test-iac-0910-006',
    name: 'test-iac-0910',
    status: '正常',
    org: '金融云门户系统',
    region: '上海',
    zone: '上海裸金属一区（赵巷）',
    os: 'Kylin Linux Advanced Server V10 (64-bit)',
    ip: '',
    owner: '12064843',
    createTime: '2026-09-10 15:48:50',
    expireTime: '2025-09-30',
    arch: 'C86',
    cpuCores: '8',
    memory: '16GB'
  },
  {
    id: 'vm-test111-007',
    name: 'test111',
    status: '正常',
    org: '金融云门户系统',
    region: '上海',
    zone: '上海裸金属一区（赵巷）',
    os: 'Kylin Linux Advanced Server V10 (64-bit)',
    ip: '190.23.55.16',
    owner: '12064927',
    createTime: '2026-09-10 10:23:26',
    expireTime: '2026-12-09',
    arch: 'C86',
    cpuCores: '4',
    memory: '8GB'
  },
  {
    id: 'vm-test091001-008',
    name: 'test091001',
    status: '正常',
    org: '金融云门户系统',
    region: '上海',
    zone: '上海裸金属一区（赵巷）',
    os: 'Kylin Linux Advanced Server V10 (64-bit)',
    ip: '21.32.70.15',
    owner: '12064927',
    createTime: '2026-09-10 09:42:33',
    expireTime: '2026-12-09',
    arch: 'C86',
    cpuCores: '4',
    memory: '8GB'
  },
  {
    id: 'vm-test091002-009',
    name: 'test091002',
    status: '正常',
    org: '金融云门户系统',
    region: '上海',
    zone: '上海裸金属一区（赵巷）',
    os: 'Kylin Linux Advanced Server V10 (64-bit)',
    ip: '21.32.70.14',
    owner: '12064927',
    createTime: '2026-09-10 09:42:33',
    expireTime: '2026-12-09',
    arch: 'C86',
    cpuCores: '4',
    memory: '8GB'
  },
  {
    id: 'vm-test0909yml01-010',
    name: 'test0909yml01',
    status: '正常',
    org: '金融云门户系统',
    region: '上海',
    zone: '上海裸金属一区（赵巷）',
    os: 'Kylin Linux Advanced Server V10 (64-bit)',
    ip: '11.12.34.18',
    owner: '12064927',
    createTime: '2026-09-09 17:11:11',
    expireTime: '2026-12-08',
    arch: 'C86',
    cpuCores: '4',
    memory: '8GB'
  },
  // Extra rows to reach 24 items matching pagination "共 24 条"
  ...Array.from({ length: 14 }).map((_, i) => ({
    id: `vm-extra-${i + 11}`,
    name: `test-srv-${(i + 11).toString().padStart(2, '0')}`,
    status: '正常',
    org: '金融云门户系统',
    region: '上海',
    zone: '上海裸金属一区（赵巷）',
    os: 'Kylin Linux Advanced Server V10 (64-bit)',
    ip: `190.23.55.${30 + i}`,
    owner: '12064927',
    createTime: '2026-09-08 14:20:00',
    expireTime: '2026-12-07',
    arch: 'C86',
    cpuCores: '4',
    memory: '8GB'
  }))
])

const trashVms = ref([
  {
    name: 'test-old-backup-vm',
    ip: '190.23.55.99',
    deleteTime: '2026-09-07 10:15:30'
  }
])

const selectedRows = ref([])
const searchField = ref('name')
const searchKeyword = ref('')
const currentPage = ref(1)
const pageSize = 10

const showBatchDropdown = ref(false)
const activeRowMore = ref(null)
const showCreateModal = ref(false)
const showTrashModal = ref(false)

const newVm = ref({
  name: 'testlu03',
  org: '金融云门户系统',
  region: '上海',
  zone: '上海裸金属一区（赵巷）',
  os: 'Kylin Linux Advanced Server V10 (64-bit)',
  ip: '190.23.55.25'
})

const filteredVmList = computed(() => {
  if (!searchKeyword.value.trim()) return vmList.value
  const kw = searchKeyword.value.trim().toLowerCase()
  return vmList.value.filter(item => {
    if (searchField.value === 'name') return item.name.toLowerCase().includes(kw)
    if (searchField.value === 'ip') return item.ip.toLowerCase().includes(kw)
    if (searchField.value === 'owner') return item.owner.toLowerCase().includes(kw)
    if (searchField.value === 'org') return item.org.toLowerCase().includes(kw)
    return true
  })
})

const totalPages = computed(() => {
  return Math.ceil(filteredVmList.value.length / pageSize) || 1
})

const pagedVmList = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  return filteredVmList.value.slice(start, start + pageSize)
})

const isAllSelected = computed(() => {
  return pagedVmList.value.length > 0 && pagedVmList.value.every(r => selectedRows.value.includes(r.id))
})

const toggleSelectAll = (e) => {
  if (e.target.checked) {
    const currentIds = pagedVmList.value.map(r => r.id)
    selectedRows.value = Array.from(new Set([...selectedRows.value, ...currentIds]))
  } else {
    const currentIds = pagedVmList.value.map(r => r.id)
    selectedRows.value = selectedRows.value.filter(id => !currentIds.includes(id))
  }
}

const handleSearch = () => {
  currentPage.value = 1
}

const handleReset = () => {
  searchKeyword.value = ''
  currentPage.value = 1
}

const handleRefresh = () => {
  alert('列表已刷新')
}

const handleOpenDetail = (item, tab = 'info') => {
  emit('select-vm', { item, tab })
}

const handleCreateSnapshot = (item) => {
  emit('open-snapshot', item)
}

const toggleRowMore = (id) => {
  activeRowMore.value = activeRowMore.value === id ? null : id
}

const alertAction = (action) => {
  alert(`已发送 ${action} 请求！`)
  activeRowMore.value = null
}

const handleExport = () => {
  alert('正在导出云虚拟机清单 (Excel)...')
}

const handleBatchAction = (action) => {
  if (selectedRows.value.length === 0) {
    alert('请先选择需要批量操作的云虚拟机')
    return
  }
  alert(`已对选中的 ${selectedRows.value.length} 台虚拟机执行 ${action}`)
  showBatchDropdown.value = false
}

const handleBatchDelete = () => {
  if (selectedRows.value.length === 0) return
  if (confirm(`确定批量删除选中的 ${selectedRows.value.length} 台云虚拟机吗？`)) {
    const toDelete = vmList.value.filter(vm => selectedRows.value.includes(vm.id))
    toDelete.forEach(vm => {
      trashVms.value.push({
        name: vm.name,
        ip: vm.ip,
        deleteTime: new Date().toISOString().replace('T', ' ').substring(0, 19)
      })
    })
    vmList.value = vmList.value.filter(vm => !selectedRows.value.includes(vm.id))
    selectedRows.value = []
  }
}

const handleDelete = (item) => {
  if (confirm(`确定删除云虚拟机 ${item.name} 吗？`)) {
    trashVms.value.push({
      name: item.name,
      ip: item.ip,
      deleteTime: new Date().toISOString().replace('T', ' ').substring(0, 19)
    })
    vmList.value = vmList.value.filter(v => v.id !== item.id)
  }
}

const confirmCreateVm = () => {
  if (newVm.value.name) {
    vmList.value.unshift({
      id: 'vm-' + Date.now(),
      name: newVm.value.name,
      status: '创建中',
      org: newVm.value.org,
      region: newVm.value.region,
      zone: newVm.value.zone,
      os: newVm.value.os,
      ip: newVm.value.ip,
      owner: '12064927',
      createTime: new Date().toISOString().replace('T', ' ').substring(0, 19),
      expireTime: '2026-12-31',
      arch: 'C86',
      cpuCores: '4',
      memory: '8GB'
    })
    showCreateModal.value = false
  }
}

const restoreVm = (vm, idx) => {
  trashVms.value.splice(idx, 1)
  vmList.value.unshift({
    id: 'vm-restored-' + Date.now(),
    name: vm.name,
    status: '正常',
    org: '金融云门户系统',
    region: '上海',
    zone: '上海裸金属一区（赵巷）',
    os: 'Kylin Linux Advanced Server V10 (64-bit)',
    ip: vm.ip,
    owner: '12064927',
    createTime: new Date().toISOString().replace('T', ' ').substring(0, 19),
    expireTime: '2026-12-31',
    arch: 'C86',
    cpuCores: '4',
    memory: '8GB'
  })
}

const purgeVm = (idx) => {
  trashVms.value.splice(idx, 1)
}
</script>

<style scoped>
.vm-list-card {
  background-color: #ffffff;
  border-radius: 4px;
  padding: 16px 20px 20px;
  min-height: calc(100vh - 110px);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
}

/* Action Bar */
.action-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
  flex-wrap: wrap;
  gap: 12px;
}

.left-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.btn-create {
  background-color: #2468f2;
  color: #ffffff;
  border: 1px solid #2468f2;
  height: 32px;
  padding: 0 16px;
  border-radius: 4px;
  font-size: 13px;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-create:hover {
  background-color: #1a56db;
}

.plus-icon {
  width: 14px;
  height: 14px;
}

.btn-outline {
  background-color: #ffffff;
  color: #606266;
  border: 1px solid #dcdfe6;
  height: 32px;
  padding: 0 14px;
  border-radius: 4px;
  font-size: 13px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 4px;
  transition: all 0.2s;
}

.btn-outline:hover:not(:disabled) {
  color: #2468f2;
  border-color: #2468f2;
}

.btn-disabled {
  background-color: #f5f7fa !important;
  border-color: #e4e7ed !important;
  color: #c0c4cc !important;
  cursor: not-allowed !important;
}

.dropdown-wrapper {
  position: relative;
}

.arrow-down {
  font-size: 10px;
  margin-left: 2px;
}

.dropdown-menu {
  position: absolute;
  top: 36px;
  left: 0;
  background: #ffffff;
  border: 1px solid #e8ecef;
  border-radius: 4px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 4px 0;
  z-index: 100;
  min-width: 100px;
}

.dropdown-item {
  padding: 8px 14px;
  font-size: 12.5px;
  color: #606266;
  cursor: pointer;
}

.dropdown-item:hover {
  background-color: #f5f8ff;
  color: #2468f2;
}

/* Right Tools */
.right-tools {
  display: flex;
  align-items: center;
}

.search-filter-wrap {
  display: flex;
  align-items: center;
  gap: 8px;
}

.search-select {
  height: 32px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  padding: 0 8px;
  font-size: 13px;
  color: #606266;
  background-color: #ffffff;
}

.search-input {
  height: 32px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  padding: 0 12px;
  font-size: 13px;
  color: #333333;
  width: 180px;
}

.search-input:focus, .search-select:focus {
  border-color: #2468f2;
  outline: none;
}

.btn-search {
  background-color: #2468f2;
  color: #ffffff;
  border: 1px solid #2468f2;
  height: 32px;
  padding: 0 14px;
  border-radius: 4px;
  font-size: 13px;
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-search:hover {
  background-color: #1a56db;
}

.search-icon {
  width: 13px;
  height: 13px;
}

.btn-reset {
  background-color: #ffffff;
  color: #606266;
  border: 1px solid #dcdfe6;
  height: 32px;
  padding: 0 14px;
  border-radius: 4px;
  font-size: 13px;
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-reset:hover {
  color: #2468f2;
  border-color: #2468f2;
}

.reset-icon {
  width: 13px;
  height: 13px;
}

.tool-icon-btn {
  background: none;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #606266;
  transition: all 0.2s;
}

.tool-icon-btn:hover {
  color: #2468f2;
  border-color: #2468f2;
}

.tool-icon-btn svg {
  width: 15px;
  height: 15px;
}

/* Table */
.table-card {
  flex: 1;
  border: 1px solid #e8ecef;
  border-radius: 4px;
  overflow-x: auto;
}

.vm-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 12.5px;
  text-align: left;
}

.vm-table thead tr {
  background-color: #f7f9fb;
  border-bottom: 1px solid #e8ecef;
}

.vm-table th {
  padding: 10px 12px;
  color: #4a5568;
  font-weight: 600;
  white-space: nowrap;
}

.vm-table td {
  padding: 11px 12px;
  color: #333333;
  border-bottom: 1px solid #f0f2f5;
  white-space: nowrap;
}

.vm-table tbody tr:hover {
  background-color: #f8fbff;
}

.col-checkbox {
  width: 36px;
  text-align: center;
}

.vm-link {
  color: #2468f2;
  cursor: pointer;
  font-weight: 500;
}

.vm-link:hover {
  text-decoration: underline;
}

.status-dot-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.status-dot-badge .dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
}

.status-normal {
  color: #52c41a;
}
.status-normal .dot {
  background-color: #52c41a;
}

.status-creating {
  color: #1890ff;
}
.status-creating .dot {
  background-color: #1890ff;
}

.col-os {
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
}

.col-time, .col-expire {
  color: #606266;
}

.op-links {
  display: flex;
  align-items: center;
  gap: 10px;
}

.op-link {
  color: #2468f2;
  cursor: pointer;
  text-decoration: none;
  font-size: 12.5px;
}

.op-link:hover {
  text-decoration: underline;
}

.op-more {
  display: inline-flex;
  align-items: center;
  gap: 2px;
}

.more-wrapper {
  position: relative;
}

.more-dropdown {
  right: 0;
  left: auto;
  min-width: 105px;
}

.btn-del {
  color: #606266;
}

.btn-del:hover {
  color: #f56c6c;
}

.empty-cell {
  text-align: center;
  padding: 50px;
  color: #909399;
}

/* Pagination */
.table-footer {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 16px;
  padding: 16px 4px 0;
  font-size: 13px;
  color: #606266;
}

.pagination {
  display: flex;
  align-items: center;
  gap: 6px;
}

.page-nav-btn {
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #dcdfe6;
  background-color: #ffffff;
  border-radius: 3px;
  cursor: pointer;
  color: #606266;
}

.page-nav-btn.disabled {
  color: #c0c4cc;
  cursor: not-allowed;
  background-color: #f5f7fa;
  border-color: #e4e7ed;
}

.page-number {
  min-width: 28px;
  height: 28px;
  padding: 0 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #dcdfe6;
  background-color: #ffffff;
  border-radius: 3px;
  cursor: pointer;
  color: #606266;
}

.page-number.active {
  border-color: #2468f2;
  color: #2468f2;
  font-weight: 600;
}

.page-size-select {
  border: 1px solid #dcdfe6;
  border-radius: 3px;
  padding: 4px 8px;
  font-size: 12px;
  background: #ffffff;
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-card {
  background: #ffffff;
  border-radius: 6px;
  width: 520px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  overflow: hidden;
}

.modal-lg {
  width: 650px;
}

.modal-header {
  padding: 16px 20px;
  border-bottom: 1px solid #e8ecef;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.modal-header h3 {
  margin: 0;
  font-size: 15px;
}

.btn-close {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  color: #909399;
}

.modal-body {
  padding: 20px;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.form-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-item label {
  color: #606266;
  font-size: 13px;
}

.form-input {
  height: 34px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  padding: 0 10px;
  font-size: 13px;
}

.form-input:focus {
  border-color: #2468f2;
  outline: none;
}

.modal-footer {
  padding: 12px 20px;
  border-top: 1px solid #e8ecef;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  background-color: #fafbfc;
}

.btn-cancel, .btn-confirm {
  padding: 6px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 13px;
}

.btn-cancel {
  border: 1px solid #dcdfe6;
  background: #ffffff;
  color: #606266;
}

.btn-confirm {
  border: 1px solid #2468f2;
  background: #2468f2;
  color: #ffffff;
}

.recycle-tip {
  margin: 0 0 12px;
  color: #909399;
  font-size: 12px;
}

.inner-table {
  border: 1px solid #e8ecef;
}
</style>
