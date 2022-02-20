import puppeteer from 'puppeteer'

const baseUrl = 'https://www.wowhead.com'

const browser = await puppeteer.launch(
  process.env.DEBUG ? { headless: false, slowMo: 250 } : {},
)
const page = await browser.newPage()
await page.goto(baseUrl + '/achievements')
await acceptCookies()
await page.screenshot({ path: 'example.png' })

await browser.close()

function acceptCookies() {
  return page.evaluate(() => {
    const acceptBtn = document.querySelector<HTMLButtonElement>(
      '#onetrust-accept-btn-handler',
    )
    acceptBtn.click()
  })
}

function sleep(ms: number) {
  return new Promise(resolve => setTimeout(resolve, ms))
}
