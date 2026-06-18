import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from './views/DashboardView.vue'
import KnowledgeList from './views/KnowledgeList.vue'
import KnowledgeDetail from './views/KnowledgeDetail.vue'
import ConflictReview from './views/ConflictReview.vue'
import SourceAudit from './views/SourceAudit.vue'
import TaskLog from './views/TaskLog.vue'
import ContributionQueue from './views/ContributionQueue.vue'
import IngestionReview from './views/IngestionReview.vue'
import KnowledgeTreeView from './views/KnowledgeTreeView.vue'
import ProjectIntegrationAudit from './views/ProjectIntegrationAudit.vue'
import SearchLab from './views/SearchLab.vue'
import SettingsView from './views/SettingsView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', redirect: '/dashboard' },
    { path: '/dashboard', component: DashboardView },
    { path: '/knowledge', component: KnowledgeList },
    { path: '/knowledge-tree', component: KnowledgeTreeView },
    { path: '/knowledge/:id', component: KnowledgeDetail, props: true },
    { path: '/ingestion', component: IngestionReview },
    { path: '/search-lab', component: SearchLab },
    { path: '/searchlab', redirect: '/search-lab' },
    { path: '/conflicts', component: ConflictReview },
    { path: '/sources', component: SourceAudit },
    { path: '/tasks', component: TaskLog },
    { path: '/projects', component: ProjectIntegrationAudit },
    { path: '/contributions', component: ContributionQueue },
    { path: '/settings', component: SettingsView }
  ]
})

export default router
