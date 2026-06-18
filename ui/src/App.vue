<script setup lang="ts">
import {
  BookOpenCheck,
  Database,
  FileInput,
  GitCompareArrows,
  GitBranch,
  Inbox,
  ListChecks,
  PlugZap,
  Search,
  SearchCheck,
  Settings,
  ShieldCheck
} from '@lucide/vue'

const nav = [
  { to: '/dashboard', label: '总览', icon: ShieldCheck },
  { to: '/knowledge', label: '知识', icon: Search },
  { to: '/knowledge-tree', label: '知识树', icon: GitBranch },
  { to: '/ingestion', label: '候选', icon: FileInput },
  { to: '/search-lab', label: '测试', icon: SearchCheck },
  { to: '/conflicts', label: '冲突', icon: GitCompareArrows },
  { to: '/sources', label: '来源', icon: Database },
  { to: '/tasks', label: '任务', icon: ListChecks },
  { to: '/projects', label: '接入', icon: PlugZap },
  { to: '/contributions', label: '倒灌', icon: Inbox },
  { to: '/settings', label: '设置', icon: Settings }
]
</script>

<template>
  <div class="app-shell">
    <aside class="sidebar">
      <div class="brand">
        <BookOpenCheck :size="22" />
        <div>
          <strong>DogSignal Gate</strong>
          <span>MCP</span>
        </div>
      </div>
      <nav class="nav-list">
        <RouterLink v-for="item in nav" :key="item.to" :to="item.to" class="nav-link">
          <component :is="item.icon" :size="18" />
          <span>{{ item.label }}</span>
        </RouterLink>
      </nav>
    </aside>
    <main class="main-view">
      <RouterView />
    </main>
  </div>
</template>
