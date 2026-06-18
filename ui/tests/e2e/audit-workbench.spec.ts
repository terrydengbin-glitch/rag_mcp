import { expect, test, type Page } from '@playwright/test'

type PageCase = {
  path: string
  heading: string
  visibleText: string[]
  stableSelectors: string[]
  screenshotName: string
}

const pageCases: PageCase[] = [
  {
    path: '/ingestion',
    heading: '候选知识审计',
    visibleText: ['审计队列', '待审计', '已沉淀知识', '当前分组没有候选', 'AI 审计包'],
    stableSelectors: ['.candidate-workbench', '.candidate-queue', '.queue-tab-row'],
    screenshotName: 'ingestion-review'
  },
  {
    path: '/knowledge-tree',
    heading: '知识树',
    visibleText: ['当前范围的知识点', '知识点内容', '待补缺口', '审计摘要'],
    stableSelectors: ['.knowledge-tree-reading-shell', '.tree-reader-sidebar', '.knowledge-card-grid', '.tree-audit-rail'],
    screenshotName: 'knowledge-tree'
  },
  {
    path: '/search-lab',
    heading: '检索测试台',
    visibleText: ['命中结果', '阻断结果'],
    stableSelectors: ['.two-column', '.search-lab-panel', '.match-list'],
    screenshotName: 'search-lab'
  }
]

async function expectNoBlankPage(page: Page) {
  const text = (await page.locator('body').innerText()).trim()
  expect(text.length).toBeGreaterThan(100)
  await expect(page.locator('body')).toBeVisible()
}

async function expectNoHorizontalOverflow(page: Page) {
  const overflow = await page.evaluate(() => {
    const root = document.documentElement
    return {
      scrollWidth: root.scrollWidth,
      clientWidth: root.clientWidth,
      bodyScrollWidth: document.body.scrollWidth
    }
  })
  expect(overflow.scrollWidth).toBeLessThanOrEqual(overflow.clientWidth + 2)
  expect(overflow.bodyScrollWidth).toBeLessThanOrEqual(overflow.clientWidth + 2)
}

async function expectStableBoxes(page: Page, selectors: string[]) {
  for (const selector of selectors) {
    const locator = page.locator(selector).first()
    await expect(locator).toBeVisible()
    const box = await locator.boundingBox()
    expect(box, `${selector} should have a bounding box`).not.toBeNull()
    expect(box!.width, `${selector} width`).toBeGreaterThan(20)
    expect(box!.height, `${selector} height`).toBeGreaterThan(20)
  }
}

for (const scenario of pageCases) {
  test(`${scenario.screenshotName} renders with audit content`, async ({ page }, testInfo) => {
    await page.goto(scenario.path)
    await expect(page.getByRole('heading', { name: scenario.heading, level: 1 })).toBeVisible()
    for (const text of scenario.visibleText) {
      await expect(page.getByText(text).first()).toBeVisible()
    }
    await expectNoBlankPage(page)
    await expectNoHorizontalOverflow(page)
    await expectStableBoxes(page, scenario.stableSelectors)
    await page.screenshot({
      path: testInfo.outputPath(`${scenario.screenshotName}-${testInfo.project.name}.png`),
      fullPage: true
    })
  })
}

test('knowledge tree candidate link filters ingestion review', async ({ page }, testInfo) => {
  await page.goto('/knowledge-tree?node_id=kt.backtest.bias')
  await expect(page.getByRole('heading', { name: 'Backtest Bias', level: 2 })).toBeVisible()
  const candidateLink = page.getByRole('link', { name: /查看候选/ }).first()
  await expect(candidateLink).toBeVisible()
  await candidateLink.click()
  await expect(page).toHaveURL(/\/ingestion\?tree_node_id=/)
  await expect(page.getByRole('heading', { name: '候选知识审计', level: 1 })).toBeVisible()
  await expect(page.locator('.tree-filter-banner')).toBeVisible()
  await expect(page.locator('.candidate-row').first()).toBeVisible()
  await expectNoHorizontalOverflow(page)
  await page.screenshot({
    path: testInfo.outputPath(`knowledge-tree-filter-hop-${testInfo.project.name}.png`),
    fullPage: true
  })
})

test('candidate audit workbench supports checklist, risk filter, and queue pagination', async ({ page }, testInfo) => {
  await page.goto('/ingestion')
  await expect(page.getByRole('heading', { name: '候选知识审计', level: 1 })).toBeVisible()
  await expect(page.getByText('当前分组没有候选')).toBeVisible()
  await page.getByRole('button', { name: /已沉淀知识/ }).click()
  await expect(page.locator('.candidate-audit-rail')).toBeVisible()
  await expect(page.getByText('人工审核 Checklist')).toBeVisible()
  await expect(page.getByText('CEK-TA-102 交接')).toBeVisible()
  await expect(page.getByRole('button', { name: /一键导出 AI 审计包 JSON/ })).toBeVisible()
  await expect(page.locator('.queue-pagination')).toBeVisible()
  await expect(page.locator('.candidate-row').first().getByText('formalized')).toBeVisible()
  await expect(page.getByText('formalized_reviewed')).toBeVisible()

  await page.getByLabel('candidate status').selectOption('accepted_for_draft')
  await expect(page.locator('.candidate-row').first()).toBeVisible()
  await expect(page.locator('.candidate-row').first().getByText('草稿已采纳')).toBeVisible()

  await page.getByLabel('page size').selectOption('20')
  await expect(page.locator('.queue-pagination')).toContainText('1 /')
  await expectNoHorizontalOverflow(page)
  await page.screenshot({
    path: testInfo.outputPath(`candidate-audit-readability-${testInfo.project.name}.png`),
    fullPage: true
  })
})

test('knowledge tree supports three-level browse and breadcrumb return', async ({ page }, testInfo) => {
  await page.goto('/knowledge-tree')
  await expect(page.getByRole('heading', { name: '知识树' })).toBeVisible()
  await expect(page.locator('.tree-nav-row.level-one')).toHaveCount(3)
  await expect(page.locator('.tree-nav-row.level-three')).toHaveCount(0)

  await page.locator('.tree-nav-row.level-one').filter({ hasText: 'Trading Engineering' }).first().click()
  await expect(page).toHaveURL(/l1=kt\.trading_engineering/)
  await expect(page.locator('.tree-nav-row.level-two').filter({ hasText: 'Backtest' }).first()).toBeVisible()
  await expect(page.locator('.tree-nav-row.level-three')).toHaveCount(0)

  await page.locator('.tree-nav-row.level-two').filter({ hasText: 'Backtest' }).first().click()
  await expect(page).toHaveURL(/l2=kt\.backtest/)
  await expect(page.locator('.tree-nav-row.level-three').filter({ hasText: 'Backtest Bias' }).first()).toBeVisible()

  await page.locator('.tree-nav-row.level-three').filter({ hasText: 'Backtest Bias' }).first().click()
  await expect(page).toHaveURL(/l3=kt\.backtest\.bias/)
  await expect(page.getByRole('heading', { name: 'Backtest Bias', level: 2 })).toBeVisible()
  await expect(page.getByRole('heading', { name: '使用边界' })).toBeVisible()
  await expect(page.getByText('只读检索，不写知识、不审批、不交易')).toBeVisible()

  await page.locator('.tree-breadcrumb-line').getByRole('button', { name: 'Backtest', exact: true }).click()
  await expect(page).toHaveURL(/l2=kt\.backtest/)
  await expect(page).not.toHaveURL(/l3=/)
  await expectNoHorizontalOverflow(page)
  await page.screenshot({
    path: testInfo.outputPath(`knowledge-tree-three-level-browse-${testInfo.project.name}.png`),
    fullPage: true
  })
})

test('knowledge tree level2 partitions align to core and Phase 38 partition contract', async ({ page }) => {
  await page.goto('/knowledge-tree')
  const expected = [
    {
      root: 'Trading Engineering',
      count: 12,
      texts: [
        'Quant Foundation',
        'Data Engineering',
        'Trade Analysis',
        'Market Conduct',
        'Market Access',
        'Audit Trace'
      ]
    },
    {
      root: 'AI Engineering',
      count: 22,
      texts: [
        'LLM Training',
        'Hybrid Scoring',
        'Numeric Scoring And Meta Labeling',
        'RAG Engineering',
        'MCP And Agent Engineering',
        'Security Governance',
        'Supply Chain Governance',
        'Database Data Contract And Storage Engineering',
        'External Project AI Memory Layer'
      ]
    },
    { root: 'Project Integration', count: 3, texts: ['Project Adapter', 'External Project Healthcheck', 'Knowledge Contribution'] }
  ]

  let total = 0
  for (const group of expected) {
    await page.locator('.tree-nav-row.level-one').filter({ hasText: group.root }).first().click()
    const level2Buttons = page.locator('.tree-nav-row.level-two')
    await expect(level2Buttons).toHaveCount(group.count)
    for (const text of group.texts) {
      await expect(level2Buttons.filter({ hasText: text }).first()).toBeVisible()
    }
    total += group.count
  }
  expect(total).toBe(37)
})

test('knowledge tree shows Phase 38 RAG pack as level3 topic', async ({ page }) => {
  await page.goto('/knowledge-tree?node_id=kt.ai_engineering.rag_engineering.trading_scoring_rag_pack')
  await expect(page.locator('.tree-nav-row.level-two').filter({ hasText: 'RAG Engineering' }).first()).toBeVisible()
  await expect(page.locator('.tree-nav-row.level-three').filter({ hasText: 'Trading Scoring RAG Pack' }).first()).toBeVisible()
})

test('knowledge tree resolves legacy node_id query into three-level state', async ({ page }) => {
  await page.goto('/knowledge-tree?node_id=kt.backtest.bias')
  await expect(page.getByRole('heading', { name: 'Backtest Bias', level: 2 })).toBeVisible()
  await expect(page.locator('.tree-nav-row.level-one').filter({ hasText: 'Trading Engineering' }).first()).toHaveClass(/is-active/)
  await expect(page.locator('.tree-nav-row.level-three').filter({ hasText: 'Backtest Bias' }).first()).toHaveClass(/is-active/)
  await expectNoHorizontalOverflow(page)
})

test('knowledge tree detail appears before open gaps and uses five-card desktop grid', async ({ page }) => {
  await page.goto('/knowledge-tree?node_id=kt.backtest.bias')
  await expect(page.locator('.knowledge-point-card').first()).toBeVisible()
  await page.locator('.knowledge-point-card').first().click()
  const detailTop = await page.locator('.knowledge-point-detail').boundingBox()
  const gapsTop = await page.getByRole('heading', { name: '待补缺口' }).boundingBox()
  expect(detailTop).not.toBeNull()
  expect(gapsTop).not.toBeNull()
  expect(detailTop!.y).toBeLessThan(gapsTop!.y)

  const gridColumns = await page.locator('.knowledge-card-grid').evaluate((element) => {
    return getComputedStyle(element).gridTemplateColumns.split(' ').length
  })
  const viewportWidth = page.viewportSize()?.width || 0
  expect(gridColumns).toBe(viewportWidth > 960 ? 5 : 1)
})
