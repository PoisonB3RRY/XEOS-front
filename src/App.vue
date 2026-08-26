<template>
  <div class="app-layout">
    <!-- Top Global Header -->
    <Header />

    <!-- Main Container (Sidebar + Content Area) -->
    <div class="main-body">
      <!-- Left Navigation Sidebar -->
      <Sidebar />

      <!-- Right Content Layout -->
      <div class="content-wrapper">
        <!-- Tab Navigation Bar -->
        <TabBar />

        <!-- Scrollable Page Container -->
        <main class="page-content">
          <BucketDetail />
        </main>
      </div>
    </div>
  </div>
</template>

<script setup>
import Header from './components/Header.vue'
import Sidebar from './components/Sidebar.vue'
import TabBar from './components/TabBar.vue'
import BucketDetail from './components/BucketDetail.vue'
</script>

<style scoped>
.app-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f0f2f5;
}

.main-body {
  flex: 1;
  display: flex;
  overflow: hidden;
}

.content-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  background-color: #f0f2f5;
}

.page-content {
  flex: 1;
  padding: 12px 16px 20px;
  overflow-y: auto;
}
</style>
