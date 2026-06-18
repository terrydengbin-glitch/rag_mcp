import { expect, test } from '@playwright/test'

test('知识树大分支首屏 2 秒内可交互且不白屏', async ({ page }) => {
  const startedAt = Date.now()
  await page.goto('/knowledge-tree?node_id=kt.trading_engineering')
  await expect(page.locator('#app')).not.toBeEmpty()
  await expect(page.getByRole('heading', { name: 'Trading Engineering', level: 2 })).toBeVisible({ timeout: 2_000 })
  await expect(page.getByText('知识树数据已加载')).toBeVisible()
  await expect(page.locator('[data-testid="knowledge-card-virtual-list"]')).toBeVisible()
  expect(Date.now() - startedAt).toBeLessThanOrEqual(2_000)
})

test('知识树大分支只渲染当前虚拟窗口摘要卡', async ({ page }) => {
  await page.goto('/knowledge-tree?node_id=kt.trading_engineering')
  await expect(page.locator('[data-testid="knowledge-card-virtual-list"]')).toBeVisible()
  const initialCards = await page.locator('.knowledge-point-card').count()
  expect(initialCards).toBeGreaterThan(0)
  expect(initialCards).toBeLessThanOrEqual(40)

  await page.locator('[data-testid="knowledge-card-virtual-list"]').evaluate((element) => {
    element.scrollTop = element.scrollHeight
    element.dispatchEvent(new Event('scroll'))
  })
  await expect(page.locator('#app')).not.toBeEmpty()
  const afterScrollCards = await page.locator('.knowledge-point-card').count()
  expect(afterScrollCards).toBeLessThanOrEqual(40)
})

test('知识树短搜索不触发大范围检索并显示中文提示', async ({ page }) => {
  await page.goto('/knowledge-tree?node_id=kt.trading_engineering')
  const search = page.getByPlaceholder('搜索当前范围知识点，例如回测、成交、MCP、回灌')
  await search.fill('回')
  await expect(page.getByText('请输入至少 2 个字符后搜索')).toBeVisible()
  await expect(page.locator('#app')).not.toBeEmpty()

  await search.fill('回测')
  await expect(page.getByText('请输入至少 2 个字符后搜索')).toBeHidden()
  await expect(page.locator('[data-testid="knowledge-card-virtual-list"]')).toBeVisible()
})
