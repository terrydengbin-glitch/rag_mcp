import { expect, test, type Page } from '@playwright/test'

async function expectMounted(page: Page) {
  await expect(page.locator('#app')).not.toBeEmpty()
  const bodyText = (await page.locator('body').innerText()).trim()
  expect(bodyText.length).toBeGreaterThan(100)
}

test('静态 JSON fixture 可以按需加载且不进入白屏', async ({ page }) => {
  const fixtureResponses: string[] = []
  page.on('response', (response) => {
    const url = response.url()
    if (url.includes('/data/') && url.endsWith('.json')) {
      fixtureResponses.push(url)
    }
  })

  await page.goto('/knowledge-tree')
  await expect(page.getByRole('heading', { name: '知识树', level: 1 })).toBeVisible()
  await expect(page.getByText('知识树数据已加载')).toBeVisible()
  await expectMounted(page)

  expect(fixtureResponses.some((url) => url.endsWith('/data/phase23Candidates.json'))).toBeTruthy()
  expect(fixtureResponses.some((url) => url.endsWith('/data/formalKnowledgeItems.json'))).toBeTruthy()
  expect(fixtureResponses.some((url) => url.endsWith('/data/knowledgeTreeNodes.json'))).toBeTruthy()
})

test('候选页刷新后继续使用懒加载数据和分页队列', async ({ page }) => {
  await page.goto('/ingestion')
  await expect(page.getByRole('heading', { name: '候选知识审计', level: 1 })).toBeVisible()
  await expect(page.getByText('静态数据已加载')).toBeVisible()
  await expect(page.getByText(/已加载 \d+ 条候选/)).toBeVisible()
  await page.getByRole('button', { name: /已沉淀知识/ }).click()
  await expect(page.locator('.candidate-row').first()).toBeVisible()
  await expect(page.locator('.queue-pagination')).toBeVisible()
  await expectMounted(page)
})

test('知识树详情页刷新后仍能显示五列知识卡和详情', async ({ page }) => {
  await page.goto('/knowledge-tree?node_id=kt.backtest.bias')
  await expect(page.getByRole('heading', { name: 'Backtest Bias', level: 2 })).toBeVisible()
  await expect(page.getByText('知识树数据已加载')).toBeVisible()
  await expect(page.locator('.knowledge-point-card').first()).toBeVisible()
  await page.locator('.knowledge-point-card').first().click()
  await expect(page.locator('.knowledge-point-detail')).toBeVisible()
  await expectMounted(page)
})
