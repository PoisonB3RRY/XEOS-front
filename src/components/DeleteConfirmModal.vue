<template>
  <div v-if="visible" class="modal-overlay" @click.self="close">
    <div class="modal-card">
      <div class="modal-header">
        <h3 class="modal-title">{{ modalTitle }}</h3>
        <button class="modal-close-btn" @click="close">×</button>
      </div>

      <div class="modal-body">
        <!-- Warning Alert Banner -->
        <div class="warning-banner">
          <div class="warning-icon">
            <svg viewBox="0 0 24 24" fill="#fa8c16">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/>
            </svg>
          </div>
          <div class="warning-text">
            <span>{{ warningContent }}</span>
          </div>
        </div>

        <!-- Confirmation text -->
        <div class="confirm-prompt-text">
          {{ confirmContent }}
        </div>
      </div>

      <div class="modal-footer">
        <button class="btn btn-default" @click="close">取消</button>
        <button class="btn btn-primary" @click="handleConfirm">确定</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  },
  actionType: {
    type: String, // 'delete' | 'disable' | 'enable'
    default: 'delete'
  },
  itemData: {
    type: Object,
    default: null
  },
  title: {
    type: String,
    default: ''
  },
  warningMessage: {
    type: String,
    default: ''
  },
  confirmMessage: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:visible', 'confirm'])

const modalTitle = computed(() => {
  if (props.title) return props.title
  if (props.actionType === 'disable') return '禁用'
  if (props.actionType === 'enable') return '启用'
  return '删除'
})

const warningContent = computed(() => {
  if (props.warningMessage) return props.warningMessage
  if (props.actionType === 'delete') {
    return '若两桶配置双向跨域复制策略，则默认删除两个桶的跨域复制策略。'
  }
  return '若两桶配置双向跨域复制策略，请注意对端桶跨域复制策略状态需保持一致。'
})

const confirmContent = computed(() => {
  if (props.confirmMessage) return props.confirmMessage
  if (props.actionType === 'disable') return '确认要禁用该跨域复制策略？'
  if (props.actionType === 'enable') return '确认要启用该跨域复制策略？'
  return '确认要删除该跨域复制策略？'
})

const close = () => {
  emit('update:visible', false)
}

const handleConfirm = () => {
  emit('confirm', props.itemData, props.actionType)
  close()
}
</script>

<style scoped>
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
  z-index: 1000;
  animation: fadeIn 0.15s ease;
}

.modal-card {
  width: 480px;
  background: #ffffff;
  border-radius: 4px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.modal-header {
  height: 48px;
  padding: 0 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid #f0f0f0;
}

.modal-title {
  font-size: 15px;
  font-weight: 600;
  color: #333333;
  margin: 0;
}

.modal-close-btn {
  background: none;
  border: none;
  font-size: 18px;
  color: #999999;
  cursor: pointer;
  padding: 4px;
  line-height: 1;
}

.modal-close-btn:hover {
  color: #333333;
}

.modal-body {
  padding: 20px 24px 16px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.warning-banner {
  background-color: #fffbe6;
  border: 1px solid #ffe58f;
  border-radius: 4px;
  padding: 10px 14px;
  display: flex;
  align-items: flex-start;
  gap: 10px;
}

.warning-icon {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
  margin-top: 1px;
}

.warning-icon svg {
  width: 16px;
  height: 16px;
  display: block;
}

.warning-text {
  font-size: 12px;
  color: #333333;
  line-height: 1.5;
}

.confirm-prompt-text {
  font-size: 13px;
  color: #333333;
  padding-left: 2px;
}

.modal-footer {
  padding: 12px 24px 20px;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.btn {
  height: 32px;
  padding: 0 18px;
  border-radius: 4px;
  font-size: 13px;
  cursor: pointer;
  font-weight: 400;
  transition: all 0.2s;
}

.btn-default {
  background: #ffffff;
  border: 1px solid #d9d9d9;
  color: #666666;
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
  background: #1d53c7;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
</style>
