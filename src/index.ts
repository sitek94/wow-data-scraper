import path from 'path'
import puppeteer from 'puppeteer'
import { acceptCookies, declineNotifications } from './utils'

const baseUrl = 'https://www.wowhead.com'

run()

async function run() {
  const browser = await puppeteer.launch(
    process.env.DEBUG ? { headless: false, slowMo: 250 } : {},
  )
  const page = await browser.newPage()

  await page.goto(url('/character-achievements/quests/eastern-kingdoms'))

  await acceptCookies(page)
  await declineNotifications(page)

  const [el] = await page.$x(
    '//*[@id="lv-achievements"]/div[2]/div/table/tbody/tr[2]/td[2]/a',
  )
  const title = await el.getProperty('textContent')
  console.log(await title.jsonValue())

  await browser.close()
}

function url(...paths: string[]) {
  return path.join(baseUrl, ...paths)
}
