import puppeteer from 'puppeteer'

const baseUrl = 'https://www.wowhead.com'

const browser = await puppeteer.launch()
const page = await browser.newPage()
await page.goto(baseUrl + '/achievements')
await page.screenshot({ path: 'example.png' })

await browser.close()
