import puppeteer from 'puppeteer'
import { acceptCookies, declineNotifications } from 'utils'

const baseUrl = 'https://www.wowhead.com'

const browser = await puppeteer.launch(
  process.env.DEBUG ? { headless: false, slowMo: 250 } : {},
)
const page = await browser.newPage()
await page.goto(baseUrl + '/achievements')

await acceptCookies(page)
await declineNotifications(page)

const [el] = await page.$x('//*[@id="fi"]/form/div[1]/h1')
const title = await el.getProperty('textContent')
console.log(await title.jsonValue())

await browser.close()
