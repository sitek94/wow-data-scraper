import puppeteer from 'puppeteer'
import { acceptCookies, declineNotifications } from './utils'
import { scrapeAchievementsPage } from 'src/achievements'

const baseUrl = 'https://www.wowdb.com'

run()

async function run() {
  const browser = await puppeteer.launch(
    process.env.DEBUG ? { headless: false, slowMo: 250 } : {},
  )
  const page = await browser.newPage()
  await page.goto(`${baseUrl}/achievements`)

  await acceptCookies(page)
  await declineNotifications(page)

  const achievements = await scrapeAchievementsPage(page)

  console.log(achievements)

  await browser.close()
}
